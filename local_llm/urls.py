from django.urls import path

from django.views.generic import TemplateView

from . import views


app_name = "local_llm"

urlpatterns = [
  path("", TemplateView.as_view(
    template_name="index.html"), name="index"),
  path("register_llm", 
       views.LlmModelRegisterView.as_view(), name="register_llm"),
  path("register_embed", 
       views.EmbedModelRegisterView.as_view(), name="register_embed"),
  path("register_document", 
       views.DocumentRegisterView.as_view(), name="register_document"),
  path("llm_and_embed", 
       views.LlmAndEmbedlView.as_view(), name="llm_and_embed"),
  path("document_and_query", 
       views.DocumentAndQuerylView.as_view(), name="document_and_query"),
  path("response/<str:llm>/<str:embed>/", 
       views.ResponseView.as_view(), name="response"),
]
