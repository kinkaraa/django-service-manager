from django.contrib import admin

from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Service


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('name', 'service_type', 'pid', 'port', 'order', 'display_is_running')
    list_editable = ('order',)
    search_fields = ('name', 'command', 'working_dir')
    list_filter = ('service_type', 'pid',)
    list_fullwidth = True

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'service_type', 'order', 'port')
        }),
        ('Execution', {
            'fields': ('command', 'working_dir')
        }),
        ('Docker (Optional)', {
            'fields': ('docker_container_name',),
            'classes': ('collapse',),
            'description': 'Untuk service Docker, isi nama container jika ingin tracking lebih spesifik'
        }),
        ('Status', {
            'fields': ('pid',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('pid',)

    @display(description='Status', header=True)
    def display_is_running(self, obj):
        if obj.is_running():
            return 'Running', 'success'
        return 'Stopped', 'danger'
