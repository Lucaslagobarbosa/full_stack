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

# Mantenha as demais classes (Exemplar, Membro, Empréstimo, Reserva) como já estão...