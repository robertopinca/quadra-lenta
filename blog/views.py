"""Views do blog - VERSAO 1.

Primeira das tres versoes pedidas no enunciado: apenas views funcionais, sem
usar Django forms e sem validacao de dados. O que chega em request.POST vai
direto para o modelo.
"""
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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
        data = parse_datetime(request.POST.get('data_postagem', ''))
        post = Post.objects.create(
            titulo=request.POST.get('titulo', ''),
            conteudo=request.POST.get('conteudo', ''),
            data_postagem=data or timezone.now(),
        )
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_form.html', {'acao': 'Escrever post'})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.titulo = request.POST.get('titulo', '')
        post.conteudo = request.POST.get('conteudo', '')
        data = parse_datetime(request.POST.get('data_postagem', ''))
        if data:
            post.data_postagem = data
        post.save()
        return redirect('post_detail', pk=post.pk)

    return render(
        request,
        'blog/post_form.html',
        {'post': post, 'acao': 'Editar post'},
    )


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    # GET mostra a pagina de confirmacao exigida pelo enunciado.
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
