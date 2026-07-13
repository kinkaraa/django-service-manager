from django.core.management.base import BaseCommand
from dashboard.models import Service


class Command(BaseCommand):
    help = 'Update Docker services to have correct service_type'

    def handle(self, *args, **options):
        # Update Docker services
        docker_services = Service.objects.filter(
            name__in=['Service SDK', 'Service BIRT Runtime Engine']
        )
        
        updated = 0
        for service in docker_services:
            service.service_type = 'docker'
            service.save()
            updated += 1
            self.stdout.write(
                self.style.SUCCESS(f'✓ Updated: {service.name} → Docker type')
            )
        
        if updated == 0:
            self.stdout.write(
                self.style.WARNING('⚠ No Docker services found to update')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Updated {updated} Docker services')
            )
