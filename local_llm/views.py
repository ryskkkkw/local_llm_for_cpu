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

from django.views.generic import CreateView, TemplateView
from .models import LlmModel, EmbedModel, Document
from config import settings

class LlmModelRegisterView(CreateView):
  model = LlmModel
  fields = ["llm_model"]
  template_name = "llm_register.html"


class EmbedModelRegisterView(CreateView):
  model = EmbedModel
  fields = ["embed_model"]
  template_name = "embed_register.html"

class DocumentRegisterView(CreateView):
  model = Document
  fields = ["document", "document_name", "embed_model"]
  template_name = "document_register.html"
  
  
class LlmAndEmbedlView(TemplateView):
  template_name = "llm_and_embed.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    context["llm_model"] = LlmModel.objects.all()
    context["embed_model"] = EmbedModel.objects.all()
    
    return context
  
  
class DocumentAndQuerylView(TemplateView):
  template_name = "document_and_query.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
   
    context["llm"] = self.request.GET.get("llm")
    context["embed"] = self.request.GET.get("embed")
    context["documents"] = Document.objects.filter(embed_model=self.request.GET.get("embed"))
    
    return context
 
  
class ResponseView(TemplateView):
  template_name = "response.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    llm_pk = self.kwargs.get("llm")
    embed_pk = self.kwargs.get("embed")
    document_pk = self.request.GET.get("document")
    query = self.request.GET.get("query")
    
    print("llm", llm_pk)
    print("embed", embed_pk)
    print("document", document_pk)
    print("query", query)
    print("MEDIA_ROOT", settings.MEDIA_ROOT)
    print("document", Document.objects.get(pk=document_pk).document)
    print("document_embed", Document.objects.get(pk=document_pk).embed_model)
    
    response = start_query(llm_pk, embed_pk, document_pk, query)
    
    context["query"] = query
    context["response"] = response
    return context
  

def start_query(llm_pk, embed_pk, document_pk, query):
  llm_resources = settings.MEDIA_ROOT
  
  PyMuPDFReader = download_loader("PyMuPDFReader")
  loader = PyMuPDFReader()
  
  document_file = Document.objects.get(pk=document_pk).document
  document = loader.load_data(file_path=f"{llm_resources}/{document_file}",
                              metadata=True)
  
  model_file = LlmModel.objects.get(pk=llm_pk).llm_model
  model_path = f"{llm_resources}/{model_file}"
  llm = LlamaCPP(model_path=model_path, temperature=0)
  
  embed_file = EmbedModel.objects.get(pk=embed_pk).embed_model
  embed_model = HuggingFaceEmbeddings(model_name=embed_file)
  
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
  
  service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
    )
  
  index_storage = f"{llm_resources}/index_storage/{embed_pk}_{document_pk}"
  if os.path.isdir(index_storage):
    print("index existed")
    storage_context = StorageContext.from_defaults(persist_dir=index_storage)
    index = load_index_from_storage(storage_context,
                                    service_context=service_context)
  else:
    print("Not index existed")
    index = VectorStoreIndex.from_documents(
      document, service_context=service_context, show_progress=True
    )
    os.mkdir(index_storage)
    index.storage_context.persist(persist_dir=index_storage)
    
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
  
  response_stream = query_engine.query(query)
  print("response_stream", response_stream)
  
  return response_stream