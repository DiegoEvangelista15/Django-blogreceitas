from django.contrib import admin
from .models import Pessoa
# Register your models here.

class ListandoPessoa(admin.ModelAdmin):
    list_display = ('nome','email')
    search_fields = ('nome',)
    list_per_page = 3       
    
    


admin.site.register(Pessoa, ListandoPessoa)
