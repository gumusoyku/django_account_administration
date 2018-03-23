from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "IBAN")
    search_fields = ("first_name", "last_name")
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(AccountAdmin, self).save_model(request=request, obj=obj, form=form, change=change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.created_by != request.user and not request.user.is_superuser:
            return "first_name", "last_name", "IBAN", "created_by"
        else:
            return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request=request, object_id=object_id)
        if (obj and obj.created_by == request.user) or request.user.is_superuser:
            extra_context = {
                "can_edit": True
            }

        return super(AccountAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {
                "can_edit": True
        }
        return super(AccountAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
