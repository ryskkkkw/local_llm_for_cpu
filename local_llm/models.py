from django.db import models
from django.urls import reverse

"""
llm_model -> llm_model file upload from local or download from huggingface.
embed_model ->  embed_model file name for download from huggingface.
documents(PDF) ->  PDF file upload from local or download from web.
index -> consists of 4-5 json files, Not need Django Model Database.

>> embed_model and documents are one to many field relations.
"""

class LlmModel(models.Model):
  llm_model = models.FileField(upload_to="llm_models/")
  
  def __str__(self):
    return str(self.llm_model)
  
  def get_absolute_url(self):
    return reverse("local_llm:index")
  

class EmbedModel(models.Model):
  embed_model = models.CharField(max_length=200)
  
  def __str__(self):
    return str(self.pk)
  
  def get_absolute_url(self):
    return reverse("local_llm:index")


class Document(models.Model):
  document = models.FileField(upload_to="documents/")
  document_name = models.CharField(max_length=200)
  embed_model = models.ForeignKey(EmbedModel, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.document}, {self.document_name}, {self.embed_model}"
  
  def get_absolute_url(self):
    return reverse("local_llm:index")
