from django.contrib import admin

from .models import Category, Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem', 'total_comentarios', 'lista_categorias')
    list_filter = ('data_postagem', 'categorias')
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_postagem'
    filter_horizontal = ('categorias',)
    inlines = [CommentInline]

    @admin.display(description='comentários')
    def total_comentarios(self, post):
        return post.comentarios.count()

    @admin.display(description='categorias')
    def lista_categorias(self, post):
        return ', '.join(c.nome for c in post.categorias.all()) or '—'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'data_postagem')
    list_filter = ('data_postagem', 'autor')
    search_fields = ('texto',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nome', 'total_posts')
    search_fields = ('nome', 'descricao')

    @admin.display(description='posts')
    def total_posts(self, categoria):
        return categoria.posts.count()
