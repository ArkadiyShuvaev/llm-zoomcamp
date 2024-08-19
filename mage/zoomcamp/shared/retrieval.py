from elasticsearch import Elasticsearch
from pprint import pprint


es = Elasticsearch("http://elasticsearch:9200")
# index_name = "documents_2024-08-16_49-00"
index_name = "documents_2024-08-16_55-13"

question = "When is the next cohort?"
size = 5

search_query = {
        "size": size,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": question,
                        "fields": ["question", "text"],
                        "type": "best_fields",
                    }
                }
            }
        },
    }

response = es.search(index=index_name, body=search_query)
most_relevant = response["hits"]["hits"][0]
pprint(most_relevant)
pprint(response['hits'])