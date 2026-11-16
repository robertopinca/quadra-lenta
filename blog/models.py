from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Categoria de posts. Um post pode estar em varias."""

    nome = models.CharField('nome', max_length=80, unique=True)
    descricao = models.TextField('descricao', blank=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.pk])


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
    categorias = models.ManyToManyField(
        Category,
        related_name='posts',
        blank=True,
        verbose_name='categorias',
    )

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-data_postagem']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])


class Comment(models.Model):
    """Comentario de um leitor num post.

    O autor referencia o modelo User do Django por settings.AUTH_USER_MODEL,
    como recomenda a documentacao, em vez de importar User direto.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='post',
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='autor',
    )
    texto = models.TextField('texto')
    data_postagem = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
        # Mais recente primeiro, como pede o enunciado.
        ordering = ['-data_postagem']

    def __str__(self):
        return f'{self.autor} em "{self.post.titulo}"'

    def get_absolute_url(self):
        return self.post.get_absolute_url()
