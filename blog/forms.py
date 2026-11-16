from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Form do Post, usado a partir da versao 2 das views.

    E aqui que entra a validacao que a versao 1 nao tinha: titulo obrigatorio,
    conteudo obrigatorio e data de postagem valida.
    """

    class Meta:
        model = Post
        fields = ['titulo', 'data_postagem', 'conteudo']
        widgets = {
            'data_postagem': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'conteudo': forms.Textarea(attrs={'spellcheck': 'false'}),
        }
        labels = {
            'titulo': 'Título',
            'data_postagem': 'Data de postagem',
            'conteudo': 'Conteúdo (HTML)',
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo'].strip()
        if len(titulo) < 4:
            raise forms.ValidationError('O título está curto demais.')
        return titulo
