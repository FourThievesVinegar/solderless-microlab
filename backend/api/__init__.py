"""
Module init.
Contains function for starting up the flask process
"""

def runFlask(in_queue, out_queue):
    import sys
    import api.routes
    from config import microlabConfig as config
    from api.app import app
    from microlab.interface import MicrolabInterface
    reload = False if len(sys.argv) > 1 and sys.argv[1] == 'production' else True

    api.routes.microlabInterface = MicrolabInterface(in_queue, out_queue)
    app.run(host='0.0.0.0', port=config.apiPort)
