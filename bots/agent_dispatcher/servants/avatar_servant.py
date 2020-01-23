from sanic import Sanic

from .avatar_blueprints import info

app = Sanic(__name__)
app.blueprint(info)


class InfoStack(object):
    def run(self, port=1700, debug=True):
        """
        $ python -m servants.avatar_servant run 1701 False
        $ curl localhost:1701/info/ping
        $ curl -s -d '{"sents":"you took sixty damage"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1701/info/event/en | json
        $ curl -s -d '{"sents":"you are dead"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1701/info/event/en | json
        """
        app.run(host='0.0.0.0', port=1701, debug=debug)


if __name__ == '__main__':
    import fire

    fire.Fire(InfoStack)

