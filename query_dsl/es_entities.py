from pprint import pprint

import elasticsearch


class QueryType:
    fuzzy = 'fuzzy'
    geo_distance = 'geo_distance'
    match = 'match'
    match_all = 'match_all'
    multi_match = 'multi_match'
    range = 'range'
    term = 'term'


class Query:
    def build(self, query_type, *args, **kwargs):
        return getattr(self, query_type)(*args, **kwargs)

    def fuzzy(self, field_name, field_value):
        return {
            QueryType.fuzzy: {
                field_name: {
                    'value': field_value,
                },
            },
        }

    def geo_distance(self, geo_field, distance, distance_unit, lat, lon):
        return {
            QueryType.geo_distance: {
                'distance': f'{distance}{distance_unit}',
                geo_field: {
                    'lat': lat,
                    'lon': lon,
                },
            },
        }

    def match(self, field_name, field_value):
        return {
            QueryType.match: {
                field_name: field_value,
            },
        }

    def match_all(self, *args, **kwargs):
        return {
            QueryType.match_all: {},
        }

    def multi_match(self, fields_names, field_value):
        return {
            QueryType.multi_match: {
                'fields': fields_names,
                'query': field_value,
            },
        }

    def term(self, field_name, field_value):
        return {
            QueryType.term: {
                field_name: field_value,
            },
        }

    def range(self, field_name, query_terms):
        query_terms = {
            key: value for key, value in query_terms.items() if
            value is not None
        }
        return {
            QueryType.range: {
                field_name: query_terms,
            },
        }


class Client:
    def __init__(self, es_host, es_index, limit):
        self.es_host = es_host
        self.es_index = es_index
        self.es_client = elasticsearch.Elasticsearch(self.es_host)
        self.limit = limit

    def search(self, query):
        pprint(
            self.es_client.search(index=self.es_index, query=query, size=self.limit)['hits']['hits']
        )
