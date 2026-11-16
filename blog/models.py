from django.db import models
from django.urls import reverse


class Post(models.Model):
    """Uma materia do blog.

    O conteudo e guardado como HTML cru, e o template usa o filtro `safe` para
    renderizar. E de proposito: assim o corpo do post pode trazer tabela de
    estatisticas e placar de partida sem precisar de um editor de texto rico.
    """

    titulo = models.CharField('titulo', max_length=200)
    conteudo = models.TextField(
        'conteudo (HTML)',
        help_text='Aceita HTML. Renderizado no template com o filtro safe.',
    )
    data_postagem = models.DateTimeField('data de postagem')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-data_postagem']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])
