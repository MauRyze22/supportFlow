from django.contrib import admin
from .models import Ticket, Comentario, Categoria

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'created']
    search_fields = ['nombre']
    list_editable = ['color']
    
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ['creador', 'asignado', 'titulo', 'estado'] 
    search_fields = ['titulo']
    
    
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['creador', 'ticket'] 
    search_fields = ['titulo']
    
    
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Categoria, CategoriaAdmin)
