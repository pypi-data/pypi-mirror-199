from elasticsearch import Elasticsearch, ApiError

from shopping.config import ELK_URL, ELK_USERNAME, ELK_PASSWORD, ELK_CERTS_CA, ELK_VERIFY_CERTS, ShoppingError


# import config


def create_es_client(
        url=ELK_URL,
        user=ELK_USERNAME,
        password=ELK_PASSWORD,
        ca_certs=ELK_CERTS_CA,
        verify_certs=ELK_VERIFY_CERTS):
    try:
        if url is None:
            return None
        if ca_certs not in ['', None]:
            if verify_certs:
                if user not in [None, '']:
                    out = Elasticsearch(
                        hosts=str(url),
                        ca_certs=str(ca_certs),
                        basic_auth=(user, password),
                        verify_certs=True)
                else:
                    out = Elasticsearch(
                        hosts=str(url),
                        ca_certs=str(ca_certs),
                        verify_certs=True)
            else:
                if user not in [None, '']:
                    out = Elasticsearch(
                        hosts=str(url),
                        basic_auth=(user, password),
                        verify_certs=False)
                else:
                    out = Elasticsearch(
                        hosts=str(url),
                        verify_certs=False)
        else:
            if user not in [None, '']:
                out = Elasticsearch(
                    hosts=str(url),
                    basic_auth=(user, password),
                    verify_certs=False)
            else:
                out = Elasticsearch(
                    hosts=str(url),
                    verify_certs=False)
    # except elasticsearch.ElasticsearchException:
    except ApiError as e:
        raise ShoppingError(e)
    return out


ELASTICSEARCH_CLIENT = create_es_client()


def filter_by_word_elk(index, word):
    response = ELASTICSEARCH_CLIENT.search(
        index=index,
        body={
            "query": {
                "match": {"word.id": word}
            },
            "size": 10000
        },
    )

    results = [result["_source"] for result in response['hits']['hits']]
    count = response['hits']['total']['value']

    return {"results": results, "count": count}


def get_all_elk(index):
    response = ELASTICSEARCH_CLIENT.search(
        index=index,
        body={
            "query": {
                "match_all": {}
            },
            "size": 10000
        }
    )

    results = [result["_source"] for result in response['hits']['hits']]
    count = response['hits']['total']['value']

    return {"results": results, "count": count}


def filter_by_word_and_source_elk(word, source):
    response = ELASTICSEARCH_CLIENT.search(
        index="krilog-offer",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"word.id": word}},
                        {"match": {"source": source}}
                    ]
                }
            },
            "size": 10000
        },
    )

    results = [result["_source"] for result in response['hits']['hits']]
    return results


def filter_by_source_elk(source):
    response = ELASTICSEARCH_CLIENT.search(
        index="krilog-offer",
        body={
            "query": {
                "match": {"source": source}
            },
            "size": 10000
        },
    )

    results = [result["_source"] for result in response['hits']['hits']]

    return results


def get_words():
    try:
        response = ELASTICSEARCH_CLIENT.search(
            index="krilog-word",
            body={
                "query": {
                    "match_all": {}
                },
                "size": 100
            },
        )
        values = [[item["_source"]["id"], item["_source"]["name"]] for item in response['hits']['hits']]
        return values
    except ApiError:
        return [["", ""]]


def get_demands():
    try:
        response = ELASTICSEARCH_CLIENT.search(
            index="krilog-demand",
            body={
                "query": {
                    "match_all": {}
                },
                "size": 10000
            },
        )
        values = [[item["_source"]["id"], "{}, {} {}, {}".format(
            item["_source"]["word"]["name"], item["_source"]["quantity"],
            item["_source"]["units"], item["_source"]["organization"])] for item in response['hits']['hits']]
        return values
    except ApiError:
        return [["", ""]]


class ElkFactory:
    def __int__(self):
        self.client = ELASTICSEARCH_CLIENT

    def filter_by_word(self, index, word):
        try:
            response = self.client.search(
                index=index,
                body={
                    "query": {
                        "match": {"word.id": word}
                    },
                    "size": 10000
                },
            )
            results = [result["_source"] for result in response['hits']['hits']]
            count = response['hits']['total']['value']
            return {"results": results, "count": count}
        except ApiError as e:
            raise ShoppingError(e)

    def get_all(self, index):
        try:
            response = self.client.search(
                index=index,
                body={
                    "query": {
                        "match_all": {}
                    },
                    "size": 10000
                }
            )
            results = [result["_source"] for result in response['hits']['hits']]
            count = response['hits']['total']['value']
            return {"results": results, "count": count}
        except ApiError as e:
            raise ShoppingError(e)

    def filter_by_word_and_source(self, word, source):
        try:
            response = self.client.search(
                index="krilog-offer",
                body={
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"word.id": word}},
                                {"match": {"source": source}}
                            ]
                        }
                    },
                    "size": 10000
                },
            )
            results = [result["_source"] for result in response['hits']['hits']]
            return results
        except ApiError as e:
            raise ShoppingError(e)

    def filter_by_source(self, source):
        try:
            response = self.client.search(
                index="krilog-offer",
                body={
                    "query": {
                        "match": {"source": source}
                    },
                    "size": 10000
                },
            )
            results = [result["_source"] for result in response['hits']['hits']]
            return results
        except ApiError as e:
            raise ShoppingError(e)

    def get_words(self):
        try:
            response = self.client.search(
                index='krilog-word',
                body={
                    'query': {
                        'match_all': {}
                    },
                    'size': 100
                },
            )
            values = [[item['_source']['id'], item['_source']['name']] for item in response['hits']['hits']]
            return values
        except ApiError:
            return [['', '']]

    def get_demands(self):
        try:
            response = self.client.search(
                index='krilog-demand',
                body={
                    'query': {
                        'match_all': {}
                    },
                    'size': 10000
                },
            )
            values = [[item['_source']['id'], '{}, {} {}, {}'.format(
                item['_source']['word']['name'], item['_source']['quantity'],
                item['_source']['units'], item['_source']['organization'])] for item in response['hits']['hits']]
            return values
        except ApiError:
            return [['', '']]
