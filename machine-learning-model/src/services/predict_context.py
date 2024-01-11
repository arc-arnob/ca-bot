import requests


STUDY = 'study'
NOT_STUDY = 'not study'

# Test Sets
ALGEBRA = 'algebra'
GEOMETRY = 'geometry'

class InferenceError(Exception):
    pass


def ask_llm(payload):
    try:
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
        headers = {"Authorization": "Bearer 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"}
        inputs = {"inputs": payload}
        response = requests.post(api_url, headers=headers, json=inputs)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as req_error:
        print(f"Request error: {req_error}")
        raise InferenceError("Request error")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise InferenceError("Unexpected error")


def predict_context(raw_conversation):
    try:
        prompt = (f"If you said ${raw_conversation}. which one out of ${STUDY} or ${NOT_STUDY} does the intent of the "
                  f"user most matches?")
        context = ask_llm(prompt)
        switch_to_study = does_user_want_to_study(raw_conversation)
        response = {
            "context": context[0]['generated_text'],
            "rag_fetch": switch_to_study[0]['generated_text']
        }
        return response

    except InferenceError as ie:
        print(f"Inference error in predict_context: {str(ie)}")
        return {"error": str(ie)}

    except Exception as e:
        print(f"An unexpected error occurred in predict_context: {e}")
        raise InferenceError("Unexpected error in predict_context")


def does_user_want_to_study(raw_conversation):
    print(raw_conversation)
    try:
        prompt = "If I said " + raw_conversation + ". Do I want to study? Answer in yes or no."
        response = ask_llm(prompt)
        return response

    except InferenceError as ie:
        print(f"Inference error in does_user_want_to_study: {str(ie)}")
        return {"error": str(ie)}

    except Exception as e:
        print(f"An unexpected error occurred in does_user_want_to_study: {e}")
        raise InferenceError("Unexpected error in does_user_want_to_study")


def rag_specific_intents(user_statement):
    try:
        prompt = "If the user said: " + user_statement + ". Is the user asking to fetch correct or wrong answers?"
        response = ask_llm(prompt)
        return response

    except InferenceError as ie:
        print(f"Inference error in rag_specific_intents: {str(ie)}")
        return {"error": str(ie)}

    except Exception as e:
        print(f"An unexpected error occurred in rag_specific_intents: {e}")
        raise InferenceError("Unexpected error in rag_specific_intents")


def which_test_set_user_wants(user_statement):
    try:
        prompt = f'''Identify if any word from the list ({ALGEBRA}, {GEOMETRY}) is mentioned "{user_statement}". Return the matching word or respond 'none' if there is no match.'''
        response = ask_llm(prompt)
        return response[0]['generated_text'].lower()

    except InferenceError as ie:
        print(f"Inference error in rag_specific_intents: {str(ie)}")
        return {"error": str(ie)}

    except Exception as e:
        print(f"An unexpected error occurred in rag_specific_intents: {e}")
        raise InferenceError("Unexpected error in rag_specific_intents")