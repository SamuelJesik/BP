from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


from django.utils.deconstruct import deconstructible
import os

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # Create the folder structure 'uploads/user_id/filename.ext'
        folder_name = str(instance.user.id)
        return os.path.join(self.sub_path, folder_name, filename)

path_and_rename = PathAndRename("uploads")




class RefactoringTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    input_code = models.TextField(help_text="Pôvodný kód na refaktorizáciu.")
    expected_output = models.TextField(help_text="Očakávaný výstup po refaktorizácii.", null=True, blank=True)
    code_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    
class UploadedFile(models.Model):
    file = models.FileField(upload_to=path_and_rename)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    RefactoringTask = models.ForeignKey(RefactoringTask, on_delete=models.CASCADE, related_name='uploaded_files')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')

    def __str__(self):
        return self.title
