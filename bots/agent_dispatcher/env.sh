#!/bin/bash
#honcho="$HOME/miniconda3/envs/bigdata/bin/honcho"
honcho='foreman'  # forman support .env file
alias s1="$honcho start"
# alias s2='foreman start -f Procfile_langs'
alias s2="$honcho start -f Procfile_langs"
# alias s3="$honcho start -f Procfile_api"
alias s3="python -m sagas.api.info_stack run 1700 False"
alias s4="python -m sagas.api.info_stack run 1700 True"

alias tool='python -m sagas.ofbiz.tools'
## import-data ./data/product/
alias import-data='python -m sagas.ofbiz.tools import_dir'
alias clip='python -m sagas.ofbiz.tools convert_minilang_from_clip'
alias clip_vars='python -m sagas.ofbiz.tools clip_vars'

alias gen_model='python -m sagas.ofbiz.gen_tool gen-model-cls'
alias gen_dss='python -m sagas.ofbiz.gen_tool gen-dss-model'
alias gen_pkg='python -m sagas.ofbiz.entity_gen gen_package'
alias gen_json='python -m sagas.ofbiz.entity_gen gen_jsonifier'
alias action='python -m sagas.bots.action_gen common '
alias execute='python -m sagas.bots.action_runner execute '

alias sgen='python -m sagas.ofbiz.gen_section gen'

alias prefab='python -m sagas.ofbiz.entity_prefabs persist_component'

## view entity model: tool entity_model <model_name>
## tool entity_data DssOrdinalSales

alias rabbit='docker exec -it rabbit_ws_rabbit_1 bash'

# alias lookup='python -m sagas.ofbiz.resources lookup'
alias lookup='python -m sagas.ru.ru_procs lookup'
alias ips='python -m sagas.ru.ru_procs ips'

# python -m sagas.ofbiz.resource_indexer search 产品价格
alias search='python -m sagas.ofbiz.resource_indexer search'
alias cn='python -m sagas.bots.hanlp_procs tree'

alias parse='python -m sagas.nlu.corenlp_helper parse'
alias nlu='python -m sagas.nlu.nlu_tools '
alias nluc='python -m sagas.nlu.nlu_tools clip_parse'

alias odoo_info='python -m sagas.crmsfa.odoo_info '

## refs
# alias ja='python -m sagas.train.parallel_corpus refs_shortcut ja'
# alias zh='python -m sagas.train.parallel_corpus refs_shortcut zh'
# alias fr='python -m sagas.train.parallel_corpus refs_shortcut fr'
# alias ru='python -m sagas.train.parallel_corpus refs_shortcut ru'

alias ko='python -m sagas.ko.korea_processor analyse'
# $ ka I ask you for an answer.
alias ka='python -m sagas.ar.arabic_processor ka'

alias say-ru='python -m sagas.nlu.nlu_tools say_with ru'
alias say-zh='python -m sagas.nlu.nlu_tools say_with zh'
alias say-ja='python -m sagas.nlu.nlu_tools say_with ja'
alias say-fr='python -m sagas.nlu.nlu_tools say_with fr'
alias say-en='python -m sagas.nlu.nlu_tools say_with en'
alias say-ko='python -m sagas.nlu.nlu_tools say_with ko'
alias say-ar='python -m sagas.nlu.nlu_tools say_with ar'
alias say-hi='python -m sagas.nlu.nlu_tools say_with hi'
alias say-id='python -m sagas.nlu.nlu_tools say_with id'

alias about='python -m sagas.ru.ru_procs about'
# alias build-ru='python -m sagas.ru.ru_procs build_words_map'
alias build-ru='python -m sagas.ru.ru_procs build_inputs'

alias plain='python -m sagas.tool.misc plain'
alias wrap='python -m sagas.tool.misc wrap_sent'
alias sb='python -m sagas.tool.misc plain'
alias sbb='python -m sagas.tool.misc plain_sents'
alias trans='python -m sagas.tool.misc trans_clip'
alias trans-ru="python -m sagas.tool.misc trans_clip ru 'en;zh-CN;ja' ja"
# alias trans-ru="python -m sagas.tool.misc trans_clip ru 'en;zh-CN;ja' en"
# read with english
# alias sr="python -m sagas.tool.misc trans_clip ru 'en;zh-CN;ja' en"
alias sr="python -m sagas.tool.misc trans_clip ru 'en;zh-CN;ja' ja False"
alias sr-d="python -m sagas.tool.misc trans_clip ru 'en;zh-CN;ja' ja True"
# add ukrainian
# alias sr="python -m sagas.tool.misc trans_clip ru 'en;uk;zh-CN;ja' ja"
# alias sp="python -m sagas.tool.misc trans_clip pt 'en;it;ja' ja False"
alias sp="python -m sagas.tool.misc trans_clip pt 'en;es;ja' ja False"
alias spt="python -m sagas.tool.misc trans_clip pt 'en;zh;ja' ja False"
alias si="python -m sagas.tool.misc trans_clip it 'en;pt;ja' ja False"
alias sit="python -m sagas.tool.misc trans_clip it 'en;zh;ja' ja False"
# alias sf="python -m sagas.tool.misc trans_clip fr 'es;pt;zh-CN;ja' ja"
alias sf="python -m sagas.tool.misc trans_clip fr 'en;zh-CN;ja' ja False"

