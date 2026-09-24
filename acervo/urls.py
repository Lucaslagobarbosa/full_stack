from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/novo/', views.criar_autor, name='criar_autor'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/novo/', views.criar_livro, name='criar_livro'),
    path('exemplares/', views.lista_exemplares, name='lista_exemplares'),
    path('exemplares/novo/', views.criar_exemplar, name='criar_exemplar'),
    path('exemplares/<int:pk>/alternar-status/', views.alternar_status_exemplar, name='alternar_status_exemplar'),
    path('membros/', views.lista_membros, name='lista_membros'),
    path('membros/novo/', views.criar_membro, name='criar_membro'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('emprestimos/novo/', views.realizar_emprestimo, name='realizar_emprestimo'),
    path('emprestimos/devolver/<int:pk>/', views.registrar_devolucao, name='registrar_devolucao'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/nova/', views.criar_reserva, name='criar_reserva'),
]