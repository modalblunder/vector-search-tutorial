import pymongo
import os
import requests

user = os.environ['VEC_APP_USER']
passW = os.environ['VEC_APP_PASS']
hface_token = os.environ['HFACE_TOKEN']
uri = os.environ['VEC_MONGO_URI']
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

client = pymongo.MongoClient(uri, username=user, password=passW)
# response = client.admin.command('ping')
# print(response)
db = client.sample_mflix
collection = db.movies

def generate_embedding(text: str) -> list[float]:
    
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hface_token}"},
        json={"inputs": text})

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

# for doc in collection.find({'plot':{"$exists": True}}).limit(50):
#   embed_val = generate_embedding(doc['plot'])
#   print(embed_val)
#   doc['plot_embedding_hf'] = embed_val
#   collection.replace_one({'_id': doc['_id']}, doc)

query = "war movies in the past"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 10,
    "index": "PlotSemanticSearch",
      }}
])

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')