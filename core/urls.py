from django.contrib import admin
from django.urls import path

from dashboard.views import (
    home,
    start_service,
    stop_service,
    restart_service,
    start_all_services,
    stop_all_services,
    view_logs,
    clear_logs,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('start/<int:service_id>/', start_service),
    path('stop/<int:service_id>/', stop_service),
    path('restart/<int:service_id>/', restart_service),

    path('start-all/', start_all_services),
    path('stop-all/', stop_all_services),
    
    path('logs/<int:service_id>/', view_logs),
    path('logs/<int:service_id>/clear/', clear_logs),
]