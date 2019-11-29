## start
```bash
$ . env.sh 
$ python -m procs_tests test_df
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

