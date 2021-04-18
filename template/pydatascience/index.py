
# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request
from flask_basicauth import BasicAuth

from function import handler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

with open('/var/openfaas/secrets/fn-basic-auth-username') as f:
    app.config['BASIC_AUTH_USERNAME'] = f.read().splitlines()[0]
f.closed

with open('/var/openfaas/secrets/fn-basic-auth-password') as f:
    app.config['BASIC_AUTH_PASSWORD'] = f.read().splitlines()[0]
f.closed

basic_auth = BasicAuth(app)


@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True


@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
@basic_auth.required
def main_route(path):
    ret = handler.handle(request.get_data())
    return ret


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
