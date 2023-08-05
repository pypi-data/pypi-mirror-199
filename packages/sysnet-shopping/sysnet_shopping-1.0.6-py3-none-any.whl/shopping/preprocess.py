import re
import time
import unicodedata
import ruian  # https://service.sysnet.cz/SYSNET/RUIAN/1.0.2/ui/
from itertools import chain

from elasticsearch import ApiError
from pynominatim import Nominatim, NominatimReverse
# from data_mining.elk import ELASTICSEARCH_CLIENT
# import config
# from data_mining.get_tweepy import get_tweets

from shopping.config import RUIAN_API, RUIAN_HOST
from shopping.elk import ELASTICSEARCH_CLIENT
from shopping.get_tweepy import get_tweets

""" NLP Stanford CS
import stanza  # https://universaldependencies.org/treebanks/cs_pdt/index.html
stanza.download("cs")  # to se musi nainstalovat predem, ma to 230 Mb
nlp = stanza.Pipeline("cs")
text = "Ukázkový text - věta 1. Tady je věta 2."
doc = nlp(text)
doc_dict_0 = doc.sentences[0].to_dict()
doc_dict_1 = doc.sentences[1].to_dict()
PROPN - lokalita
lemma - zakladni tvar
"""

CURRENCY = {
    "Kč": ["Kč", "CZK", "kč", "KČ"],
    "EUR": ["Euro", "EUR", "€", "eur", "Eur", "EURO"]
}

UNITS = {
    "ks": ["ks", "kusů", "kusy", "kus", "kusech"]
}


def ruian_configuration():
    configuration = ruian.Configuration()
    configuration.api_key['X-API-KEY'] = RUIAN_API
    configuration.host = RUIAN_HOST
    api_instance_public = ruian.PublicApi(ruian.ApiClient(configuration))
    return api_instance_public


"""DATA MINING"""


def get_coordinates(location, city):
    api_instance_public = ruian_configuration()
    api_response = api_instance_public.search_address_ft_api(query=location)
    if city != "":
        if api_response:
            if api_response[0].locality == city and 47.9 <= float(api_response[0].coordinates.wgs.lat) <= 51.2 and \
                    11.9 <= float(api_response[0].coordinates.wgs.lon) <= 19.1:
                lat = api_response[0].coordinates.wgs.lat
                lon = api_response[0].coordinates.wgs.lon
            else:
                time.sleep(0.5)
                nom = Nominatim()
                coord = nom.query(city)
                if coord:
                    lat = coord[0]["lat"]
                    lon = coord[0]["lon"]
                else:
                    lat = None
                    lon = None
        else:
            time.sleep(0.5)
            nom = Nominatim()
            coord = nom.query(city)
            if coord:
                lat = coord[0]["lat"]
                lon = coord[0]["lon"]
            else:
                lat = None
                lon = None
    else:
        lat = None
        lon = None
    coords = [lat, lon]
    return coords


def get_address(lat, lon):
    api_instance_public = ruian_configuration()
    api_response = api_instance_public.nearby_address_wgs_api(lat=lat, lon=lon)
    city = ''
    if api_response:
        city = api_response[0].address.locality
    else:
        time.sleep(0.5)
        nomrev = NominatimReverse()
        adress = nomrev.query(lat=lat, lon=lon)
        if adress:
            adress = dict(adress)
            if 'address' in adress:
                if 'city' in adress['address']:
                    city = adress['address']['city']
                elif 'town' in adress['address']:
                    city = adress['address']['town']
                elif 'village' in adress['address']:
                    city = adress['address']['village']
    return city


LOC_STR_TO_DELETE = r"(česká republika|čr|hlavní město|hl.m.|česká repu|česká republik)"


def clean_address_coords(region="", city="", street=""):
    print('{}(region={}, city={}, street={})'.format('clean_address_coords', region, city, street))
    address = [city, street]  # ruian.search_address neumi kraj
    for item in address:
        index = address.index(item)
        item = item.lower()
        item = re.sub(LOC_STR_TO_DELETE, "", item)
        item = re.sub(" - ", "-", item)
        item = re.sub(",", "", item)
        item = re.sub(" +", " ", item)
        address[index] = item.lstrip().rstrip()
    if street != "":
        address = ", ".join(address)
    else:
        address = address[0]
    coords = get_coordinates(location=address, city=city)
    lat = coords[0]
    lon = coords[1]
    if lat is None or lon is None:
        address = city.split(" ")[0]
        print("to je nova adresa ", address)
        coords = get_coordinates(location=address, city=address)
        print(coords)
        lat = coords[0]
        lon = coords[1]
        city = address  # address_orig[1]
    return lat, lon, city


