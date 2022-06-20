from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # traz o modelo de usuários
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
            nome = request.POST['nome']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if not nome.strip():
                messages.error(request, 'O campo nome nao pode ficar vazio')
                return redirect ('cadastro')
            if not email.strip():
                messages.error(request, 'O campo email nao pode ficar vazio')
                return redirect ('cadastro')
            if password != password2:
                messages.error(request, 'As senhas nao sao iguais')
                return redirect ('cadastro')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Usuário ja cadastrado')
                return redirect ('cadastro')
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário ja cadastrado')
                return redirect ('cadastro')
            user = User.objects.create_user(username=nome, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso!!!')         
            return redirect('login')        
    else:        
        return render(request, 'usuarios/cadastro.html')
    
def login(request):
    if request.method == 'POST':
            email = request.POST['email']
            senha = request.POST['senha']
            
            if email == '' or senha == '':
                messages.error(request, 'O campo email ou senha nao podem ficar vazios')
                return redirect('login')
            if User.objects.filter(email=email).exists():
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()  # ele filtra no email e baseado nele e traz o username
                user = auth.authenticate(request, username = nome, password=senha)
                if user is not None:
                    auth.login(request, user)           
                    return redirect('dashboard')   
    return render(request, 'usuarios/login.html')
    
def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        dados = {
            'receitas': receitas
        }
        
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        
        receita = Receita.objects.create(
            pessoa=user,
            nome_receita=nome_receita,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo,
            rendimento=rendimento,
            categoria=categoria,
            foto_receita=foto_receita,
            )
        receita.save() # depois de pegar do form, ele taz passa pras variaveis da receita e esse comando salva no BD
        
        
        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')
    
# posso criar funções para otimizar as descrições

def deleta_receita(request,receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')
    
    
def edita_receita(request,receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'usuarios/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')
        
        
    