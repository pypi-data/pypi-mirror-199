# from data_mining.preprocess import strip_accents, price_mining, quantity_mining, elk_clean_and_create_address
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from math import ceil

from elasticsearch import ApiError

from shopping.elk import ELASTICSEARCH_CLIENT, filter_by_word_and_source_elk
# from data_mining.elk import ELASTICSEARCH_CLIENT, filter_by_word_and_source_elk

from shopping.preprocess import strip_accents, price_mining, quantity_mining, elk_clean_and_create_address


def sbazar_one_word(exp, blacklist, wordcore, word_decl, word_decl_re):
    offers = []
    expression = strip_accents(exp.lower()).replace(
        " ", "%20")  # převedení výrazu do podoby přímo zadatelné do sbazarové URL. Skloňuje sám, synonyma netřeba

    # počítadlo stránek
    page_number = 1
    next_number = True

    while next_number:
        response = requests.get(
            "https://www.sbazar.cz/hledej/{}/0-vsechny-kategorie/cela-cr/cena-neomezena/nejnovejsi/{}".format(
                expression, str(page_number)))
        soup = BeautifulSoup(response.text, "lxml")
        # zkoumám, zda existuje další stránka inzerátů - pokud ano, zvednu číslo stránky, jinak zastavuji cyklus
        list_of_links = soup.find_all('a', href=True)
        for tag in list_of_links:
            if tag.text == "Další":
                page_number += 1
                next_number = True
                break
            else:
                next_number = False

        # dolování seznamu inzerátů v json
        script_source = soup.find("script", src=None)
        pattern = "IMA.Cache = .+?;\n"
        raw_data = re.findall(pattern, script_source.string, re.S)
        raw_data2 = raw_data[0].split('"results":')
        b = None
        for a in raw_data2:
            if "images" in a:
                b = a
                break
        # nalezen správný kus kódu začínající results: a obsahující inzeráty - konec je potřeba nalézt počítáním závorek a pak převést do json
        if b:
            count_of_starts = 0
            count_of_ends = 0
            results_final = ""

            for znak in b:
                if znak == "[":
                    count_of_starts = count_of_starts + 1
                elif znak == "]":
                    count_of_ends = count_of_ends + 1

                results_final += znak

                if count_of_starts == count_of_ends and count_of_starts > 0:
                    break

            output = json.loads(results_final)
            # seznam inzerátů hotov, kromě description a dopočítávaných věcí už obsahují všechny údaje
            for x in output:
                my_string = None
                # vyřazuji inzeráty obsahující v nadpisu něco s blacklistových slov
                if any(word in x["name"].lower() for word in blacklist):
                    pass
                # vyřazuji inzeráty NEobsahující v nadpisu definovaný kořen slova
                elif any(core in x["name"].lower() for core in wordcore):
                    # description = "neuvedeno"  # predefine kvůli vytěžování - pokud existuje, přepíše se
                    username = ""
                    # ošetřeny nalezené výjimky - jiné eshopy apod., může tam být něco dalšího
                    if "user" in x and x["user"] is not None and "user_service" in x["user"]:
                        x["link"] = "https://www.sbazar.cz/" + x["user"]["user_service"]["shop_url"] + "/detail/" + x[
                            "seo_name"]
                        username = x["user"]["user_service"]["shop_url"]
                    elif "shop" in x:
                        username = x["shop"]["name"]
                        x["link"] = "https://www.sbazar.cz/rozbalena-nabidka/" + x["seo_name"] + "-" + x["id"]
                    elif "premise" in x:
                        username = x["premise"]["name"]
                        x["link"] = "https://www.sbazar.cz/" + str(x["premise"]["id"]) + "/detail/" + x["seo_name"]
                    else:
                        x["link"] = "https://www.sbazar.cz/"

                    # pro každý inzerát je potřeba ještě extra otevřít detail kvůli description, doluje se podobně
                    response_item = requests.get(x["link"])
                    soup_item = BeautifulSoup(response_item.text, "lxml")
                    script_source_item = soup_item.find("script", src=None)
                    pattern = "IMA.Cache = .+?;\n"
                    raw_data_item = re.findall(pattern, script_source_item.string, re.S)
                    raw_data_3 = raw_data_item[0].split('"result":')

                    for item_anno in raw_data_3:
                        if "description" in item_anno:
                            my_string = item_anno

                    # nalezen správný json s údaji o inzerátu
                    if my_string:
                        count_of_starts = 0
                        count_of_ends = 0
                        results_final = ""

                        for letter in my_string:
                            if letter == "{":
                                count_of_starts = count_of_starts + 1
                            elif letter == "}":
                                count_of_ends = count_of_ends + 1

                            results_final += letter

                            if count_of_starts == count_of_ends and count_of_starts > 0:
                                break

                        output2 = json.loads(results_final)
                        description = output2["description"] if output2["description"] else "Neuvedeno"
                        # vyřazuji inzeráty obsahující v popisu něco s blacklistových slov - pokud není, pokračuji zbylými údaji
                        if any(word in description.lower() for word in blacklist):
                            pass
                        else:
                            price = x["price"]
                            currency_offer = "Kč"
                            if price == 0:
                                price_preproc = price_mining(x["name"], description)
                                price = price_preproc["price"]
                                currency_offer = price_preproc["currency"]

                            # některé nabídky nemají lokaci, typicky jiné eshopy, které tam něco přeprodávají
                            if "locality" in x and "region" in x["locality"]:
                                locality = {
                                    "pid": "0" + str(x["id"]),
                                    # pridavam 0 pred id - bazos ma taky 9mistna id a pomlatilo by se to - tam pridavam 9
                                    "region": x["locality"]["region"],
                                    "street": x["locality"]["street"]
                                }
                                if x["locality"]["entity_type"] == "district":
                                    locality["city"] = x["locality"]["district"]
                                elif x["locality"]["entity_type"] == "quarter":
                                    locality["city"] = x["locality"]["quarter"]
                                else:  # pro entity_type municipality, ward a prip. neco dalsiho
                                    locality["city"] = x["locality"]["municipality"]
                            else:
                                locality = {
                                    "pid": "0" + str(x["id"]),
                                    "region": "",
                                    "city": "",
                                    "street": ""
                                }
                            offer_dict = {
                                "id": x["id"],
                                "url": x["link"],
                                "name_offer": x["name"],
                                "name_user": username,
                                "created": x["create_date"].replace("T", " ") if "create_date" in x else datetime.now(),
                                "fulltext": description,
                                "locality": locality,
                                "price": price,
                                "currency": currency_offer,
                                "quantity": quantity_mining(
                                    word=exp, name=x["name"], fulltext=description,
                                    word_decl=word_decl, word_decl_re=word_decl_re)["quantity"],
                                "units": quantity_mining(
                                    word=exp, name=x["name"], fulltext=description,
                                    word_decl=word_decl, word_decl_re=word_decl_re)["units"],
                                "source": "Sbazar"
                            }
                            offers.append(offer_dict)
                else:
                    pass
    return offers


