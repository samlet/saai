## start
```bash
$ . env.sh 
$ python -m procs_tests test_df
```

## nlu train & run
```sh
# for ja
$ start train_ja
$ start nlu ja
$ start query_ja
# or
$ curl localhost:2000/model/parse -d '{"text":"卵を食べる"}' | json

# for zh
$ start train_zh
$ start nlu zh
$ curl localhost:2000/model/parse -d '{"text":"几台电脑"}' | json
```


