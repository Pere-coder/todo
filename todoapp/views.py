from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
        
    all_todos = todo.objects.filter(user = request.user)
    context = {
            'todos': all_todos
    }
        
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('todo')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if len(password) < 3:
            messages.error(request, 'password must be at least three characters')
            return redirect('register')
        
        get_all_users_by_email = User.objects.filter(email=email)
        if get_all_users_by_email:
            messages.error(request, 'email already exist')
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email,  password=password)
        new_user.save
        
        messages.success(request, 'user sucesfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('todo')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('todo')
        else:
           messages.error(request, 'user does not exist')
           return redirect('login') 
        
    return render(request, 'todoapp/login.html', {})


@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name = name)
    get_todo.delete()
    return redirect('todo')
    
@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name = name)
    get_todo.status = True
    get_todo.save()
    return redirect('todo')
    