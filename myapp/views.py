# myapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import  RefactoringTask, UploadedFile
from .forms import RefactoringTaskForm
from .forms import UploadCodeForm  # Ensure you have this imports
from django.contrib.auth.decorators import login_required  # If you want to require users to be logged in
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import UploadCodeForm
from django.contrib import messages
from subprocess import Popen, PIPE
import subprocess
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.views.decorators.http import require_http_methods
import json
import tempfile
import sys







 ##############################################################################################

@login_required
def add_task(request):
    if request.method == 'POST':
        form = RefactoringTaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = RefactoringTaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def list_tasks(request):
    tasks = RefactoringTask.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(RefactoringTask, id=task_id)
    
    # Only get files uploaded by the current user for this task, ordered by the upload date
    uploaded_files = task.uploaded_files.filter(user=request.user).order_by('uploaded_at') 

    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(
                file=request.FILES['file'],
                RefactoringTask=task,
                user=request.user
            )
            uploaded_file.save()
            # Redirect to the same page to show the updated file list
            return redirect('task_detail', task_id=task.id)
    else:
        form = UploadCodeForm()

    # Pass the uploaded_files filtered by the current user to the template
    return render(request, 'task_detail.html', {'task': task, 'form': form, 'uploaded_files': uploaded_files})

@login_required
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registering
            return redirect('index')  # Redirect to a home page or other appropriate page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



# Set up Django's logging system to capture information about failures
logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["POST"])  # Ensure this endpoint only allows POST requests
def run_code(request, task_id):
    # Log the raw request body for debugging purposes
    logger.info(f"Received run_code request for task_id: {task_id} with body: {request.body}")

    try:
        # Decode request body assuming it is JSON
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        # If there's an error decoding the JSON, log it and return a bad request response
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({"error": "Invalid JSON data."}, status=400)

    # Extract 'code' from JSON data
    code = data.get('code')
    if not code:
        error_msg = "No code provided in the POST request."
        logger.error(error_msg)
        return JsonResponse({"error": error_msg}, status=400)


    #tests

   # Path k adresáru s testami
    host_tests_dir = 'C:/Users/samxk/PycharmProjects/BP/test_directory'
    
    # Získanie dočasného adresára pre systém
    temp_dir = tempfile.gettempdir() 
    # Názov dočasného súboru pre kód užívateľa
    temp_code_file_name = f'temp_code_{task_id}.py' 
    # Cesta k dočasnému súboru v adresári s testami
    temp_code_file_path = os.path.join(host_tests_dir, temp_code_file_name) 
    
    # Execute the code
    try:
        
        # Uložíme kód do dočasného súboru
        with open(temp_code_file_path, 'w') as temp_file:
            temp_file.write(code)
        logger.info(f"Temporary code file created at {temp_code_file_path}.")


        # Vytvoríme Docker kontajner a spustíme skript
        docker_command = [
            'docker', 'run',
            '-v', f"{host_tests_dir}:/usr/src/app",  # adresár /tmp k pracovnému adresáru kontajnera
            'python-runner', 
            'python', f'/usr/src/app/{temp_code_file_name}'
        ]
        result = subprocess.run(
            docker_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        temp_code_file_name = f'temp_code_{task_id}.py'
        test_pattern = f'tests_task_{task_id}*.py'  # Pattern pre hľadanie testov relevantných k task_id

         # Po vykonaní kódu spustíme unit testy
        docker_command_test = [
            'docker', 'run',
            '-v', f"{host_tests_dir}:/tests",
            'python-runner', 
            'python', '-m', 'unittest', 'discover', '/tests', test_pattern
        ]
        

        test_result = subprocess.run(
            docker_command_test,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60  # Dlhší časový limit pre testy
        )

        # Zaznamenáme výsledky testov
        logger.info(f"Tests executed with stdout: {test_result.stdout}")
        if test_result.stderr:
            logger.error(f"Tests executed with stderr: {test_result.stderr}")

        # Odstránenie dočasného súboru
        #os.remove(temp_code_file_path)
        logger.info(f"Temporary code file {temp_code_file_name} removed.")

        # Log the output and any errors
        logger.info(f"Code executed with stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"Code executed with stderr: {result.stderr}")
        output = result.stdout
        errors = result.stderr

        if output:
            print(output)  # Toto sa zaloguje do Docker logov
        if errors:
            print(errors, file=sys.stderr)  # Chyby sa zalogujú ako štandardný chybový výstup

        # Return the response
        return JsonResponse({
            "code_stdout": result.stdout,
            "code_stderr": result.stderr,
            "code_returncode": result.returncode,
            "test_stdout": test_result.stdout,
            "test_stderr": test_result.stderr,
            "test_returncode": test_result.returncode
        })

    except subprocess.TimeoutExpired as e:
        logger.error(f"Code execution exceeded time limit: {e}")
        return JsonResponse({"error": "Execution time exceeded limit."}, status=408)

    except Exception as e:
        logger.exception("An error occurred during code execution.")
        return JsonResponse({"error": str(e)}, status=500)
    

    