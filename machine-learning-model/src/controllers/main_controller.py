from flask import request, Response, json, Blueprint
from ..services.short_term_memory_service import (save_to_short_term_memory, get_recent_conversation_history,
                                                  ShortTermMemoryError)
from ..services.long_term_memory_service import (fetch_from_domain_knowledge, KnowledgeFetchError)

from ..services.predict_context import (predict_context, InferenceError)

from ..services.dialog_manager import lets_talk

resources = Blueprint("cabot", __name__)


@resources.route('/user_convo', methods=["POST"])
def save_to_short_term_memory_controller():
    try:
        # Assuming raw_conversation_log is obtained from the POST request
        raw_conversation_log = request.json
        # Call the function to save to short-term memory
        save_to_short_term_memory(raw_conversation_log)

        # Return success response
        return Response(
            response=json.dumps({'status': "success"}),
            status=200,
            mimetype='application/json'
        )
    except ShortTermMemoryError as e:
        # Handle the custom exception and return an error response
        error_message = str(e)
        return Response(
            response=json.dumps({'status': "error", 'message': error_message}),
            status=500,  # Internal Server Error
            mimetype='application/json'
        )


@resources.route('/get_recent_conversations', methods=["POST"])
def get_recent_conversation_controller():
    try:
        raw_conversation = request.json
        result = get_recent_conversation_history(raw_conversation)
        if result is not None:
            return Response(
                response=json.dumps({'data': result, 'status': "success"}),
                status=200,
                mimetype='application/json'
            )
    except ShortTermMemoryError as e:
        error_message = str(e)
        return Response(
            response=json.dumps({'status': "error", 'message': error_message}),
            status=500,  # Internal Server Error
            mimetype='application/json'
        )


@resources.route('/get_domain_knowledge', methods=["POST"])
def fetch_from_domain_knowledge_controller():
    try:
        raw_conversation = request.json
        result = fetch_from_domain_knowledge(raw_conversation['user'])
        if result is not None:
            return Response(
                response=json.dumps({'data': result, 'status': "success"}),
                status=200,
                mimetype='application/json'
            )
    except KnowledgeFetchError as e:
        error_message = str(e)
        return Response(
            response=json.dumps({'status': "error", 'message': error_message}),
            status=500,  # Internal Server Error
            mimetype='application/json'
        )


@resources.route('/predict_context', methods=["POST"])
def predict_context_controller():
    try:
        raw_conversation = request.json
        result = predict_context(raw_conversation['user'])
        if result is not None:
            return Response(
                response=json.dumps({'data': result, 'status': "success"}),
                status=200,
                mimetype='application/json'
            )
    except InferenceError as e:
        error_message = str(e)
        return Response(
            response=json.dumps({'status': "error", 'message': error_message}),
            status=500,  # Internal Server Error
            mimetype='application/json'
        )


@resources.route('/lets_talk', methods=["POST"])
def lets_talk_controller():
    try:
        raw_conversation = request.json
        result = lets_talk(raw_conversation)
        print(result)
        if result is not None:
            return Response(
                response=json.dumps({'data': result, 'status': "success"}),
                status=200,
                mimetype='application/json'
            )
    except InferenceError as e:
        error_message = str(e)
        return Response(
            response=json.dumps({'status': "error", 'message': error_message}),
            status=500,  # Internal Server Error
            mimetype='application/json'
        )

