from django.contrib import admin
from .models import Ticket, Comentario, Categoria

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'created']
    search_fields = ['nombre']
    list_editable = ['color']

admin.site.register(Ticket)
admin.site.register(Comentario)
admin.site.register(Categoria, CategoriaAdmin)
