from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'pid', 'port', 'order', 'is_running')
    list_editable = ('order',)
    search_fields = ('name', 'command', 'working_dir')
    list_filter = ('service_type', 'pid',)
    
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
    
    def is_running(self, obj):
        return '✅ Running' if obj.is_running() else '❌ Stopped'
    is_running.short_description = 'Status'