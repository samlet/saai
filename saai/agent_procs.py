from typing import List, Dict, Any, Optional, Text

import asyncio
import glob
from rasa.train import train_async
import rasa.utils.io as io_utils
import logging

from rasa.utils.endpoints import ClientResponseError, EndpointConfig
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.model import get_model, get_latest_model
from rasa.core.channels.channel import UserMessage

logger = logging.getLogger(__name__)

class BotsConf(object):
    def __init__(self, conf='agents.json'):
        # import json_utils
        from python_json_config import ConfigBuilder
        from saai.saai_conf import saai_conf

        # self.endpoint = EndpointConfig("http://localhost:5055/webhook")
        self.conf=f"{saai_conf.runtime_dir}/conf/{conf}"
        # conf_data=json_utils.read_json_file(self.conf)
        builder = ConfigBuilder()
        self.config = builder.parse_config(self.conf)
        # bot_locs={'genesis': '/pi/ws/sagas-ai/bots/genesis'}
        # self.bot_locs = conf_data['bot_locs']
        # self.config_file=conf_data['config_file']

        self.templates_dir=f'{saai_conf.runtime_dir}/templates'
        self.ruleset_files='/pi/stack/conf/ruleset_*.json'

    def get_loc(self, bot:Text):
        return self.config.get(bot).location

    def get_config(self, bot:Text):
        return self.config.get(bot).config_file

    def get_endpoint(self, bot:Text):
        from sagas.conf.runtime import runtime
        bot_endpoint=f"{bot}_actions" if runtime.is_docker() else 'localhost'
        return EndpointConfig(f"http://{bot_endpoint}:5055/webhook")

def generate_domain_file(conf:BotsConf):
    cnt = io_utils.read_yaml_file(f'{conf.templates_dir}/domain.yml')
    intents = cnt['intents']
    actions = cnt['actions']
    for f in glob.glob(conf.ruleset_files):
        rules = io_utils.read_json_file(f)
        for rule in rules:
            intents.append({rule['intent']: {'triggers': rule['action']}})
            actions.append(rule['action'])
    return cnt

async def train_agent(bot:Text, conf:BotsConf):
    cnt=generate_domain_file(conf)

    prefix = f"{conf.get_loc(bot)}"
    # domain_file="./out/domain_1.yml"
    domain_file = f"{prefix}/domain.yml"
    io_utils.write_yaml_file(cnt, domain_file)
    await train_async(
        domain=domain_file,
        config=f"{prefix}/{conf.get_config(bot)}",
        training_files=f"{prefix}/data/",
        output_path=f"{prefix}/models/",
    )

async def load_agent(bot:Text, conf:BotsConf) -> Agent:
    # train it
    await train_agent(bot, conf)
    # load it
    bot_loc = get_latest_model(f"{conf.get_loc(bot)}/models")
    print(f'.. load bot model {bot_loc}')
    agent = Agent.load(bot_loc, action_endpoint=conf.get_endpoint(bot))
    return agent

agents={}
async def get_agent(bot:Text, conf:BotsConf, force=False) -> Agent:
    if force or (bot not in agents):
        agents[bot]=await load_agent(bot, conf)
    return agents[bot]

async def handle_message(mod, text, sender, conf:BotsConf):
    agent=await get_agent(mod, conf)
    message = UserMessage(text, sender_id=sender)
    return await agent.handle_message(message)

class AgentProcs(object):
    def env(self):
        """
        $ python -m saai.agent_procs env
        :return:
        """
        conf=BotsConf()
        print(conf.get_endpoint('genesis').url)
        print(conf.get_loc('genesis'))
        print(conf.get_config('genesis'))

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


