from ..services.short_term_memory_service import save_to_short_term_memory, get_recent_conversation_history
from ..services.long_term_memory_service import fetch_from_domain_knowledge
from ..services.predict_context import predict_context, ask_llm


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
    augmented_prompt="Using given dialogs reply"
    prompt = knowledge + " " + augmented_prompt + " " + user_conversation['USER']
    generated_dialog = ask_llm(prompt)
    return {
        "prompt": prompt,
        "generated_text": generated_dialog
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