alias sd-detail="python -m sagas.tool.misc trans_clip de 'en;zh-CN;ja' ja True"
# alias sd-f="python -m sagas.tool.misc trans_clip de 'en;fr;es;ru;zh-CN;ko;ja' ja False"
alias sd+etc="python -m sagas.tool.misc trans_clip de 'en;fr;es;pt;ru;zh-CN;ja' ja False"
alias sd="python -m sagas.tool.misc trans_clip de 'en;zh-CN;ja' ja False"
alias sd+nl="python -m sagas.tool.misc trans_clip de 'en;nl;zh-CN;ja' ja False"
alias sd+ru="python -m sagas.tool.misc trans_clip de 'en;ja;ru' ru"
alias sd+fr="python -m sagas.tool.misc trans_clip de 'en;ja;fr' fr"
# alias sd="python -m sagas.tool.misc trans_clip de 'en;ja;ru' ru"

alias bd='python -m sagas.tool.misc trans_clip_opt de'
alias be='python -m sagas.tool.misc trans_clip_opt en'
alias bj='python -m sagas.tool.misc trans_clip_opt ja'

# alias scs="python -m sagas.tool.misc trans_clip cs 'en;zh-CN;ja' ja False"
alias scs-ru="python -m sagas.tool.misc trans_clip cs 'en;ja;ru' ru False"
alias scs="python -m sagas.tool.misc trans_clip cs 'en;sk;ru' ru False"
alias scs+pl="python -m sagas.tool.misc trans_clip cs 'en;pl;ru' ru False"
alias scs+bg="python -m sagas.tool.misc trans_clip cs 'en;bg;ru' ru False"

alias spl="python -m sagas.tool.misc trans_clip pl 'en;cs;ru' ru False"

# alias se="python -m sagas.tool.misc trans_clip en 'fr;zh-CN;ja' ja False"
alias se="python -m sagas.tool.misc trans_clip en 'fr;zh-CN;ja' en False"
alias se-ar="python -m sagas.tool.misc trans_clip en 'fr;zh-CN;ar' ar False"
alias se-hi="python -m sagas.tool.misc trans_clip en 'fr;zh-CN;hi' hi False"
alias se-ko="python -m sagas.tool.misc trans_clip en 'fr;zh-CN;ko' ko False"

# alias ses="python -m sagas.tool.misc trans_clip es 'en;zh-CN;ja' ja False"
alias ses="python -m sagas.tool.misc trans_clip es 'en;zh-CN;ja' en False"
alias she="python -m sagas.tool.misc trans_clip he 'en;zh;ja' ja False"
alias saf="python -m sagas.tool.misc trans_clip af 'en;zh;ja' ja False"
# Indonesian
alias sidj="python -m sagas.tool.misc trans_clip id 'en;zh-CN;ja' ja False"
alias sid="python -m sagas.tool.misc trans_clip id 'en;zh-CN;ja' en False"
# alias sid+="python -m sagas.tool.misc trans_clip id 'en;zh-CN;ja' id False"

# Irish
alias sga="python -m sagas.tool.misc trans_clip ga 'en;zh-CN;ja' ja False"
# Welsh
alias scy="python -m sagas.tool.misc trans_clip cy 'en;zh-CN;ja' ja False"
# Hungarian (匈牙利语)
alias shu="python -m sagas.tool.misc trans_clip hu 'en;zh-CN;ja' ja False"

alias sa="python -m sagas.tool.misc trans_clip ar 'en;zh-CN;ja' ja False"
alias sfa="python -m sagas.tool.misc trans_clip fa 'en;zh-CN;ja' ja False"
# alias sj="engine=knp python -m sagas.tool.misc trans_clip ja 'en;zh-CN;fr' ja False"
alias sj="python -m sagas.tool.misc trans_clip ja 'en;zh-CN;fr' ja False"
alias sja="engine=corenlp python -m sagas.tool.misc trans_clip ja 'en;zh-CN;fr' ja False"

alias st="python -m sagas.tool.misc trans_clip tr 'en;zh-CN;ja' ja False"
alias sz="python -m sagas.tool.misc trans_clip zh 'en;fr;ja' ja False"
alias sv="python -m sagas.tool.misc trans_clip sv 'en;no;ja' ja False"
alias sv-de="python -m sagas.tool.misc trans_clip sv 'en;no;de' de False"
# alias sv-de="python -m sagas.tool.misc trans_clip sv 'en;ja;de' de False"

