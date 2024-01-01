# TODO: Create or update Domain Knowledge - NOT Needed, run from separate Script
from sentence_transformers import SentenceTransformer, util
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()


# TODO: Fetch Domain Knowledge - Done
class KnowledgeFetchError(Exception):
    pass


def fetch_from_domain_knowledge(query):
    try:
        pinecone.init(
            api_key=os.environ.get('pinecone_long_term_mem'),
            environment="gcp-starter",
        )
        index_name = 'ca-v1-rag'
        index = pinecone.Index(index_name)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        encoded_query = model.encode(query).tolist()
        res = index.query(
            vector=encoded_query,
            top_k=15,
            include_metadata=True,
            include_values = True
        )
        return res.to_dict()
    except Exception as e:
        # You can log the error or handle it based on your requirements
        print(f"An error occurred: {str(e)}")
        raise KnowledgeFetchError("Error fetching knowledge from domain knowledge.")


# TODO: Store User Meta in Long Term
def remember_user():
    pass
