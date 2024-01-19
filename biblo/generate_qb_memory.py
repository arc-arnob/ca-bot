import json
import random
import requests
from read_json_config import read_json

BASE_URL = "http://127.0.0.1:3000/api/v1"
"""
{
"Q1":{"question":"",
"options":["","","",""],
"answered_before":True/False,
"correct_answer":"",

"given_answer":""
"is_correct":True/False,
"context":"quiz"
}
}

"""

def make_api_call(route, method, data):
    url = f"{BASE_URL}/{route}"

    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError("Invalid HTTP method")
    return response.json()["data"]


def generate_qb_topic(user_id, topic="BODMAS"):
    #fetch from RAG
    route = "get_domain_knowledge"
    payload = {"user":f"Ask me questions about {topic}", "user_id":user_id}
    question_bank = make_api_call(route, "POST", payload)
    no_of_questions = read_json("TOTAL_QUESTIONS")
    print(question_bank)
    
    previous_questions = []
    prev_incorrect_questions = []
    new_questions = []

    for question in question_bank:
        if "is_correct" in question and question["topic"] == topic:
            previous_questions.append(question)
            if not question["is_correct"]:
                prev_incorrect_questions.append(question)
        else:
            new_questions.append(question)

    if len(new_questions) >= (no_of_questions - len(previous_questions)):
        ask_questions = random.sample(new_questions, no_of_questions - len(prev_incorrect_questions))
    else:
        ask_questions = new_questions
    ask_questions.extend(prev_incorrect_questions)

    return ask_questions

if __name__ == "__main__":
    # generate_qb_topic(1, "profit and loss")
    generate_qb_topic(1, "algebra")

