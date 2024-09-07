#! /usr/bin/python
from elasticsearch import Elasticsearch
import json
import warnings

import warnings
warnings.filterwarnings("ignore")

# Connexion au cluster
client = Elasticsearch(hosts = "http://@localhost:9200")

# Préciser le numéro de votre question ici.
# Si vous effectuez plusieurs requêtes pour la même question, écrivez "1-1", "1-2" ext...
question_number = "2-5"
question_number =["1-2","2-1","2-2","2-3","2-4","2-5","2-6","3-","4-1","4-2","4-3","4-4","5-1","5-2","5-3","5-4"]
query =[]
query1_2 ={
  "query": {
    "match_all": {}
  }
}
query.append(query1_2)
query2_1={
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Division Name.keyword"
      }
    }
  }
}
query.append(query2_1)
query2_2={
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Department Name.keyword"
      }
    }
  }
}
query.append(query2_2)
query2_3={
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Class Name.keyword"
      }
    }
  }
}
query.append(query2_3)
query2_4={
  "size": 0,
  "aggs": {
    "unique_makes": {
      "cardinality": {
        "field": "Clothing ID"
      }
    }
  }
}
query.append(query2_4)
query2_5={
  "size": 0,
  "aggs": {
    "division_agg": {
      "terms": {
        "field": "Division Name.keyword"
      },
      "aggs": {
        "departement_agg": {
          "terms": {
            "field": "Department Name.keyword"
          }
        }
      }
    }
  }
}
query.append(query2_5)
query2_6={
  "size": 0,
  "aggs": {
    "models_agg": {
      "terms": {
        "field": "Department Name.keyword"
      }
    }
  }
}
query.append(query2_6)
query3_={
  "query": {
    "bool": {
      "filter": {
        "term": {
          "Department Name.keyword": ""
        }
      }
    }
  }
}
query.append(query3_)
query4_1 ={
  "size": 0,
  "aggs": {
    "age_distribution": {
      "histogram": {
        "field": "Age",
        "interval": 20
      }
    }
  }
}
query.append(query4_1)

query4_2={
  "size": 0,
  "aggs": {
    "rating_stat": {
      "extended_stats": {
        "field": "Rating"
      }
    }
  }
}
query.append(query4_2)
query4_3=  {
  "size": 0,
  "aggs": {
    "division_agg": {
      "terms": {
        "field": "Class Name.keyword"
      },
      "aggs":{
        "rating":{
          "stats":{
            "field": "Rating"
          }
        }
      }
    }
  }

}
query.append(query4_3)

query4_4={
  "size": 0,
  "aggs": {
    "age_distribution": {
      "histogram": {
        "field": "Age",
        "interval": 20
      }
    },
    "agg_class": {
      "terms": {
        "field": "Class Name.keyword"
      }
    }
  }
}
query.append(query4_4)
query5_1={
  "size": 0,
  "query": {
    "range": {
      "Rating": {
        "gte": 4
      }
    }
  },
  "aggs": {
    "agg_title": {
      "terms": {
        "field": "Title.keyword",
        "size": 10
      }
    }
  }
}
query.append(query5_1)
query5_2={
  "size": 0,
  "query": {
    "range": {
      "Rating": {
        "lte": 3
      }
    }
  },
  "aggs": {
    "agg_title": {
      "terms": {
        "field": "Title.keyword",
        "size": 10
      }
    }
  }
}
query.append(query5_2)
query5_3={
  "size": 0,
  "query": {
    "range": {
      "Rating": {
        "gte": 4
      }
    }
  },
  "aggs": {
    "classname": {
      "terms": {
        "field": "Class Name.keyword",
        "size": 40
      },
      "aggs": {
        "averagerating": {
          "avg": {
            "field": "Rating"
          }
        }
      }
    }
  }
}
query.append(query5_3)
query5_4={
  "size": 0,
  "query": {
    "range": {
      "Rating": {
        "lte": 2
      }
    }
  },
  "aggs": {
    "classname": {
      "terms": {
        "field": "Class Name.keyword",
        "size": 40
      },
      "aggs": {
        "averagerating": {
          "avg": {
            "field": "Rating"
          }
        }
      }
    }
  }
}
query.append(query5_4)




# Sauvegarde de la requête et la réponse dans un fichier json

for quest, quer in zip(question_number,query):
  response = client.search(index="eval", body=quer)
  with open("./eval/{}.json".format("q_" + quest + "_response"), "w") as f:
    json.dump(dict(response), f, indent=2)

  with open("./eval/{}.json".format("q_" + quest + "_request"), "w") as f:
    json.dump(quer, f, indent=2)




# Récupération du template
template = client.indices.get_mapping()

# Sauvegarde dans un fichier json
with open("./eval/{}.json".format("index_template"), "w") as f:
  json.dump(dict(template), f, indent=2)