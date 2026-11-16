from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Form do Post, usado a partir da versao 2 das views.

    E aqui que entra a validacao que a versao 1 nao tinha: titulo obrigatorio,
    conteudo obrigatorio e data de postagem valida.
    """

    class Meta:
        model = Post
        fields = ['titulo', 'data_postagem', 'categorias', 'conteudo']
        widgets = {
            'data_postagem': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'categorias': forms.CheckboxSelectMultiple(),
            'conteudo': forms.Textarea(attrs={'spellcheck': 'false'}),
        }
        labels = {
            'titulo': 'Título',
            'data_postagem': 'Data de postagem',
            'categorias': 'Categorias',
            'conteudo': 'Conteúdo (HTML)',
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo'].strip()
        if len(titulo) < 4:
            raise forms.ValidationError('O título está curto demais.')
        return titulo


class CommentForm(forms.ModelForm):
    """Form do comentario.

    O autor e um campo de escolha entre os usuarios cadastrados: autenticacao
    e assunto do laboratorio 5, e esta entrega nao a pede. Os usuarios sao
    criados pelo administrador, a partir do super-usuario.
    """

    class Meta:
        model = Comment
        fields = ['autor', 'texto']
        labels = {
            'autor': 'Comentando como',
            'texto': 'Comentário',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autor'].empty_label = 'escolha um usuário'

    def clean_texto(self):
        texto = self.cleaned_data['texto'].strip()
        if len(texto) < 3:
            raise forms.ValidationError('Escreva alguma coisa antes de enviar.')
        return texto
