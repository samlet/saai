import asyncio
import glob
from rasa.train import train_async
import rasa.utils.io as io_utils

from rasa.utils.endpoints import ClientResponseError, EndpointConfig
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.model import get_model, get_latest_model
from rasa.core.channels.channel import UserMessage

endpoint = EndpointConfig("http://localhost:5055/webhook")
bot_locs={'genesis': '/pi/ws/sagas-ai/bots/genesis'}
templates_dir='/pi/ws/sagas-ai/templates'

def generate_domain_file():
    cnt = io_utils.read_yaml_file(f'{templates_dir}/domain.yml')
    intents = cnt['intents']
    actions = cnt['actions']
    for f in glob.glob('/pi/stack/conf/ruleset_*.json'):
        rules = io_utils.read_json_file(f)
        for rule in rules:
            intents.append({rule['intent']: {'triggers': rule['action']}})
            actions.append(rule['action'])
    return cnt

async def train_agent(bot):
    cnt=generate_domain_file()

    prefix = f"{bot_locs[bot]}"
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
async def get_agent(bot) -> Agent:
    if bot not in agents:
        # train it
        await train_agent(bot)
        # load it
        bot_loc = get_latest_model(f"{bot_locs[bot]}/models")
        print(f'.. load bot model {bot_loc}')
        agent = Agent.load(bot_loc, action_endpoint=endpoint)
        agents[bot]=agent
    return agents[bot]

async def handle_message(mod, text, sender):
    agent=await get_agent(mod)
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
        return loop.run_until_complete(handle_message(bot, text, sender='default'))

if __name__ == '__main__':
    import fire
    fire.Fire(AgentProcs)


