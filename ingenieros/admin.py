from django.contrib import admin
from .models import EngineerModel, AdministracionModel, EquiposModel, InspeccionesModel

# Register your models here.

class EquiposModelAdmin(admin.ModelAdmin):
    populated_fields = {
        "slug" : ("calle", "equipo_numer",)
    }
    readonly_fields = ("slug", "qr",)


admin.site.register(EngineerModel)
admin.site.register(AdministracionModel)
admin.site.register(EquiposModel, EquiposModelAdmin)
admin.site.register(InspeccionesModel)

