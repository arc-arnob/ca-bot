from flask import request, Response, json, Blueprint

resources = Blueprint("cabot", __name__)


@resources.route('/user_convo', methods=["GET"])
def save_to_short_term_memory():
    print("This RAN!!!")
    return Response(
        response=json.dumps({'status': "success"}),
        status=200,
        mimetype='application/json'
    )
