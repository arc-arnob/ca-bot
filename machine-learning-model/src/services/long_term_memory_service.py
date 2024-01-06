# TODO: Create or update Domain Knowledge - NOT Needed, run from separate Script
from sentence_transformers import SentenceTransformer, util
from ..services.short_term_memory_service import get_data_for_stm_to_ltm
import pinecone
import time
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


class KnowledgeFetchError(Exception):
    pass


class UserLTMSaveError(Exception):
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
def create_or_update_user(payload):
    index_name = 'long-term-memory'
    try:
        pinecone.init(
            api_key=os.environ.get('pinecone_ltm'),
            environment="gcp-starter",
        )
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

        current_timestamp = int(time.mktime(datetime.now().timetuple()))
        model = SentenceTransformer('all-MiniLM-L6-v2')
        final_vector = model.encode(f"User {payload['user_name']} ({payload['user_id']}) interacted with the system "
                                    f"in the '{payload['context']}' context. Duri"
                                    f"ng the last test session on {payload['last_test_session_set']}, "
                                    f"the user achieved category-wise scores of Physics: "
                                    f"{payload['category_wise_score_category_1']}, Geometry: "
                                    f"{payload['category_wise_score_category_2']}, and General: "
                                    f"{payload['category_wise_score_category_3']}. The user's last reported state of "
                                    f"mind was '{payload['last_state_of_mind']}'.")
        metadata = payload
        index.upsert([(payload["user_id"], final_vector.tolist(), metadata)])

    except Exception as e:
        # You can log the error or handle it based on your requirements
        print(f"An error occurred: {str(e)}")
        raise UserLTMSaveError("Error fetching knowledge from long term memory.")


def stm_to_ltm_migration():
    # Fetch from STM
    # empty STM
    # Loop 1 for context general_convo
    # save to LTM
    # Loop 2 context quiz data
    # Save to LTM
    # Update user metadata
    data = get_data_for_stm_to_ltm()
    print(data)
