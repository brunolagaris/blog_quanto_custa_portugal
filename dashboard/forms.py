from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full text-4xl font-bold bg-transparent border-none focus:ring-0 placeholder-slate-300 px-0 mb-2',
                'placeholder': 'Título do Artigo...'
            }),
            'content': forms.Textarea(attrs={
                'id': 'editor-content', # ID fixo para o JS encontrar
                'class': 'hidden',      # Esconde o original
                'required': False       # Evita o erro de "not focusable"
            }),
        }