# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した3番目のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 主なディレクトリの説明

<br>

# 1.　プロジェクトについて

3番目のポートフォリオとして、ローカル環境でLLMを動かせる[llama.cpp](https://github.com/ggerganov/llama.cpp)のPythonバインディングライブラリである[llama-cpp-python](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file)と、LLMが参照するデータを拡張するフレームワークである[LlamaIndex](https://github.com/run-llama/llama_index?tab=readme-ov-file)を使ったプログラムを作成しました。気軽に手元のノートPCのCPUで動かすLLMプログラムということで、プロジェクト名は「local_llm_for_cpu」としました。 

このプロジェクトを始めた理由は、生成AIが日常生活でも広く使われて身近な存在になってきていることや、そもそもPythonを学んだ理由の一つが、機械学習やAIといった分野に関心があり、いずれ取り組んでみたいと考えていたからです。そして何より、生成AIは高性能なGPUが必要であり、クラウド環境を使うとしてもある程度のコストがかかると考えていましたが、llama-cpp-pythonの存在を知ったことで、ローカルで気軽に色々と試しながら作業ができると思えたことが大きかったです。  

LLMのコンテキスト拡張ができるLlamaIndexを組み込んだのは、最初は2番目のポートフォリオである[e-lection](https://github.com/ryskkkkw/e-lection)に、投票機能だけでなくユーザーの政治に関する疑問などに答える機能を加えたいと考えたからです。LLMだけでは、持っているデータがそのモデルをトレーニングした時点のものに限られ、最新の情報を踏まえたQ&Aが実行できないことや、特定分野の詳細な情報を求められたときに対応が難しいため、LLMが推論を行う際にLlamaIndexで政治に関する資料データを与えることで、政治関係のドメインに特化した生成AIによるQ&A機能を実装することが目的でした。  

しかし、[e-lection](https://github.com/ryskkkkw/e-lection)のREADME「1.プロジェクトについて」に書いたとおり、CPUで動かすLLMのQ&Aは実行に多くの時間を要するので、最終的にはe-lectionには組み込まずに別のプロジェクトとして、llama-cpp-pythonとLlamaIndexを組み合わせたローカルで動くLLMプログラム「「local_llm_for_cpu」」という形にしました。  
結果的に別のプロジェクトとなりましたが、ローカル環境で動かすこと、任意のデータを与えて特定分野の質問にも答えられるようにすることという機能面での目的は一定程度達成できました。
<br>

# 2.ディレクトリ構成

プロジェクトディレクトリの主な構成は以下のとおりです。

    local_llm_for_cpu
    ├── config
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   └── production.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── llm_resources
    │   ├── documents
    │   ├── index_storage
    │   └── llm_models
    ├── local_llm
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── test-llm-model.gguf
    │   ├── test_document1.pdf
    │   ├── test_document2.pdf
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    ├── static
    │   └── style.css
    └── templates
        ├── base.html
        ├── document_and_query.html
        ├── document_register.html
        ├── embed_register.html
        ├── index.html
        ├── llm_and_embed.html
        ├── llm_register.html
        └── response.html
