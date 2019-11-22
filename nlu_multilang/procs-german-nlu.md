# procs.md
⊕ [Language Support](https://rasa.com/docs/nlu/0.13.8/languages/)
⊕ [服务器配置](https://rasa.com/docs/nlu/0.13.8/config/#section-configuration)
⊕ [Choosing a Rasa NLU Pipeline](https://rasa.com/docs/nlu/0.13.8/choosing_pipeline/#choosing-pipeline)

## start
```sh
# create configure files: config.yml, nlu_data/nlu_data.md

# train
./train.sh
# start nlu server
./nlu-server.sh
# execute a intent query
./query.sh 
# or via curl
$ curl -XPOST localhost:5000/parse -d '{"q":"Shenzhen ist das Silicon Valley für Hardware-Firmen", "project":"german"}'
```
+ 结果如下:

```json
{
  "intent": {
    "name": "tech",
    "confidence": 0.9565718770027161
  },
  "entities": [
    {
      "entity": "LOC",
      "value": "Silicon Valley",
      "start": 17,
      "confidence": null,
      "end": 31,
      "extractor": "ner_spacy"
    }
  ],
  "intent_ranking": [
    {
      "name": "tech",
      "confidence": 0.9565718770027161
    },
    {
      "name": "farvel",
      "confidence": 0.0
    },
    {
      "name": "hallo",
      "confidence": 0.0
    }
  ],
  "text": "Shenzhen ist das Silicon Valley für Hardware-Firmen",
  "project": "german",
  "model": "model_20190104-024340"
}
```


