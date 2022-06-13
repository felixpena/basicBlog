from django.contrib import admin

# Register your models here.

from .models import BlogAuthor, Blog, BlogComment


# Minimal registration of Models.
admin.site.register(BlogAuthor)
admin.site.register(BlogComment)


class BlogCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = BlogComment
    max_num=0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Administration object for Blog models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of blog comments in blog view (inlines)

    Objeto de administración para los modelos de Blog. 
    Define:
     - los campos a mostrar en la vista de lista (list_display)
     - ordena los campos en la vista de detalle (fields), agrupando los campos de fecha horizontalmente
     - añade la adición en línea de los comentarios del blog en la vista de blog (inlines)

    """
    list_display = ('name', 'author', 'post_date')
    inlines = [BlogCommentsInline]
