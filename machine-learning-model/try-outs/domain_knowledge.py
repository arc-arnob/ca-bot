#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:20:45 2023

@author: arnobchowdhury
"""

# Setup
from datasets import load_dataset
import os
from langchain.vectorstores import Pinecone
# Pine Code Vector DB setup
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Embeddings
from langchain.embeddings import HuggingFaceEmbeddings

dataset = load_dataset("math_qa", split="train")


#%%
print(dataset[0])
df = dataset.to_pandas()

#%% Preparing Knowldege Data from Embedding
import json

def create_one_liner_prompts(datasets):
    prompts = []
    for dataset in datasets:
        prompt = f'Problem: {dataset["Problem"]}\nOptions: {dataset["options"]}\nCorrect Answer: {dataset["correct"]}\nCategory: {dataset["category"]}\nExplanation: {dataset["Rationale"]}'
        prompts.append(prompt)
    return prompts

prompts = create_one_liner_prompts(dataset)

def create_one_liner_prompt(data):
    prompt = f'Problem: {dataset["Problem"]}\nOptions: {dataset["options"]}\nCorrect Answer: {dataset["correct"]}\nCategory: {dataset["category"]}\nExplanation: {dataset["Rationale"]}'
    return prompt

prompts = create_one_liner_prompts(dataset)

# %% Performing Embedding

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

#query_embedding = model.encode('Ask me a question from gain topic')
#passage_embedding = model.encode(prompts)

# %%
similarity = util.dot_score(query_embedding, passage_embedding)
print("Similarity:", util.dot_score(query_embedding, passage_embedding)[0][3]) 

#%%
# get API key from app.pinecone.io and environment from console
pinecone.init(
    api_key=os.environ.get('bac9d10e-b651-4414-8dd2-1bd94da6b85d') or 'bac9d10e-b651-4414-8dd2-1bd94da6b85d',
    environment="gcp-starter",
)

#%% Configure Pinecone
import time

index_name = 'ca-v1-rag'

if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        index_name,
        dimension=384,
        metric='cosine'
    )
    # wait for index to finish initialization
    while not pinecone.describe_index(index_name).status['ready']:
        time.sleep(1)

index = pinecone.Index(index_name)

#%%
index.describe_index_stats()

# %% 
from tqdm.auto import tqdm  # for progress bar
batch_size = 100
data = dataset.to_pandas()

for i in tqdm(range(0, len(data), batch_size)):
    i_end = min(len(data), i+batch_size)
    batch = data.iloc[i:i_end]
    ids = [f"{i}-{x['category']}" for i, x in batch.iterrows()]
    text_to_embed = [f"Problem: {dataset['Problem']}\nOptions: {dataset['options']}\nCorrect Answer: {dataset['correct']}\nCategory: {dataset['category']}\nExplanation: {dataset['Rationale']}" for _, dataset in batch.iterrows()]
    passage_embedding = model.encode(text_to_embed).tolist()
    metadata = [
        {'category': x['category'],
         'question': x['Problem'],
         'correct': x['correct'],
         'explanation': x['Rationale'],
         'options': x['options']
        } for i, x in batch.iterrows()
    ]
    index.upsert(vectors=zip(ids, passage_embedding, metadata))



# %%
queryINeed = model.encode("Can you expalain me anything about cars").tolist()
res = index.query(
  vector=queryINeed,
  top_k=1,
  include_metadata=True
)
print(res)


# %% Coversation Tagging