def bazos_one_word(exp, blacklist, wordcore, word_decl, word_decl_re):
    offers = []
    expression = strip_accents(exp.lower()).replace(
        " ",
        "+")  # převedení výrazu do podoby přímo zadatelné do bazošové URL. Skloňuje sám, synonyma netřeba

    # zjistim pocet stranek pro dany vyraz
    response = requests.get(
        "https://www.bazos.cz/search.php?hledat={}&rubriky=www&hlokalita=&humkreis=25&cenaod=&cenado=&Submit=Hledat&kitx=ano".format(
            expression))
    soup = BeautifulSoup(response.text, "lxml")
    anno_count_pool = soup.find('div', {'class', 'listainzerat inzeratyflex'})
    count_text = anno_count_pool.find('div', {'class', 'inzeratynadpis'}).text
    count = int(count_text.split("inzerátů z ", 1)[1].replace(" ", ""))
    no_of_pages = ceil(count / 20)

    # počítadlo stránek
    page_number = 0

    while page_number < no_of_pages:
        # TODO osetrit error 403
        response = requests.get(
            "https://www.bazos.cz/search.php?hledat={}&hlokalita=&humkreis=25&cenaod=&cenado=&order=&crz={}".format(
                expression, str(page_number * 20)))
        soup = BeautifulSoup(response.text, "lxml")
        anno_list = soup.find_all('div', {'class', 'inzeraty inzeratyflex'})

        for anno in anno_list:
            name_offer = anno.find('h2', {'class', 'nadpis'}).text
            # vyřazuji inzeráty obsahující v nadpisu něco s blacklistových slov
            name_user = None
            if any(word in name_offer.lower() for word in blacklist):
                pass
            # vyřazuji inzeráty NEobsahující v nadpisu definovaný kořen slova
            elif any(core in name_offer.lower() for core in wordcore):
                fulltext = anno.find('div', {'class', 'popis'}).text
                # vyřazení inzerátů obsahující ve fulltextu něco s blacklistových slov
                if any(word in fulltext.lower() for word in blacklist):
                    pass
                else:
                    pricepool = anno.find('div', {'class', 'inzeratycena'}).text
                    if re.search('(.+?) Kč', str(pricepool)):
                        price = int(re.search('(.+?) Kč', str(pricepool)).group(1).replace(" ", ""))
                    else:
                        price = 0
                    currency = "Kč"
                    if price == 0:
                        price_preproc = price_mining(name_offer, fulltext)
                        price = price_preproc["price"]
                        currency = price_preproc["currency"]

                    '''
                    city_plus_psc = anno.find('div', {'class','inzeratylok'}).text
                    city = re.split(r'\d\d\d \d\d', city_plus_psc)[0]
                    '''

                    url = anno.a["href"]
                    idpool = re.search('\/inzerat(.+?)\/', str(url))
                    identifier = idpool.group(
                        1)  # id pro bazoš začíná lomítkem - možno odlišit příp. jinak, ale je to nutné - má taky 9místná čísla jako Sbazar, může se pomlátit, už se mi to v jednom případě stalo
                    datepool = anno.find("span", {'class', 'velikost10'})
                    datepool2 = re.search('\[(.+?)\]', str(datepool))
                    if datepool2:
                        date = datepool2.group(1)
                    else:
                        date = None

                    # pro každý inzerát je potřeba ještě extra otevřít detail kvůli jménu usera a souřadnicím
                    response_detail = requests.get(url)
                    soup_detail = BeautifulSoup(response_detail.text, "lxml")
                    detail_pool = soup_detail.find_all('td')
                    namepool = ""
                    # name = ""
                    # lat = None
                    # lon = None
                    for cell in detail_pool:
                        if "Jméno:" in str(cell):
                            namepool = cell
                            break

                    a_list = namepool.find_all("a")
                    map_link = None
                    for x in a_list:
                        if "jmeno" in str(x):
                            name_user = x.text
                        if "google.com/maps" in str(x):
                            map_link = x["href"]

                    coordinates_str = re.search('google.com\/maps\/place\/(.*)\/@', map_link)
                    c = coordinates_str.group(1)
                    lat = float(c.split(",")[0])
                    lon = float(c.split(",")[1])

                    # detail inzerátu už obsahuje souřadnice, podle nich se hledá město
                    locality = {
                        "pid": "8" + str(identifier),  # 8 náhodně vybrána pro jednoznačnou identifikaci
                        "lat": lat,
                        "lon": lon
                    }
                    offer_dict = {
                        "id": identifier,
                        "url": url,
                        "name_offer": name_offer,
                        "name_user": name_user,
                        "created": datetime.strptime(date, "%d.%m. %Y") if date else datetime.now(),
                        "fulltext": fulltext,
                        "locality": locality,
                        "price": price,
                        "currency": currency,
                        "quantity": quantity_mining(word=exp, name=name_offer, fulltext=fulltext,
                                                    word_decl=word_decl, word_decl_re=word_decl_re)["quantity"],
                        "units": quantity_mining(word=exp, name=name_offer, fulltext=fulltext,
                                                 word_decl=word_decl, word_decl_re=word_decl_re)["units"],
                        "source": "Bazoš"
                    }
                    offers.append(offer_dict)
            else:
                pass
        page_number = page_number + 1
    return offers


