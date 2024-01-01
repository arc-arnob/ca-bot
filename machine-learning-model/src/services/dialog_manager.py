from ..services.long_term_memory_service import fetch_from_domain_knowledge
from ..services.predict_context import predict_context, ask_llm
from ..services.short_term_memory_service import (save_to_short_term_memory, get_recent_conversation_history,
                                                  update_stm_metadata)


class DialogManagerError(Exception):
    pass


def lets_talk(raw_conversation):
    # Store to Short Term Memory
    save_to_short_term_memory(raw_conversation)
    # Predict Context
    user_intent = predict_context(raw_conversation['USER'])
    # if Study, fetch RAG
    domain_knowledge = None
    if user_intent['rag_fetch'] == 'yes':
        domain_knowledge = fetch_from_domain_knowledge(raw_conversation['USER'])
    recent_convos = get_recent_conversation_history(raw_conversation)
    # Else Get last few convos and Reply to most resent user conversation
    generated_dialog = generate_dialog(raw_conversation, user_intent, domain_knowledge, recent_convos)
    return generated_dialog


def generate_dialog(user_conversation, user_intent, domain_knowledge, recent_convos):
    knowledge = prompt_ready_recent_conversation(recent_convos)
    augmented_prompt = ".Use the above information to respond to the message: "
    prompt = "Below are some of the most relevant interactions from this chat: " + knowledge + " " + augmented_prompt + " " + user_conversation['USER']
    generated_dialog = ask_llm(prompt)
    return {
        "prompt": prompt,
        "generated_text": generated_dialog,
        "domain_knowledge": domain_knowledge,
        "user_intent": user_intent
    }


def prompt_ready_recent_conversation(recent_convos):
    # Combine BOT and USER messages from recent conversations
    conversation_strings = []

    for convo in recent_convos:
        bot_message = convo["metadata"]["BOT"]
        user_message = convo["metadata"]["USER"]
        conversation_strings.append(f"BOT: {bot_message} USER: {user_message}")

    # Combine all conversation strings into a single prompt
    full_prompt = "\n".join(conversation_strings)

    return full_prompt


def update_rag_with_user_response(quiz_payload):
    try:
        # Get Short term memory index
        # do something like index.update(id="id-3", set_metadata={"type": "web", "new": True})
        """
        :param quiz_payload:
        :return:
        """
        update_id = quiz_payload['rag_data']['id']
        values = quiz_payload['rag_data']['values']
        user_response = quiz_payload['user_response']
        metadata = quiz_payload['rag_data']['metadata']
        metadata['user_answer'] = user_response['answer']
        metadata['is_correct'] = user_response['is_correct']
        metadata['user_reasoning'] = user_response['reason']
        set_metadata = metadata
        update_stm_metadata(update_id, values, set_metadata)
    except Exception as e:
        error_message = f"An error with dialog manager: {str(e)}"
        raise DialogManagerError(error_message)
