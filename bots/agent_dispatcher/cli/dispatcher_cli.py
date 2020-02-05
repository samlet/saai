import requests
from pprint import pprint
def talk(sents, sender='default', port=5005):
    response = requests.post(f'http://localhost:{port}/webhooks/rest/webhook',
                             json={'message': sents, 'sender':sender})
    print('status code:', response.status_code)
    pprint(response.json())

class DispatcherCli(object):
    def dump(self, sents):
        """
        $ python -m cli.dispatcher_cli dump 'I was born in the summer of 1999.'
        :param sents:
        :return:
        """
        # talk('I was born in the summer of 1999.')
        talk(sents)

if __name__ == '__main__':
    import fire
    fire.Fire(DispatcherCli)

