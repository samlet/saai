import asyncio
import glob
from rasa.train import train_async
import rasa.utils.io as io_utils

from rasa.utils.endpoints import ClientResponseError, EndpointConfig
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.model import get_model, get_latest_model
from rasa.core.channels.channel import UserMessage

class BotsConf(object):
    def __init__(self, conf='/pi/ws/sagas-ai/conf/agents.json'):
        import json_utils
        self.endpoint = EndpointConfig("http://localhost:5055/webhook")
        self.conf=conf
        conf_data=json_utils.read_json_file(self.conf)
        # bot_locs={'genesis': '/pi/ws/sagas-ai/bots/genesis'}
        self.bot_locs = conf_data['bot_locs']
        self.templates_dir='/pi/ws/sagas-ai/templates'
        self.ruleset_files='/pi/stack/conf/ruleset_*.json'

def generate_domain_file(conf):
    cnt = io_utils.read_yaml_file(f'{conf.templates_dir}/domain.yml')
    intents = cnt['intents']
    actions = cnt['actions']
    for f in glob.glob(conf.ruleset_files):
        rules = io_utils.read_json_file(f)
        for rule in rules:
            intents.append({rule['intent']: {'triggers': rule['action']}})
            actions.append(rule['action'])
    return cnt

async def train_agent(bot, conf):
    cnt=generate_domain_file(conf)

    prefix = f"{conf.bot_locs[bot]}"
    # domain_file="./out/domain_1.yml"
    domain_file = f"{prefix}/domain.yml"
    io_utils.write_yaml_file(cnt, domain_file)
    await train_async(
        domain=domain_file,
        config=f"{prefix}/config.yml",
        training_files=f"{prefix}/data/",
        output_path=f"{prefix}/models/",
    )

agents={}
async def get_agent(bot, conf) -> Agent:
    if bot not in agents:
        # train it
        await train_agent(bot, conf)
        # load it
        bot_loc = get_latest_model(f"{conf.bot_locs[bot]}/models")
        print(f'.. load bot model {bot_loc}')
        agent = Agent.load(bot_loc, action_endpoint=conf.endpoint)
        agents[bot]=agent
    return agents[bot]

async def handle_message(mod, text, sender, conf):
    agent=await get_agent(mod, conf)
    message = UserMessage(text, sender_id=sender)
    return await agent.handle_message(message)

class AgentProcs(object):
    def tests(self, bot='genesis'):
        """
        $ python -m saai.agent_procs tests
        :param bot:
        :return:
        """
        text = '/behave_purpose{"object_type": "restaurant"}'
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(handle_message(bot, text, sender='default', conf=BotsConf()))

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(AgentProcs)


