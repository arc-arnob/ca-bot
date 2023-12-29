from flask import request, Response, json, Blueprint
import time
from ..services.short_term_memory_service import (save_to_short_term_memory, get_recent_conversation_history,
                                                  ShortTermMemoryError)

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
        matches = result.json()
        print(matches)
        return Response(
            response=json.dumps({'data': matches, 'status': "success"}),
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