def elk_sbazar_one_word(word_id, word_decl, word_decl_re, delete_existing=True):
    word_object = ELASTICSEARCH_CLIENT.get(index="krilog-word", id=word_id)["_source"]
    exp = word_object["name"]
    blacklist = [res["name"] for res in word_object["restricted_words"]]
    wordcore = [word_object["word_core"], strip_accents(word_object["word_core"].lower())]

    if delete_existing:
        offer_actual = filter_by_word_and_source_elk(word_id, "Sbazar")
        for offer_old in offer_actual:
            ELASTICSEARCH_CLIENT.delete(index="krilog-offer", id=offer_old["id"])
            print("Offer s id {} byl vymazán z elk".format(offer_old["id"]))

    expression = strip_accents(exp.lower()).replace(" ",
                                                    "%20")  # převedení výrazu do podoby přímo zadatelné do sbazarové URL. Skloňuje sám, synonyma netřeba

    # počítadlo stránek
    page_number = 1
    next_number = True

    while next_number:
        response = requests.get(
            "https://www.sbazar.cz/hledej/{}/0-vsechny-kategorie/cela-cr/cena-neomezena/nejnovejsi/{}".format(
                expression, str(page_number)))
        soup = BeautifulSoup(response.text, "lxml")
        # zkoumám, zda existuje další stránka inzerátů - pokud ano, zvednu číslo stránky, jinak zastavuji cyklus
        list_of_links = soup.find_all('a', href=True)
        for tag in list_of_links:
            if tag.text == "Další":
                page_number += 1
                next_number = True
                break
            else:
                next_number = False

        # dolování seznamu inzerátů v json
        script_source = soup.find("script", src=None)
        pattern = "IMA.Cache = .+?;\n"
        raw_data = re.findall(pattern, script_source.string, re.S)
        raw_data2 = raw_data[0].split('"results":')
        b = None
        for a in raw_data2:
            if "images" in a:
                b = a
                break
        # nalezen správný kus kódu začínající results: a obsahující inzeráty - konec je potřeba nalézt počítáním závorek a pak převést do json
        if b:
            count_of_starts = 0
            count_of_ends = 0
            results_final = ""

            for znak in b:
                if znak == "[":
                    count_of_starts = count_of_starts + 1
                elif znak == "]":
                    count_of_ends = count_of_ends + 1

                results_final += znak

                if count_of_starts == count_of_ends and count_of_starts > 0:
                    break

            output = json.loads(results_final)
            # seznam inzerátů hotov, kromě description a dopočítávaných věcí už obsahují všechny údaje
            for x in output:
                # vyřazuji inzeráty obsahující v nadpisu něco s blacklistových slov
                if any(word in x["name"].lower() for word in blacklist):
                    pass
                # vyřazuji inzeráty NEobsahující v nadpisu definovaný kořen slova
                elif any(core in x["name"].lower() for core in wordcore):
                    # description = "neuvedeno"  # predefine kvůli vytěžování - pokud existuje, přepíše se
                    username = ""
                    # ošetřeny nalezené výjimky - jiné eshopy apod., může tam být něco dalšího
                    if "user" in x and x["user"] is not None:
                        x["link"] = "https://www.sbazar.cz/" + x["user"]["user_service"]["shop_url"] + "/detail/" + x[
                            "seo_name"]
                        username = x["user"]["user_service"]["shop_url"]
                    elif "shop" in x:
                        username = x["shop"]["name"]
                        x["link"] = "https://www.sbazar.cz/rozbalena-nabidka/" + x["seo_name"] + "-" + x["id"]
                    elif "premise" in x:
                        username = x["premise"]["name"]
                        x["link"] = "https://www.sbazar.cz/" + str(x["premise"]["id"]) + "/detail/" + x["seo_name"]
                    else:
                        x["link"] = "https://www.sbazar.cz/"

                    # pro každý inzerát je potřeba ještě extra otevřít detail kvůli description, doluje se podobně
                    response_item = requests.get(x["link"])
                    soup_item = BeautifulSoup(response_item.text, "lxml")
                    script_source_item = soup_item.find("script", src=None)
                    pattern = "IMA.Cache = .+?;\n"
                    raw_data_item = re.findall(pattern, script_source_item.string, re.S)
                    raw_data_3 = raw_data_item[0].split('"result":')
                    my_string = None
                    for item_anno in raw_data_3:
                        if "description" in item_anno:
                            my_string = item_anno

                    # nalezen správný json s údaji o inzerátu
                    if my_string:
                        count_of_starts = 0
                        count_of_ends = 0
                        results_final = ""

                        for letter in my_string:
                            if letter == "{":
                                count_of_starts = count_of_starts + 1
                            elif letter == "}":
                                count_of_ends = count_of_ends + 1

                            results_final += letter

                            if count_of_starts == count_of_ends and count_of_starts > 0:
                                break

                        output2 = json.loads(results_final)
                        description = output2["description"] if output2["description"] else "Neuvedeno"
                        # vyřazuji inzeráty obsahující v popisu něco s blacklistových slov - pokud není, pokračuji zbylými údaji
                        if any(word in description.lower() for word in blacklist):
                            pass
                        else:
                            price = x["price"]
                            currency_offer = "Kč"
                            if price == 0:
                                price_preproc = price_mining(x["name"], description)
                                price = price_preproc["price"]
                                currency_offer = price_preproc["currency"]

                            # některé nabídky nemají lokaci, typicky jiné eshopy, které tam něco přeprodávají
                            if "locality" in x and "region" in x["locality"]:
                                if x["locality"]["entity_type"] == "district":
                                    locality = elk_clean_and_create_address(
                                        pid="0" + str(x["id"]),
                                        # pridavam 0 pred id - bazos ma taky 9mistna id a pomlatilo by se to - tam pridavam 9
                                        region=x["locality"]["region"],
                                        city=x["locality"]["district"],
                                        street=x["locality"]["street"])
                                elif x["locality"]["entity_type"] == "quarter":
                                    locality = elk_clean_and_create_address(
                                        pid="0" + str(x["id"]),
                                        # pridavam 0 pred id - bazos ma taky 9mistna id a pomlatilo by se to - tam pridavam 9
                                        region=x["locality"]["region"],
                                        city=x["locality"]["quarter"],
                                        street=x["locality"]["street"])
                                else:  # pro entity_type municipality, ward a prip. neco dalsiho
                                    locality = elk_clean_and_create_address(
                                        pid="0" + str(x["id"]),
                                        # pridavam 0 pred id - bazos ma taky 9mistna id a pomlatilo by se to - tam pridavam 9
                                        region=x["locality"]["region"],
                                        city=x["locality"]["municipality"],
                                        street=x["locality"]["street"])

                            else:
                                locality = elk_clean_and_create_address(
                                    pid="0" + str(x["id"]),
                                    region="",
                                    city="",
                                    street="")

                            # uložení nabídky
                            # podmínku mazání ponechat, i když je nahoře delete všeho - jeden inzerát se může najít vícekrát pro různé výrazy a docházelo by k jeho multiplikaci
                            try:
                                # offer_exists = es.get(index="krilog-offer", id=x["id"])["_source"]
                                ELASTICSEARCH_CLIENT.delete(index="krilog-offer", id=x["id"])
                                print("Offer s id {} byl vymazán z elk".format(x["id"]))
                            except ApiError:
                                pass

                            anno = {"id": x["id"],
                                    "url": x["link"],
                                    "name_offer": x["name"],
                                    "name_user": username,
                                    "word": {"id": word_id, "name": exp},
                                    "created": x[
                                                   "create_date"] + ".000Z" if "create_date" in x else "2000-01-01T12:00:00.000Z",
                                    "price": price,
                                    "currency": currency_offer,
                                    "quantity": quantity_mining(word=exp, name=x["name"], fulltext=description,
                                                                word_decl=word_decl, word_decl_re=word_decl_re)[
                                        "quantity"],
                                    "units": quantity_mining(word=exp, name=x["name"], fulltext=description,
                                                             word_decl=word_decl, word_decl_re=word_decl_re)["units"],
                                    "fulltext": description,
                                    "locality": locality,
                                    "source": "Sbazar"
                                    }

                            try:
                                ELASTICSEARCH_CLIENT.update(
                                    index="krilog-offer",
                                    id=x["id"],
                                    body={"doc": anno}
                                )
                                print("Proběhla aktualizace Offer s id {}".format(x["id"]))

                            except ApiError:
                                ELASTICSEARCH_CLIENT.index(
                                    index="krilog-offer",
                                    id=x["id"],
                                    op_type="create",
                                    # body=offer,
                                    document=anno
                                )
                                print("Byla vytvorena nova Offer s id {}".format(x["id"]))

                else:
                    pass

    response = ELASTICSEARCH_CLIENT.search(
        index="krilog-offer",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"word.id": word_id}},
                        {"match": {"source": "Sbazar"}}
                    ]
                }
            },
        },
    )

    offers_new = [result["_source"] for result in response['hits']['hits']]

    return offers_new
