from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
import json
import os


# Create your views here.
DATA_FILE = 'data/distribution_book.json'

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as file:
        json.dump(items, file, indent=4)

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('Index')
        else:
            form = UserCreationForm()
        return render(request, 'register.html', {form})
    
# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
        return render(request, 'login.html')
    
# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Protected Index View
@login_required
def index(request):
    items = load_items()
    return render(request, 'index.html', 
                  {
                      'items': items
                      })

# Add Item View
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            items = load_items()
            items.append(form.cleaned_data)
            save_items(items)
            return redirect('index')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', 
                  {
                      'form': form
                      })

# Delete Item View
@login_required
def delete_item(request, item_id):
    items = load_items()
    if 0 <= item_id < len(items):
        del items[item_id]
        save_items(items)
    return redirect('index')

# Update Item View
@login_required
def update_item(request, item_id):
    items = load_items()
    if 0 <= item_id < len(items):
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                items[item_id] = form.cleaned_data
                save_items(items)
                return redirect('index')
        else:
            form = ItemForm()
        return render(request, 'update_item.html', 
                    {
                        'form': form, 
                        'item_id': item_id
                        })
    return redirect('index')