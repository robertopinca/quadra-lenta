"""Views do blog - VERSAO 3.

Terceira das tres versoes pedidas no enunciado: o CRUD inteiro com as classes
genericas do Django.

Duas coisas que as versoes anteriores faziam a mao e agora saem de graca:
DetailView ja responde 404 para pk inexistente, e DeleteView ja renderiza
blog/post_confirm_delete.html no GET, pedindo a confirmacao antes de apagar.
"""
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Form em branco para comentar sem sair da pagina do post.
        contexto['comment_form'] = CommentForm()
        return contexto


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    extra_context = {'acao': 'Escrever post'}


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    extra_context = {'acao': 'Editar post'}


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categorias'


class CategoryDetailView(DetailView):
    """Pagina individual de categoria.

    Reaproveita blog/post_list.html, como pede o enunciado: o mesmo template
    da listagem geral, com a categoria no contexto para o cabecalho mudar.
    """

    model = Category
    template_name = 'blog/post_list.html'
    context_object_name = 'categoria'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['posts'] = self.object.posts.all()
        return contexto


class CommentCreateView(CreateView):
    """Cria um comentario preso ao post que veio na URL."""

    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # 404 se o post da URL nao existe.
        self.post_comentado = get_object_or_404(Post, pk=kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['post'] = self.post_comentado
        return contexto

    def form_valid(self, form):
        form.instance.post = self.post_comentado
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_comentado.get_absolute_url()
