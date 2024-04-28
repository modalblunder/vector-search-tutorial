import pymongo
import os
import openai

# Set your secrets
openai.api_key = os.environ['VEC_OPEN_API_KEY']
user = os.environ['VEC_APP_USER']
passW = os.environ['VEC_APP_PASS']
uri = os.environ['VEC_MONGO_URI']

client = pymongo.MongoClient(uri, username=user, password=passW)

db = client.sample_mflix
collection = db.embedded_movies

def generate_embedding(text: str):

    response = openai.embeddings.create(
        model="text-embedding-ada-002", 
        input=text
    )
    return response.data[0].embedding

query = "naval spy stories in the united states"
embedding = generate_embedding(query)
# print(embedding)

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": embedding,
    "path": "plot_embedding",
    "numCandidates": 1000,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')