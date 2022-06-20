from django.db import models

# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return self.nome