alias svi="python -m sagas.tool.misc trans_clip vi 'en;zh-CN;ja' ja False"
alias suk="python -m sagas.tool.misc trans_clip uk 'en;zh-CN;ja' ja False"

# alias sda="python -m sagas.tool.misc trans_clip da 'en;ja;de' de False"
alias sda="python -m sagas.tool.misc trans_clip da 'en;no;de' de False"
alias sda+sv="python -m sagas.tool.misc trans_clip da 'en;sv;de' de False"
alias snl+cj="python -m sagas.tool.misc trans_clip nl 'en;zh;ja' ja False"
alias snl="python -m sagas.tool.misc trans_clip nl 'en;zh;ja' ja False"

# Norwegian
alias sno="python -m sagas.tool.misc trans_clip no 'en;ja;de' de False"
alias ssv="python -m sagas.tool.misc trans_clip sv 'en;ja;de' de False"
alias snl+de="python -m sagas.tool.misc trans_clip nl 'en;ja;de' de False"

alias shi="python -m sagas.tool.misc trans_clip hi 'zh-CN;ur;en' hi False"

alias sel="python -m sagas.tool.misc trans_clip el 'en;zh-CN;ja' ja False"
alias sca="python -m sagas.tool.misc trans_clip ca 'en;es;ja' ja False"
alias sko="python -m sagas.tool.misc trans_clip ko 'en;zh-CN;ja' ja False"
alias sfi="python -m sagas.tool.misc trans_clip fi 'en;zh-CN;ja' ja False"

# 
alias ta='python -m sagas.tool.misc trans_en_ar'
alias tk='python -m sagas.tool.misc trans_en_ko'
alias tf='python -m sagas.tool.misc trans_en_fa'
alias th='python -m sagas.tool.misc trans_en_hi'
alias the='python -m sagas.tool.misc trans_en_he'
alias tfi='python -m sagas.tool.misc trans_en_fi'
alias tpt='python -m sagas.tool.misc trans_en_pt'

alias trans-rus="python -m sagas.tool.misc trans_clip ru 'en;es;fr;de;zh-CN;ja'"
alias trans-de="python -m sagas.tool.misc trans_clip de 'en;zh-CN;ja' ja"
alias trans-des="python -m sagas.tool.misc trans_clip de 'en;es;fr;ru;zh-CN;ja'"
alias trans-fr="python -m sagas.tool.misc trans_clip fr 'en;zh-CN;ja' en"
alias trans-frs="python -m sagas.tool.misc trans_clip fr 'en;es;de;ru;zh-CN;ja'"

alias trans-ko="python -m sagas.tool.misc trans_clip en 'zh-CN;ja;ko' ko"
# alias sk="python -m sagas.tool.misc trans_clip en 'zh-CN;ja;ko' ko"
# alias sk="python -m sagas.tool.misc trans_clip de 'en;zh-CN;ja;ko' ko"
alias to-zh="python -m sagas.nlu.google_translator translate"
alias ltp='python -m sagas.zh.ltp_procs analyse'

alias all_sources='python -m sagas.nlu.trans_cacher all_sources'
alias sn='python -m sagas.tool.misc add_serial_no'
alias all_langs='python -m sagas.nlu.wordnet_procs all_langs'

# $ word juego es
alias word='python -m sagas.nlu.wordnet_procs word_sets'
alias wordnet='python -m sagas.nlu.wordnet_procs'
# 在终端上输出单词的定义和继承链
alias def='python -m sagas.nlu.nlu_cli get_word_def'

# $ hyper game.n.03
alias hyper='python -m sagas.nlu.wordnet_procs desc_hyper'

# 输出继承链以及在不同语言的词根表示
alias expl='python -m sagas.nlu.nlu_cli explore'

# dep-parse: $ domains 'Ivan is the best dancer .' en spacy
alias domains='python -m sagas.tool.misc verb_domains'
alias rules='python -m sagas.tool.misc exec_rules'
alias ascviz='python -m sagas.nlu.nlu_cli ascii_viz'

# translit
alias tra='python -m sagas.nlu.transliterations trans_polyglot_from_clip '
# search corpus: search 'I read a letter.' ja,id
alias search='python -m sagas.corpus.searcher run '
alias tr-ar='python -m sagas.nlu.translit_ar translit True'
alias search_id='python -m sagas.corpus.index_trainer search_id'

# odoo
alias open_products='open http://localhost:8069/web#action=283&model=product.template&view_type=kanban&menu_id=168'

## 
alias verbs='python -m sagas.nlu.ruleset_procs verbs'

## docker execs
# agents saai.saai_cli nlu_reload en
# agents saai.saai_cli bot_reload genesis
alias agents='docker exec -it sagas_agent_servant_1 python -m'

