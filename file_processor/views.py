from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserLoginForm
import os
# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,get_user_model,login,logout
from .models import ProcessingLog
from .file_processing_service import process_file  # Create this service to handle processing logic

def home(request):
    return render(request, 'file_processor/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    
    return render(request, "file_processor/login.html", context)

@login_required
def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES and request.FILES['file']:
            uploaded_file = request.FILES['file']
            
            # Check that file is an Excel file (.xlsx, .xls)
            if not uploaded_file.name.endswith('.xlsx') and not uploaded_file.name.endswith('.xls'):
                return render(request, 'file_processor/upload.html')
            
            processed_file_path = process_file(uploaded_file, request.user)

            ProcessingLog.objects.create(
                user=request.user,
                file_name=uploaded_file.name,
                processed_file_path=processed_file_path
            )
            
            with open(processed_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(processed_file_path)}'
                                
                return response
        else:
            return render(request, 'file_processor/upload.html')
    
    return render(request, 'file_processor/upload.html')
