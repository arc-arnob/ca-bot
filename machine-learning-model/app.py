from src import config, app
from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
    # http_server = WSGIServer((config.HOST, config.PORT), app)
    # http_server.spawn = 4
    # http_server.serve_forever()