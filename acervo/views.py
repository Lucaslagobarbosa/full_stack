from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Autor, Livro, Exemplar, Membro, Empréstimo, Reserva
from .forms import AutorForm, LivroForm, ExemplarForm, MembroForm, EmprestimoForm, ReservaForm

def index(request):
    total_livros = Livro.objects.count()
    total_membros = Membro.objects.count()
    emprestivos_ativos = Empréstimo.objects.filter(ativo=True).count()
    reservas_pendentes = Reserva.objects.filter(status='AGUARDANDO').count()
    
    context = {
        'total_livros': total_livros,
        'total_membros': total_membros,
        'emprestivos_ativos': emprestivos_ativos,
        'reservas_pendentes': reservas_pendentes,
    }
    return render(request, 'acervo/index.html', context)

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'acervo/lista_autores.html', {'autores': autores})

def criar_autor(request):
    form = AutorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_autores')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Novo Autor'})

def lista_livros(request):
    livros = Livro.objects.select_related('autor').all()
    return render(request, 'acervo/lista_livros.html', {'livros': livros})

def criar_livro(request):
    form = LivroForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_livros')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Novo Livro'})

def lista_exemplares(request):
    exemplares = Exemplar.objects.select_related('livro').all()
    return render(request, 'acervo/lista_exemplares.html', {'exemplares': exemplares})

def criar_exemplar(request):
    form = ExemplarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_exemplares')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Novo Exemplar'})

def lista_membros(request):
    membros = Membro.objects.all()
    return render(request, 'acervo/lista_membros.html', {'membros': membros})

def criar_membro(request):
    form = MembroForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_membros')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Novo Membro'})

def lista_emprestimos(request):
    emprestimos = Empréstimo.objects.select_related('exemplar__livro', 'membro').all()
    for e in emprestimos:
        e.calcular_multa()
    return render(request, 'acervo/lista_emprestimos.html', {'emprestimos': emprestimos})

def realizar_emprestimo(request):
    form = EmprestimoForm(request.POST or None)
    if form.is_valid():
        emprestimo = form.save()
        reserva = Reserva.objects.filter(livro=emprestimo.exemplar.livro, membro=emprestimo.membro, status='AGUARDANDO').first()
        if reserva:
            reserva.status = 'ATENDIDA'
            reserva.save()
        return redirect('lista_emprestimos')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Realizar Empréstimo'})

def registrar_devolucao(request, pk):
    emprestimo = get_object_or_404(Empréstimo, pk=pk)
    if emprestimo.ativo:
        emprestimo.data_devolucao_real = timezone.now().date()
        emprestimo.ativo = False
        emprestimo.calcular_multa()
        emprestimo.save()
        
        exemplar = emprestimo.exemplar
        exemplar.status = 'DISPONIVEL'
        exemplar.save()
    return redirect('lista_emprestimos')

def lista_reservas(request):
    reservas = Reserva.objects.select_related('livro', 'membro').all()
    return render(request, 'acervo/lista_reservas.html', {'reservas': reservas})

def criar_reserva(request):
    form = ReservaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_reservas')
    return render(request, 'acervo/form_generico.html', {'form': form, 'titulo': 'Nova Reserva'})
