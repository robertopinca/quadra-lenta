from django.contrib import admin

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem', 'total_comentarios')
    list_filter = ('data_postagem',)
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_postagem'
    inlines = [CommentInline]

    @admin.display(description='comentários')
    def total_comentarios(self, post):
        return post.comentarios.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'data_postagem')
    list_filter = ('data_postagem', 'autor')
    search_fields = ('texto',)
