from django.core.management.base import BaseCommand
from dashboard.models import Service


class Command(BaseCommand):
    help = 'Setup initial services'

    def handle(self, *args, **options):
        services = [
            {
                'name': 'Service Collection',
                'command': 'go run cmd/web/main.go',
                'working_dir': '~/Documents/ilham/Work_Samb/service-collection',
            },
            {
                'name': 'Service Proxy',
                'command': 'go run main.go',
                'working_dir': '~/Documents/ilham/Work_Samb/service-proxy',
            },
            {
                'name': 'Service Proxy Frontend',
                'command': 'npm run dev',
                'working_dir': '~/Documents/ilham/Work_Samb/service-proxy/public',
            },
            {
                'name': 'Service Master',
                'command': 'go run cmd/web/main.go',
                'working_dir': '~/Documents/ilham/Work_Samb/service-master',
            },
            {
                'name': 'Service Identity Access',
                'command': 'go run main.go',
                'working_dir': '~/Documents/ilham/Work_Samb/service-identity-access',
            },
            {
                'name': 'Service Print',
                'command': 'go run cmd/web/main.go',
                'working_dir': '~/Documents/ilham/Work_Samb/service-print',
            },
            {
                'name': 'Service SDK',
                'command': 'docker-compose up -d',
                'working_dir': '~/Documents/ilham/Work_Samb/service_sdk',
                'service_type': 'docker',
            },
            {
                'name': 'Service BIRT Runtime Engine',
                'command': 'docker-compose up -d',  # Remove sudo - user harus di docker group
                'working_dir': '~/Documents/ilham/Work_Samb/service-birt-runtime-engine',
                'service_type': 'docker',
            },
        ]

        for service_data in services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'command': service_data['command'],
                    'working_dir': service_data['working_dir'],
                    'service_type': service_data.get('service_type', 'standard'),
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {service.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Already exists: {service.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Setup complete! Total services: {Service.objects.count()}')
        )
