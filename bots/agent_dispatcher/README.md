# procs-agent-dispatcher.md
* 可以将agent_dispatcher作为工程模板, 新的模块可以基于这个模板进行创建.

## start
```bash
$ python -m sagas.kit.rulesets_kit execute ./assets/rs_common_id.yml 'move_unable'
$ python -m sagas.kit.rulesets_kit execute ./assets/rs_tests_ja.yml describe_object

$ sagas ruleset 'Dia datang ke Shanghai untuk menjumpai adiknya.' purpose id True
$ sagas examples perception id True
$ sagas examples food en True
$ sagas examples injured en True

$ .env.sh
$ ses 'Este juego es facilísimo.'
```

+ dump additional info

```bash
$ honcho start
# 如果没有编译duckling, 可以使用docker版本, 并从Procfile中删除duckling的启动行,
# 在一个单独的控制台上执行以下命令:
# docker run -it -p 8000:8000 rasa/duckling
$ honcho start -f Procfile_mod
$ python -m cli.dispatcher_cli dump 'I was born in the summer of 1999.'
```

后台的action_dump_info会输出:

```
15:16:14 actions.1    | 2020-02-05 15:16:14 INFO     actions.actions  - [
15:16:14 actions.1    |   {
15:16:14 actions.1    |     "inspector": "ins_date",
15:16:14 actions.1    |     "provider": "duckling",
15:16:14 actions.1    |     "part": "obl",
15:16:14 actions.1    |     "value": [
15:16:14 actions.1    |       {
15:16:14 actions.1    |         "body": "summer of 1999",
15:16:14 actions.1    |         "start": 7,
15:16:14 actions.1    |         "value": {
15:16:14 actions.1    |           "values": [
15:16:14 actions.1    |             {
15:16:14 actions.1    |               "to": {
15:16:14 actions.1    |                 "value": "1999-09-24T00:00:00.000-07:00",
15:16:14 actions.1    |                 "grain": "day"
15:16:14 actions.1    |               },
15:16:14 actions.1    |               "from": {
15:16:14 actions.1    |                 "value": "1999-06-21T00:00:00.000-07:00",
15:16:14 actions.1    |                 "grain": "day"
15:16:14 actions.1    |               },
15:16:14 actions.1    |               "type": "interval"
15:16:14 actions.1    |             }
15:16:14 actions.1    |           ],
15:16:14 actions.1    |           "to": {
15:16:14 actions.1    |             "value": "1999-09-24T00:00:00.000-07:00",
15:16:14 actions.1    |             "grain": "day"
15:16:14 actions.1    |           },
15:16:14 actions.1    |           "from": {
15:16:14 actions.1    |             "value": "1999-06-21T00:00:00.000-07:00",
15:16:14 actions.1    |             "grain": "day"
15:16:14 actions.1    |           },
15:16:14 actions.1    |           "type": "interval"
15:16:14 actions.1    |         },
15:16:14 actions.1    |         "end": 21,
15:16:14 actions.1    |         "dim": "time",
15:16:14 actions.1    |         "latent": false
15:16:14 actions.1    |       }
15:16:14 actions.1    |     ],
15:16:14 actions.1    |     "delivery": "slot"
15:16:14 actions.1    |   }
15:16:14 actions.1    | ]
```

