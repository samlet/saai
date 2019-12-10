# procs-saya.md
## start
```sh
rasa train
start actions

# invoke action: 'action_hello_world'
rasa shell
> /behave_hi{"hotel":{"name":"test"}} 
> /behave_hi{"hotel":{"name":"test", "ft":[1,2]}} 
```

