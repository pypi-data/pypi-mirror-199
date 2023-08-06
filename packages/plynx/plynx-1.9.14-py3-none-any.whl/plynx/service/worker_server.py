"""The serving logic of the worker"""
import logging
import os

from flask import Flask
from flask.logging import create_logger
from flask_cors import CORS

from plynx.utils.db_connector import check_connection
from plynx.utils.logs import set_logging_level

app = Flask(__name__)
logger = create_logger(app)


@app.route("/")
def hello_world():
    """Hello world"""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


def run_worker_server(verbose, port, debug):
    """Run worker service"""

    # set up logger level
    set_logging_level(verbose, logger=logger)
    set_logging_level(verbose, logger=logging.getLogger('werkzeug'))

    check_connection()

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=False,
        threaded=True,
    )
