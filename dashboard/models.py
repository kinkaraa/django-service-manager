from django.db import models


class Service(models.Model):
    SERVICE_TYPES = [
        ('standard', 'Standard Process'),
        ('docker', 'Docker Container'),
    ]
    
    name = models.CharField(max_length=100)
    command = models.TextField()
    working_dir = models.TextField()
    pid = models.IntegerField(null=True, blank=True)
    port = models.CharField(max_length=50, null=True, blank=True, help_text="Port atau URL (opsional)")
    order = models.IntegerField(default=0, help_text="Urutan tampilan")
    log_file = models.CharField(max_length=255, null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='standard')
    docker_container_name = models.CharField(max_length=100, null=True, blank=True, help_text="Nama container untuk tracking (opsional)")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def is_running(self):
        if self.service_type == 'docker':
            # Check docker container status
            return self._check_docker_running()
        else:
            # Check PID for standard processes
            if self.pid:
                import psutil
                return psutil.pid_exists(self.pid)
        return False
    
    def _check_docker_running(self):
        """Check if docker container is running"""
        import subprocess
        try:
            # Try to get container name from command
            container_name = self.docker_container_name
            if not container_name:
                # Try to extract from working_dir or use service name
                container_name = self.name.lower().replace(' ', '-')
            
            # Check if any containers are running in this directory
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                cwd=self.working_dir if self.working_dir else None
            )
            
            # If we have container names running, consider it running
            if result.returncode == 0 and result.stdout.strip():
                return True
                
            return False
        except:
            return False
    
    def get_log_path(self):
        """Generate log file path"""
        import os
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f'service_{self.id}.log')