from django.shortcuts import render, get_object_or_404
from .models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    """ Detalhar funções - docstring """
    # receitas = Receita.objects.all()
    # receitas = Receita.objects.filter(publicada=True) # para apenas mostrar o que estiver como True
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    
    #paginação 
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')  # identificar a pagina que estou
    receitas_por_pagina = paginator.get_page(page)
    
    
    dados = {'receitas':receitas_por_pagina}  
    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    
    receita_exibir = {
        'receita': receita
    }
    
    return render(request, 'receita.html', receita_exibir)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    
    if 'buscar' in request.GET:
        nome_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_buscar)
            
    dados = {
        'receitas': lista_receitas
    }        
    
    
    return render (request, 'buscar.html', dados)
