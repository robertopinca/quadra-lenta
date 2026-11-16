"""Views do blog - VERSAO 3.

Terceira das tres versoes pedidas no enunciado: o CRUD inteiro com as classes
genericas do Django.

Duas coisas que as versoes anteriores faziam a mao e agora saem de graca:
DetailView ja responde 404 para pk inexistente, e DeleteView ja renderiza
blog/post_confirm_delete.html no GET, pedindo a confirmacao antes de apagar.
"""
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


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
