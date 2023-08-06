from django.contrib import admin
from .models import *

admin.site.register(ContractType)
admin.site.register(Category)
admin.site.register(Contract)
admin.site.register(BasicSalary)
admin.site.register(PositionSalary)
admin.site.register(EmpSalary)
admin.site.register(EmpPlacement)
admin.site.register(EmpPosition)
admin.site.register(EmpContractToR)


class OrganogramaAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Organograma, OrganogramaAdmin)
