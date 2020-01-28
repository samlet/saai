from sanic import Sanic

from .nlu_mod import info

app = Sanic(__name__)
app.blueprint(info)


class NluDispatcher(object):
    def run(self, port=1700, debug=True):
        """
        $ python -m servants.nlu_dispatcher run 1702 False
        $ rasa run --enable-api

        see also: procs-nlu-integration.ipynb
        """
        app.run(host='0.0.0.0', port=1702, debug=debug)


if __name__ == '__main__':
    import fire

    fire.Fire(NluDispatcher)

