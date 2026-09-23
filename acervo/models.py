from django.db import models
from django.utils import timezone
from datetime import timedelta

class Autor(models.Model):
    nome = models.CharField(max_length=150)
    nacionalidade = models.CharField(max_length=100, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    TIPO_ACERVO_CHOICES = [
        ('DIGITAL', 'Digital'),
        ('FISICO', 'Físico'),
    ]

    CATEGORIA_CHOICES = [
        ('000', '000 – Generalidades e Informação: Obras gerais, enciclopédias, jornais e biblioteconomia.'),
        ('100', '100 – Filosofia e Psicologia: Ética, lógica e investigações sobre a mente humana.'),
        ('200', '200 – Religião e Teologia: Mitologia, teologia e estudos sobre crenças e religiões.'),
        ('300', '300 – Ciências Sociais e Direito: Política, economia, sociologia, educação e leis.'),
        ('400', '400 – Linguística e Idiomas: Gramáticas, dicionários e estudos de línguas.'),
        ('500', '500 – Ciências Puras (Exatas e Naturais): Matemática, física, química, biologia e astronomia.'),
        ('600', '600 – Ciências Aplicadas (Tecnologia): Medicina, engenharia, agricultura e administração.'),
        ('700', '700 – Artes e Recreação: Pintura, música, arquitetura, esportes e lazer.'),
        ('800', '800 – Literatura: Poesia, romances, contos, crônicas e crítica literária.'),
        ('900', '900 – História e Geografia: Biografias, viagens e acontecimentos históricos'),
    ]

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    ano_publicacao = models.IntegerField()
    tipo_acervo = models.CharField(
        max_length=10, 
        choices=TIPO_ACERVO_CHOICES, 
        default='FISICO'
    )
    categoria = models.CharField(
        max_length=3, 
        choices=CATEGORIA_CHOICES, 
        default='000'
    )

    def __str__(self):
        return f"{self.titulo} ({self.autor.nome})"

class Exemplar(models.Model):
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('EMPRESTADO', 'Emprestado'),
        ('MANUTENCAO', 'Em Manutenção'),
    ]
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='exemplares')
    codigo_patrimonio = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')

    def __str__(self):
        return f"Exemplar {self.codigo_patrimonio} - {self.livro.titulo}"

class Membro(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Empréstimo(models.Model):
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(default=timezone.now)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(blank=True, null=True)
    multa_calculada = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_devolucao_prevista = timezone.now().date() + timedelta(days=14)
            self.exemplar.status = 'EMPRESTADO'
            self.exemplar.save()
        super().save(*args, **kwargs)

    def calcular_multa(self):
        if self.ativo and self.data_devolucao_real is None:
            hoje = timezone.now().date()
            if hoje > self.data_devolucao_prevista:
                atraso = (hoje - self.data_devolucao_prevista).days
                self.multa_calculada = atraso * 2.50
            else:
                self.multa_calculada = 0.00
        elif self.data_devolucao_real and self.data_devolucao_real > self.data_devolucao_prevista:
            atraso = (self.data_devolucao_real - self.data_devolucao_prevista).days
            self.multa_calculada = atraso * 2.50
        return self.multa_calculada

    def __str__(self):
        return f"Empréstimo: {self.exemplar.livro.titulo} para {self.membro.nome}"

class Reserva(models.Model):
    STATUS_RESERVA = [
        ('AGUARDANDO', 'Aguardando'),
        ('ATENDIDA', 'Atendida'),
        ('CANCELADA', 'Cancelada'),
    ]
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reservas')
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_RESERVA, default='AGUARDANDO')

    def __str__(self):
        return f"Reserva #{self.id} - {self.livro.titulo} por {self.membro.nome}"