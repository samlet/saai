## start
```bash
$ . env.sh 
$ python -m procs_tests test_df

# run agents servant
$ honcho start
# or
$ s1
```

## nlu train & run
```sh
# for ja
$ start train_ja
$ start nlu ja 2000
$ start query_ja
# or
$ curl localhost:2000/model/parse -d '{"text":"卵を食べる"}' | json

# for zh
$ start train_zh
$ start nlu zh 2000
$ curl localhost:2000/model/parse -d '{"text":"几台电脑"}' | json

# for en
$ start train en
$ start nlu en 2001
$ curl localhost:2001/model/parse -d '{"text":"can i get french food"}' | json
```

+ run manager

■ nlu_multilang的启动管理器:
    + sagas-ai/saai/runner.py

```sh
$(server) python -m saai.runner exec_spec zh,en,ja
$ python -m saai.runner invoke "几台电脑" zh
$ python -m saai.runner invoke "卵を食べる" ja
$ python -m saai.runner invoke "can i get french food" en
$ python -m saai.runner invoke "Shenzhen ist das Silicon Valley für Hardware-Firmen" de
```

## sagas servants
■ agent servant:
    $ start actions
    + sagas-ai/saai/agent_procs.py
        $ python -m saai.agent_procs tests
    + sagas-ai/saai/agent_servant.py
        $ python -m saai.agent_servant
    + procs-agent-cli.ipynb
    $ python -m saai.saai_cli bot_message

+ conf: sagas-ai/conf/agents.json

## saya individuals
```sh
# nlu/nlg/actions/agent均独立运行, see: Procfile_intp
# nlu/nlg是语言相关的组件, actions/agent是语言无关的组件
$ alias saya="$honcho start -f Procfile_intp"
$ saya
# cd bots/saya ; $rasa shell --endpoints endpoints.yml
$ start saya
```




