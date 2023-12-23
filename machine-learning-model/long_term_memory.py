#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 18:58:32 2023

@author: arnobchowdhury
"""
# %%
import requests

api_key = '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'

api_endpoint = "https://api.openai.com/v1/embeddings"

data = {
    "input": "Your text string goes here",
    "model": "text-embedding-ada-002"
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the API call
response = requests.post(api_endpoint, json=data, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract and print the embedding
    embedding = response.json()["embedding"]
    print(embedding)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}\n{response.text}")
    
    
#%%
from datasets import load_dataset

dataset = load_dataset("math_qa")
    
# %%
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

#Our sentences we like to encode
sentences = ['This framework generates embeddings for each input sentence',
    'Sentences are passed as a list of string containing 2 dog instances',
    'The quick brown fox jumps over the lazy dog.']

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

query_embedding = model.encode('What does dog do?')

print("Similarity:", util.dot_score(query_embedding, embeddings))

# %%
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

query_embedding = model.encode('What does fox do?')
passage_embedding = model.encode(['The fox ran after dog barked at it',
    'the dog bit fox',
    'The quick brown fox jumps over the lazy dog.'])

print("Similarity:", util.dot_score(query_embedding, passage_embedding)) 