def elk_clean_and_create_address(pid, region="", city="", street=""):
    if city is None:
        city = ""
    if street is None:
        street = ""
    address_orig = [region, city, street]
    response_post = None
    try:
        locality = ELASTICSEARCH_CLIENT.get(index="krilog-locality", id=pid)["_source"]
    except ApiError:
        response = ELASTICSEARCH_CLIENT.search(
            index="krilog-locality",
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"region": region}},
                            {"match": {"city": city}},
                            {"match": {"street": street}}
                        ]
                    }
                },
            },
        )
        try:
            results = [result["_source"] for result in response['hits']['hits']]
            locality = results[0]
        except:  # [ValueError, TypeError, KeyError, IndexError]
            locality = None

    if locality and (locality["coordinates_LAT"] not in [None, ""] and locality["coordinates_LON"] not in [None, ""]):
        locality = locality
    else:
        address = [city, street]  # ruian.search_address neumi kraj
        for item in address:
            index = address.index(item)
            item = item.lower()
            item = re.sub(LOC_STR_TO_DELETE, "", item)
            item = re.sub(" - ", "-", item)
            item = re.sub(",", "", item)
            item = re.sub(" +", " ", item)
            address[index] = item.lstrip().rstrip()
        if street != "":
            address = ", ".join(address)
        else:
            address = address[0]
        coords = get_coordinates(location=address, city=city)
        lat = coords[0]
        lon = coords[1]
        if lat is None or lon is None:
            address = city.split(" ")[0]
            print("to je nova adresa ", address)
            coords = get_coordinates(location=address, city=address)
            print(coords)
            lat = coords[0]
            lon = coords[1]
            address_orig[1] = address

        if locality and (locality["coordinates_LAT"] in [None, ""] or locality["coordinates_LON"] in [None, ""]) and \
                lon is not None and lat is not None:
            response_post = ELASTICSEARCH_CLIENT.update(
                index="krilog-locality",
                id=locality["id"],
                body={"doc": {"coordinates_LAT": lat, "coordinates_LON": lon, "id": locality["id"], "region": region,
                              "city": city, "street": street}}
            )
            print('Proběhla aktualizace lokality s id {}'.format(locality["id"]))

            try:
                time.sleep(0.3)
                locality = ELASTICSEARCH_CLIENT.get(index="krilog-locality", id=locality["id"])["_source"]
            # tohle je snad blbost, to nemuze nastat
            except ApiError:
                response_post = ELASTICSEARCH_CLIENT.index(
                    index="krilog-locality",
                    id=locality["id"],
                    op_type="create",
                    # body=offer,
                    document={"coordinates_LAT": lat, "coordinates_LON": lon, "id": pid, "region": address_orig[0],
                              "city": address_orig[1], "street": address_orig[2]}
                )
                print('Byla vytvorena nova Locality s id {}'.format(locality["id"]))

        elif locality and (lon is None) and (lat is None):
            try:
                locality = ELASTICSEARCH_CLIENT.get(index="krilog-locality", id=locality["id"])["_source"]
            # taky blbost
            except ApiError:
                response_post = ELASTICSEARCH_CLIENT.index(
                    index="krilog-locality",
                    id=locality["id"],
                    op_type="create",
                    document={"coordinates_LAT": lat, "coordinates_LON": lon, "id": pid, "region": address_orig[0],
                              "city": address_orig[1], "street": address_orig[2]}
                )
                print("Byla vytvorena nova Locality s id {}".format(locality["id"]))
        else:
            response_post = ELASTICSEARCH_CLIENT.index(
                index="krilog-locality",
                id=pid,
                op_type="create",
                # body=offer,
                document={"coordinates_LAT": lat, "coordinates_LON": lon, "id": pid, "region": address_orig[0],
                          "city": address_orig[1], "street": address_orig[2]}
            )
            print("Byla vytvorena nova Locality s id {}".format(pid))

            time.sleep(0.3)
            locality = ELASTICSEARCH_CLIENT.get(index="krilog-locality", id=pid)["_source"]
    print('{}: {}'.format('elk_clean_and_create_address', response_post))
    return locality


def re_dict(dict_to_re):
    redict = list(dict.values(dict_to_re))
    redict = list(chain.from_iterable(redict))
    redict = "|".join(redict)
    return redict


