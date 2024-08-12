# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した3番目のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 主なディレクトリの説明

<br>

# 1.　プロジェクトについて

3つ目のポートフォリオとして、ローカル環境でLLMを動かせる[llama.cpp](https://github.com/ggerganov/llama.cpp)のPythonバインディングライブラリである[llama-cpp-python](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file)と、LLMが参照するデータを拡張するフレームワークである[LlamaIndex](https://github.com/run-llama/llama_index?tab=readme-ov-file)を使ったプログラムを作成しました。気軽に手元のノートPCのCPUで動かすLLMプログラムということで、プロジェクト名は「local_llm_for_cpu」としました。 

このプロジェクトを始めた理由は、生成AIが日常生活でも広く使われて身近な存在になってきていることや、そもそもPythonを学んだ理由の一つが、機械学習やAIといった分野に関心があり、いずれ取り組んでみたいと考えていたからです。そして何より、生成AIは高性能なGPUが必要であり、クラウド環境を使うとしてもある程度のコストがかかると考えていましたが、llama-cpp-pythonの存在を知ったことで、ローカルで気軽に色々と試しながら作業ができると思えたことが大きかったです。  

LLMのコンテキスト拡張ができるLlamaIndexを組み込んだのは、最初は2番目のポートフォリオである[e-lection](https://github.com/ryskkkkw/e-lection)に、投票機能だけでなくユーザーの政治に関する疑問などに答える機能を加えたいと考えたからです。LLMだけでは、持っているデータがそのモデルをトレーニングした時点のものに限られ、最新の情報を踏まえたQ&Aが実行できないことや、特定分野の詳細な情報を求められたときに対応が難しいため、LLMが推論を行う際にLlamaIndexで政治に関する資料データを与えることで、政治関係のドメインに特化した生成AIによるQ&A機能を実装することが目的でした。  

しかし、[e-lection](https://github.com/ryskkkkw/e-lection)のREADME「1.プロジェクトについて」に書いたとおり、CPUで動かすLLMのQ&Aは実行に多くの時間を要するので、最終的にはe-lectionには組み込まずに別のプロジェクトとして、llama-cpp-pythonとLlamaIndexを組み合わせたローカルで動くLLMプログラム「local_llm_for_cpu」という形にしました。  
結果的に別のプロジェクトとなりましたが、ローカル環境で動かすこと、任意のデータを与えて特定分野の質問にも答えられるようにすることという機能面での目的は一定程度達成できました。  

なお、これまでのプロジェクトと違い、このプロジェクトはLLMがメインのアプリケーションであり、CPUで実行するためパフォーマンスも十分ではないのでデプロイはしていませんが、Python,Djangoを学んだことのアウトプットというのがポートフォリオとしては本来の目的であるため、Djangoのフレームワークに組み込む形で実装しています。
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

# 3.主なディレクトリの説明

local_llmがこのプロジェクトで唯一のアプリケーションなので、その中で主なところを説明します。

- モデルはLlmModel、EmbedModel、Documentの３つを実装しています。
- LlmModelはアプリケーションで使用するLLM用のファイルフィールド持つモデルです。
- EmbedModelはLLMが参照するデータを拡張するファイルやユーザーの質問を、ベクトル化する際に使うEmbeddingモデルを指定するための文字列フィールドを持つモデルです。
- DocumentはLLMの参照データを拡張するファイル用のファイルフィールド、ファイル名の文字列フィールドを持ちます。また、DocumentはEmbedModelオブジェクトと多対一関係になっています。
<br>

- コンテキスト拡張したLLMのQ&Aを実行するためには、使用するLLM、Embeddingモデル、documentファイルを事前に登録する必要があります（それぞれ複数登録できます）。
- LLMはローカルにあるLLMファイルからアップロードする仕様になっています。アップロードしたLLMファイルは、local_llm_for_cpu/llm_resources/llm_modelsに登録されます。開発時のテストでは、[こちらのモデル](https://huggingface.co/mmnga/ELYZA-japanese-Llama-2-7b-fast-instruct-gguf/blob/main/ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf)を使用しました。
- Embeddingモデルは、使用するモデル名をEmbedModelにあらかじめ登録しておき、Q&A実行時にそのモデル名でHuggingFaceからEmbeddingモデルをダウンロードする仕様です。開発時のテストでは、[こちらのモデル](https://huggingface.co/oshizo/sbert-jsnli-luke-japanese-base-lite)を使用しました。
- documentファイルはLLM同様にローカルにあるファイルをアップロードします。このアプリケーションではPDFファイルをアップロードする仕様になっています。アップロードしたPDFファイルは、local_llm_for_cpu/llm_resources/documentsに登録されます。ファイルを登録するときは、ファイル名の入力と関連付けるEmbeddingモデルの選択も必要です。
<br>

- LLM、Embeddingモデル、documentファイルの登録が完了すると、LlamaIndexでコンテキスト拡張したLLMのQ&Aを実行できます。フローは次のようになっています。
  1. 始めにQ&Aで使用するLLMとEmbeddingモデルを選択する（llm_and_embed.htmlで選択フォームが表示される）。
  2. フォームを送信すると、LLMのコンテキスト拡張で使用するdocumentファイルの選択、質問を入力するフォーム画面（document_and_query.html）に遷移する。
  3. documentファイルは、先に選択したEmbeddingモデルに関連付けられているdocumentファイルのみ表示される。また、質問の内容は自由だが、LLMのコンテキスト拡張をしたQ&Aがアプリケーションの趣旨なので、選択したdocumentファイルに関する質問を入力する。
  4. documentファイルを選択し、質問を入力してからフォームを送信するとQ&Aが実行される。CPUでLLMを動かしているため時間を要するが、実行が終わると回答画面（response.html）にLLMが作成した答えが表示される。
<br>

- Q&AはResponseViewでstart_query関数を呼び出して実行します。この関数がアプリケーションの要の部分であり、また、DjangoではなくLlamaIndexがメインとなっているため、簡単にですがコードに一部コメントを入れて説明します。

        # local_llm_for_cpu/local_llm/views.py

        import os
        import sys, logging
        
        logging.basicConfig(stream=sys.stdout, level=logging.NOTSET, force=True)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
        
        from langchain.embeddings.huggingface import HuggingFaceEmbeddings
        from llama_index.llms import LlamaCPP
        from llama_index import (
            VectorStoreIndex,
            ServiceContext,
            StorageContext,
            download_loader,
            PromptTemplate,
            load_index_from_storage,
        )

        ...

        def start_query(llm_pk, embed_pk, document_pk, query):
          llm_resources = settings.MEDIA_ROOT
          PyMuPDFReader = download_loader("PyMuPDFReader")
          loader = PyMuPDFReader()

          # 事前に選択したdocumentファイル（PDF）を読み込む。
          document_file = Document.objects.get(pk=document_pk).document
          document = loader.load_data(file_path=f"{llm_resources}/{document_file}",
                                      metadata=True)

          # LlamaIndexでllama-cpp-pythonを使用するために、LlamaCPPに事前に選択したLLMのパスを渡してLLMをセットアップする。
          model_file = LlmModel.objects.get(pk=llm_pk).llm_model
          model_path = f"{llm_resources}/{model_file}"
          llm = LlamaCPP(model_path=model_path, temperature=0)

          # 事前に選択したEmbeddingモデル名を使って、HuggingFaceからEmbeddingモデルをダウンロードする。
          embed_file = EmbedModel.objects.get(pk=embed_pk).embed_model
          embed_model = HuggingFaceEmbeddings(model_name=embed_file)

          # 開発時に使用したLLM、Embeddingモデルは日本語データで学習したモデルであり、documentも日本語のファイルなので、
          # QAテンプレートもデフォルトの英語テンプレートではなく日本語テンプレートを使用する。
          qa_tmpl_str = (
            "コンテキスト情報は以下のとおりです。\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "事前知識ではなくコンテキスト情報を考慮して、クエリに答えます。\n"
            "Query: {query_str}\n"
            "Answer: "
            )
          refine_tmpl_str = (
            "オリジナルのクエリは次のとおりです: {query_str}。\n"
            "既存の回答は次のとおりです: {existing_answer}\n"
            "以下の追加のコンテキストを使用して、既存の回答を(必要な場合のみ)改良する機会があります。\n"
            "------------\n"
            "{context_msg}\n"
            "------------\n"
            "新しいコンテキストを考慮して、元の回答を改良し、クエリに対するより適切な回答を求めます。コンテキストが役に立たない場合は、元の回答を返します。\n"
            "Refined Answer: "
            )
          qa_tmpl = PromptTemplate(qa_tmpl_str)
          refine_tmpl = PromptTemplate(refine_tmpl_str)

          # サービスコンテキストにセットアップしたLLMとダウンロードしたEmbeddingモデルを設定する。
          service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            )

          # 使用するdocumentについて、選択したEmbeddingモデルで既にベクトルインデックスが作成されている場合は、
          # llm_resources/index_storageに該当のベクトルインデックスがあるので読み込む。
          index_storage = f"{llm_resources}/index_storage/{embed_pk}_{document_pk}"
          if os.path.isdir(index_storage):
            print("index existed")
            storage_context = StorageContext.from_defaults(persist_dir=index_storage)
            index = load_index_from_storage(storage_context,
                                            service_context=service_context)
  
          # 初めて使用するdocumentだったり、documentは使用したことがあるがベクトル化に使ったEmbeddingモデルが今回のモデルと別だったりすると、
          # 該当するベクトルインデックスがないため、新たにベクトルインデックスを作成し、llm_resources/index_storageに保存する。
          else:
            print("Not index existed")
            index = VectorStoreIndex.from_documents(
              document, service_context=service_context, show_progress=True
            )
            os.mkdir(index_storage)
            index.storage_context.persist(persist_dir=index_storage)

          # 作成したインデックス上に、Q&Aを実行するクエリエンジンを構成し、サービスコンテキスト（LLM、Embeddingモデル）やテンプレートを設定する。
          query_engine = index.as_query_engine(
            show_progress=True,
            streaming=True,
            service_context=service_context,
            text_qa_template=qa_tmpl,
            refine_tmpl=refine_tmpl,
            # temperature=0,
            # similarity_top_k=4,
            # response_mode="refine",
          )

          # クエリエンジンを使って質問を実行する。
          response_stream = query_engine.query(query)
          print("response_stream", response_stream)
          
          return response_stream
<br>

- 「1.プロジェクトについて」に書いたとおり、実行速度や精度といったパフォーマンスはあまり高くありませんでした。
- そのため、VectorStoreIndexではなく、Postgresqlを使ったPGVectorStoreを使うことで、ベクトルの類似性による検索だけでなく、キーワード検索も組み合わせたハイブリッド検索を試してみたり、パラメータのsimilarity_top_kをデフォルトの2から4に変更したりしましたが、あまり精度は改善されませんでした。
- 反対に、精度を上げようとすると実行速度がさらに遅くなったため、今回のプロジェクトではパフォーマンスはある程度妥協する結果となりました。

<br>

- テストはlocal_llmディレクトリのtest.pyに、LLMやEmbeddingモデル名、documentファイルの登録などについてのテストコードを書いています。
- テスト用のファイルも同じディレクトリに配置し、正しいディレクトリにファイルが登録されるかをテストしています。
- LLMのQ&Aがメインの機能ということもあり、これまでのプロジェクトと違ってあまり多くのパターンのテストはできていませんが、Q&Aを実行するまでのviewの各機能については一通りテストを行い、レスポンスに意図したテンプレートや文言が含まれているかを確認しています。

