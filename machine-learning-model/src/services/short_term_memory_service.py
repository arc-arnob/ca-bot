import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import pinecone
import time
import uuid
from datetime import datetime
load_dotenv()
from flask import json


class ShortTermMemoryError(Exception):
    pass


def save_to_short_term_memory(raw_conversation_log):
    try:
        index_name = 'bot-short-term-memory'
        pinecone.init(
            api_key=os.environ.get('5d14cafb-ac8a-494f-a10d-1a659a866081') or '5d14cafb-ac8a-494f-a10d-1a659a866081',
            environment="gcp-starter",
        )

        # Create or fetch Index
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension=384,  # Remember to change this dimension based on encoder
                metric='cosine'
            )

            # Wait for index to finish initialization
            while not pinecone.describe_index(index_name).status['ready']:
                time.sleep(1)

        index = pinecone.Index(index_name)

        # Fetch Model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        user_embed = context_encoding(raw_conversation_log)
        unique_id = str(uuid.uuid4())
        current_timestamp = int(time.mktime(datetime.now().timetuple()))
        metadata = {"BOT":  raw_conversation_log.get('BOT'), "USER": raw_conversation_log.get('USER'), "timestamp": current_timestamp}
        index.upsert([(unique_id, user_embed, metadata)])

    except Exception as e:
        # Catch any exception that occurs during execution
        error_message = f"An error occurred: {str(e)}"
        raise ShortTermMemoryError(error_message)


def get_recent_conversation_history(raw_convo, number_of_convo=6):
    try:
        some_related_convo = None
        index_name = 'bot-short-term-memory'
        encoded_query = context_encoding(raw_convo)
        pinecone.init(
            api_key=os.environ.get('5d14cafb-ac8a-494f-a10d-1a659a866081') or '5d14cafb-ac8a-494f-a10d-1a659a866081',
            environment="gcp-starter",
        )
        index = pinecone.Index(index_name)
        response = index.query(
            vector=encoded_query,
            top_k=number_of_convo,
            include_metadata=True
        )
        return response

    except Exception as e:
        print(e)
        error_message = f"An error occurred while fetching recent convo 001x: {str(e)}"
        raise ShortTermMemoryError(error_message)


def context_encoding(raw_conversation_log):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    bot_message = raw_conversation_log.get('BOT')
    user_message = raw_conversation_log.get('USER')
    return model.encode("When you said " + bot_message + "the user replied " + user_message).tolist()