def twitter_offer_mining(q, lang, count, word, word_decl, search):
    word_dict = word
    tw_offers, cols, count_results = get_tweets(word=q, lang=lang, count=count, retweet=False)
    offers_dict = []
    if count_results > 0:
        units = re_dict(UNITS)
        curr = re_dict(CURRENCY)

        for offer in tw_offers:
            source = "Twitter"
            twid = offer["id"]
            url = f"https://twitter.com/stanberger_/status/{twid}"
            name_offer = "N/A"  # u Twitteru neni
            name_user = offer["name_user"]
            word = f"{word}"
            search = f"{search}"
            created = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.strptime(offer['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            fulltext = offer["full_text"]
            city = offer["location"]  # casto se v Tw nevyplnuje

            PRICE_RE = r"(\d+[\s\d]*)\s*(" + curr + r")"
            price_all = re.findall(PRICE_RE, fulltext)
            if price_all:
                price = price_all[0][0].replace(" ", "")
                currency = price_all[0][1]
            else:
                price = 0
                currency = "neuvedeno"
            word_re = word.lower()
            if word_decl != "":
                r = r"(\d+[\s\d]*)\s*(" + word_re + r"|" + word_decl + r"|" + units + r")"
            else:
                r = r"(\d+[\s\d]*)\s*(" + word_re + r"|" + units + r")"
            quantity_all = re.findall(r, fulltext.lower())
            if quantity_all:
                quantity = quantity_all[0][0].replace(" ", "")
                units = quantity_all[0][1]
                if units == word_re:
                    units = "ks"
            else:
                quantity = 0
                units = "neuvedeno"

            offer_dict = {
                "id": twid,
                "url": url,
                "name_offer": name_offer,
                "name_user": name_user,
                "word": word_dict,
                "search": search,
                "created": created,
                "fulltext": fulltext,
                "locality": city,
                "price": price,
                "currency": currency,
                "quantity": quantity,
                "units": units,
                "source": source
            }
            offers_dict.append(offer_dict)
            cols = list(offers_dict[0].keys())
    return offers_dict, cols, count_results


def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = str(text, 'utf-8')
    except:  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def quantity_mining(word, name, fulltext, word_decl, word_decl_re):
    units_all = re_dict(UNITS)
    # units_found = ""

    word_re = word.lower()
    # word = f"{word}"
    if word_decl_re != "":
        r = r"(\d+[\s\d]*)\s*(" + word_re + r"|" + word_decl + r"|" + units_all + r")"
    else:
        r = r"(\d+[\s\d]*)\s*(" + word_re + r"|" + units_all + r")"
    quantity_all = re.findall(r, name.lower())
    if quantity_all:
        quantity_source = quantity_all[0][0]
        quantity_list = quantity_source.split(
            " ")  # s tim jeste neco vymyslet - jen kdyz mezera oddeluje trojice od konce
        try:
            quantity = int(quantity_list[-1])
        except:  # [ValueError, TypeError, KeyError, IndexError]
            try:
                quantity = int(quantity_list[-2])
            except:  # [ValueError, TypeError, KeyError, IndexError]
                quantity = 0
        if quantity > 0:
            units_found = quantity_all[0][1]
            if units_found in [word_re, word_decl]:
                units_found = "ks"
            elif units_found in units_all:
                for k, v in UNITS.items():
                    if units_found in v:
                        units_found = k
                        break
            else:
                units_found = ""
        else:
            units_found = "neuvedeno"

    else:
        quantity_all = re.findall(r, fulltext.lower())
        if quantity_all:
            quantity_source = quantity_all[0][0]
            quantity_list = quantity_source.split(
                " ")  # s tim jeste neco vymyslet - jen kdyz mezera oddeluje trojice od konce
            try:
                quantity = int(quantity_list[-1])
            except:  # [ValueError, TypeError, KeyError, IndexError]
                try:
                    quantity = int(quantity_list[-2])
                except:  # [ValueError, TypeError, KeyError, IndexError]
                    quantity = 0
            if quantity > 0:
                units_found = quantity_all[0][1]
                if units_found in [word_re, word_decl]:
                    units_found = "ks"
                elif units_found in units_all:
                    for k, v in UNITS.items():
                        if units_found in v:
                            units_found = k
                            break
                else:
                    units_found = ""
            else:
                units_found = "neuvedeno"

        else:
            quantity = 0  # [0]
            units_found = "neuvedeno"  # [0][1]

    return {"quantity": quantity, "units": units_found}


def price_mining(name, fulltext):
    curr = re_dict(CURRENCY)
    PRICE_RE = r"(\d+[\s\d]*)\s*,?\s*-?\s*(" + curr + r")"

    price_all_name = re.findall(PRICE_RE, name)
    if price_all_name:
        price_source = price_all_name[0][0]
        price_list = price_source.split(" ")
        try:
            price = int(price_list[-1])
        except:  # [ValueError, TypeError, KeyError, IndexError]
            try:
                price = int(price_list[-2])
            except:  # [ValueError, TypeError, KeyError, IndexError]
                price = 0
        currency_found = price_all_name[0][1]
    else:
        price_all_fulltext = re.findall(PRICE_RE, fulltext)
        if price_all_fulltext:
            price_source = price_all_fulltext[0][0]
            price_list = price_source.split(" ")
            try:
                price = int(price_list[-1])
            except:  # [ValueError, TypeError, KeyError, IndexError]
                try:
                    price = int(price_list[-2])
                except:  # [ValueError, TypeError, KeyError, IndexError]
                    price = 0
            currency_found = price_all_fulltext[0][1]
        else:
            price = 0
            currency_found = 'neuvedeno'
    for k, v in CURRENCY.items():
        if currency_found in v:
            currency_found = k
            break

    return {'price': price, 'currency': currency_found}
