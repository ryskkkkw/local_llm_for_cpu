from pathlib import Path
import time

from django.test import TestCase
from django.urls import reverse

from config import settings
from .models import LlmModel, EmbedModel, Document


class LlmModeRegisterlViewTest(TestCase):
  def test_llm_register(self):
    test_file = "test-llm-model.gguf"
    test_file_path = Path(settings.BASE_DIR, "local_llm", test_file)
    
    with open(test_file_path, "r") as f:
      response = self.client.post(reverse("local_llm:register_llm"), 
                                  {"llm_model": f})
      response = self.client.get(response.url)
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, "index.html")
      
      registered_file_path = Path(settings.BASE_DIR, "llm_resources",
                                  "llm_models", test_file)
      self.assertTrue(Path.exists(registered_file_path))
      time.sleep(2)
      Path.unlink(registered_file_path)
      

class EmbedModelRegisterViewTest(TestCase):
  def test_embed_register(self):
    response = self.client.post(reverse("local_llm:register_embed"),
                                {"embed_model": "test/test-embed-model"})
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "index.html")


class DocumentRegisterlViewTest(TestCase):
  def test_document_register(self):
    test_file = "test_document1.pdf"
    test_file_path = Path(settings.BASE_DIR, "local_llm", test_file)
    embed_model = EmbedModel.objects.create(embed_model=
                                            "test/test-embed-model")
    
    with open(test_file_path, "r") as f:
      response = self.client.post(reverse("local_llm:register_document"), 
                                  {"document": f,
                                   "document_name": test_file,
                                   "embed_model": embed_model})
      response = self.client.get(response.url)
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, "index.html")
      
      registered_file_path = Path(settings.BASE_DIR, "llm_resources", 
                                  "documents", test_file)
      self.assertTrue(Path.exists(registered_file_path))
      time.sleep(2)
      Path.unlink(registered_file_path)


class LlmAndEmbedlViewTest(TestCase):    
  def test_llm_embed_view(self):
    test_llm_file = "test-llm-model.gguf"
    test_llm_file_path = Path(settings.BASE_DIR, "local_llm", 
                              test_llm_file)
    with open(test_llm_file_path, "r") as f:
      self.client.post(reverse("local_llm:register_llm"), 
                       {"llm_model": f})
    test_llm_model = LlmModel.objects.first()
    
    self.client.post(reverse("local_llm:register_embed"),
                     {"embed_model": "test/test-embed-model1"})
    self.client.post(reverse("local_llm:register_embed"),
                     {"embed_model": "test/test-embed-model2"})
    test_embed_model1 = EmbedModel.objects.first()
    test_embed_model2 = EmbedModel.objects.last()
    
    response = self.client.get(reverse("local_llm:llm_and_embed"))
    print(response)
    print(response.content)
    self.assertTemplateUsed(response, "llm_and_embed.html")
    self.assertContains(response, test_llm_model)
    self.assertContains(response, test_embed_model1.embed_model)
    self.assertContains(response, test_embed_model2.embed_model)
    
    time.sleep(2)
    registered_file_path = Path(settings.BASE_DIR, "llm_resources",
                                "llm_models", test_llm_file)
    Path.unlink(registered_file_path)


class DocumentAndQueryViewTest(TestCase):
  def test_document_query_view(self):
    test_llm_file = "test-llm-model.gguf"
    test_llm_file_path = Path(settings.BASE_DIR, "local_llm", 
                              test_llm_file)
    with open(test_llm_file_path, "r") as f:
      self.client.post(reverse("local_llm:register_llm"), 
                       {"llm_model": f})
    test_llm_model = LlmModel.objects.first()
    print(test_llm_model.pk, test_llm_model)
    
    self.client.post(reverse("local_llm:register_embed"),
                     {"embed_model": "test/test-embed-model1"})
    self.client.post(reverse("local_llm:register_embed"),
                     {"embed_model": "test/test-embed-model2"})
    test_embed_model1 = EmbedModel.objects.first()
    test_embed_model2 = EmbedModel.objects.last()
    print(test_embed_model1.pk, test_embed_model1.embed_model)
    print(test_embed_model2.pk, test_embed_model2.embed_model)

    test_doc_file1 = "test_document1.pdf"
    test_doc_file_path1 = Path(settings.BASE_DIR, "local_llm", 
                                test_doc_file1) 
    with open(test_doc_file_path1, "r") as f:
      self.client.post(reverse("local_llm:register_document"), 
                       {"document": f,
                        "document_name": test_doc_file1,
                        "embed_model": test_embed_model1})
    test_document1 = Document.objects.first()
    print(test_document1.document_name)
      
    test_doc_file2 = "test_document2.pdf"
    test_doc_file_path2 = Path(settings.BASE_DIR, "local_llm", 
                                test_doc_file2) 
    with open(test_doc_file_path2, "r") as f:
      self.client.post(reverse("local_llm:register_document"), 
                       {"document": f,
                        "document_name": test_doc_file2,
                        "embed_model": test_embed_model2})
    test_document2 = Document.objects.last()
    print(test_document2.document_name)
    
    response = self.client.get(reverse("local_llm:document_and_query"),
                               {"llm": test_llm_model.pk,
                                "embed": test_embed_model1.pk})
    print(response)
    print(response.content)
    self.assertTemplateUsed(response, "document_and_query.html")
    self.assertContains(response, test_document1.document_name)
    self.assertNotContains(response, test_document2.document_name)
    
    time.sleep(2)
    registered_file_path = Path(settings.BASE_DIR, "llm_resources",
                                "llm_models", test_llm_file)
    Path.unlink(registered_file_path)
    
    registered_file_path = Path(settings.BASE_DIR, "llm_resources", 
                                "documents", test_doc_file1)
    Path.unlink(registered_file_path)
    
    registered_file_path = Path(settings.BASE_DIR, "llm_resources", 
                                "documents", test_doc_file2)
    Path.unlink(registered_file_path)
