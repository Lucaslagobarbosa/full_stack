from django import forms
from .models import Autor, Livro, Exemplar, Membro, Empréstimo, Reserva

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = ['livro', 'codigo_patrimonio', 'status']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'codigo_patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Empréstimo
        fields = ['exemplar', 'membro']
        widgets = {
            'exemplar': forms.Select(attrs={'class': 'form-control'}),
            'membro': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_exemplar(self):
        exemplar = self.cleaned_data.get('exemplar')
        if exemplar.status != 'DISPONIVEL':
            raise forms.ValidationError("Este exemplar não está disponível para empréstimo.")
        return exemplar

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro', 'membro']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'membro': forms.Select(attrs={'class': 'form-control'}),
        }
