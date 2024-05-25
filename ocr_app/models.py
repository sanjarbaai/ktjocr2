from django.db import models
from django.contrib.auth.models import User


class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"PDFFile(id={self.id}, uploaded_at={self.uploaded_at})"


class OCRResult(models.Model):
    pdf_file = models.ForeignKey(PDFFile, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    original_image_path = models.CharField(max_length=255)
    image_paths = models.JSONField(default=list)
    texts = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"OCRResult(id={self.id}, document_name={self.document_name})"