"""
Module init.
Contains function for starting up the flask process
"""

def runFlask(in_queue, out_queue):
    import logging
    logging.info("### STARTING API ###")
    werkzeugLogger = logging.getLogger("werkzeug")
    # suppresses logging of individual requests to endpoints. Prevents log spam
    werkzeugLogger.setLevel(logging.WARNING)
    import sys
    import api.routes
    from config import microlabConfig as config
    from api.app import app
    from microlab.interface import MicrolabInterface
    reload = False if len(sys.argv) > 1 and sys.argv[1] == 'production' else True

    api.routes.microlabInterface = MicrolabInterface(in_queue, out_queue)
    app.run(host='0.0.0.0', port=config.apiPort)
