# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# from server import server

from pymongo import MongoClient
client = MongoClient()

db = client.memory_app
collection_words = db.practise_words
collection_systems = db.accepted_memory_systems

collection_words.drop()
collection_words.insert_one({"words": [
    'cheese', 'wireframe', 'grass', 'portal', 'ball'
]})

collection_systems.drop()
collection_systems.insert_many([
    {'system': 'number_shape'},
    {'system': 'number_rhyme'},
    {'system': 'alphabet'}
])

client.close()
