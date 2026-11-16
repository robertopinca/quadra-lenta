"""Views do blog - VERSAO 2.

Segunda das tres versoes pedidas no enunciado: continuam sendo views
funcionais, mas agora o CRUD passa por um Django form (PostForm), que traz a
validacao que faltava na versao 1.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    # get_object_or_404 responde 404 quando o post nao existe.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_form.html',
        {'form': form, 'acao': 'Escrever post'},
    )


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/post_form.html',
        {'form': form, 'post': post, 'acao': 'Editar post'},
    )


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    # GET mostra a pagina de confirmacao exigida pelo enunciado.
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
