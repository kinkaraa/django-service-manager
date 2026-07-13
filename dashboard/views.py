import os
import signal
import subprocess

import psutil
from django.shortcuts import get_object_or_404, redirect, render

from .models import Service


def home(request):
    services = Service.objects.all()
    
    running_count = 0
    stopped_count = 0
    
    # Update status untuk setiap service
    for service in services:
        # Check if running based on service type
        is_running = service.is_running()
        
        if is_running:
            running_count += 1
            # Update PID to 1 for docker services if they're running but no PID
            if service.service_type == 'docker' and not service.pid:
                service.pid = 1  # Placeholder PID for display
                service.save()
        else:
            stopped_count += 1
            # Clear PID if not running
            if service.pid:
                service.pid = None
                service.save()

    return render(request, 'dashboard/home.html', {
        'services': services,
        'running_count': running_count,
        'stopped_count': stopped_count,
    })


def start_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Cek kalau sudah running
    if service.is_running():
        return redirect('/')

    # Expand ~ ke home directory
    working_dir = os.path.expanduser(service.working_dir)
    
    # Setup log file
    log_path = service.get_log_path()
    log_file = open(log_path, 'a')
    service.log_file = log_path
    
    process = subprocess.Popen(
        service.command,
        shell=True,
        cwd=working_dir,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid  # Create new process group
    )

    # For docker services, use placeholder PID since the command will exit quickly
    if service.service_type == 'docker':
        service.pid = 1  # Placeholder
    else:
        service.pid = process.pid
    
    service.save()

    return redirect('/')


def stop_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if service.service_type == 'docker':
        # For docker services, run docker-compose down
        working_dir = os.path.expanduser(service.working_dir)
        try:
            subprocess.run(
                ['docker-compose', 'down'],
                cwd=working_dir,
                capture_output=True
            )
        except:
            pass
    else:
        # For standard processes, kill the process tree
        if service.pid and psutil.pid_exists(service.pid):
            try:
                parent = psutil.Process(service.pid)
                # Kill child processes juga
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                parent.terminate()
                
                # Wait for process to terminate
                psutil.wait_procs([parent] + children, timeout=3)
            except:
                pass

    service.pid = None
    service.log_file = None
    service.save()

    return redirect('/')


def restart_service(request, service_id):
    stop_service(request, service_id)
    return start_service(request, service_id)


def start_all_services(request):
    services = Service.objects.all()

    for service in services:
        # Skip kalau sudah running
        if service.is_running():
            continue
        
        # Expand ~ ke home directory
        working_dir = os.path.expanduser(service.working_dir)
        
        # Setup log file
        log_path = service.get_log_path()
        log_file = open(log_path, 'a')
        service.log_file = log_path
            
        process = subprocess.Popen(
            service.command,
            shell=True,
            cwd=working_dir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid
        )

        # For docker services, use placeholder PID
        if service.service_type == 'docker':
            service.pid = 1  # Placeholder
        else:
            service.pid = process.pid
            
        service.save()

    return redirect('/')


def stop_all_services(request):
    services = Service.objects.all()

    for service in services:
        if service.service_type == 'docker':
            # For docker services, run docker-compose down
            working_dir = os.path.expanduser(service.working_dir)
            try:
                subprocess.run(
                    ['docker-compose', 'down'],
                    cwd=working_dir,
                    capture_output=True
                )
            except:
                pass
        else:
            # For standard processes
            if service.pid and psutil.pid_exists(service.pid):
                try:
                    parent = psutil.Process(service.pid)
                    children = parent.children(recursive=True)
                    for child in children:
                        child.terminate()
                    parent.terminate()
                    
                    psutil.wait_procs([parent] + children, timeout=3)
                except:
                    pass

        service.pid = None
        service.log_file = None
        service.save()

    return redirect('/')


def view_logs(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    logs = ""
    log_path = service.get_log_path()
    
    if os.path.exists(log_path):
        try:
            # For docker services, try to get docker-compose logs instead
            if service.service_type == 'docker':
                working_dir = os.path.expanduser(service.working_dir)
                
                # Try docker-compose logs
                try:
                    result = subprocess.run(
                        ['docker-compose', 'logs', '--tail=500'],
                        cwd=working_dir,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.stdout:
                        logs = result.stdout
                    else:
                        # Fallback to log file
                        result = subprocess.run(
                            ['tail', '-n', '1000', log_path],
                            capture_output=True,
                            text=True
                        )
                        logs = result.stdout
                except subprocess.TimeoutExpired:
                    logs = "⏱ Timeout getting docker logs. Container might still be starting..."
                except Exception as e:
                    logs = f"Unable to fetch docker logs. Check if containers are running.\nError: {str(e)}"
            else:
                # Use tail command untuk read file yang masih di-write
                result = subprocess.run(
                    ['tail', '-n', '1000', log_path],
                    capture_output=True,
                    text=True
                )
                logs = result.stdout
            
            if not logs:
                logs = "Service started, waiting for output..."
        except Exception as e:
            logs = f"Error reading log file: {str(e)}"
    else:
        if service.service_type == 'docker':
            # For docker services, try to get logs directly even if log file doesn't exist
            working_dir = os.path.expanduser(service.working_dir)
            try:
                result = subprocess.run(
                    ['docker-compose', 'logs', '--tail=500'],
                    cwd=working_dir,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                logs = result.stdout if result.stdout else "No logs available from docker-compose. Start the service first."
            except:
                logs = "No logs available yet. Start the service first."
        else:
            logs = "No logs available yet. Start the service first."
    
    return render(request, 'dashboard/logs.html', {
        'service': service,
        'logs': logs
    })


def clear_logs(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    log_path = service.get_log_path()
    
    if os.path.exists(log_path):
        open(log_path, 'w').close()
    
    return redirect(f'/logs/{service_id}/')