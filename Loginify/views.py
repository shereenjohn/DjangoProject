from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def hello_world(request):
    return HttpResponse("Hello, world!")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if user already exists
        if UserDetails.objects.filter(email=email).exists():
            return render(request, 'Loginify/signup.html', {'error': 'Email already exists!'})
        
        if UserDetails.objects.filter(username=username).exists():
            return render(request, 'Loginify/signup.html', {'error': 'Username already exists!'})
        
        # Create new user
        user = UserDetails.objects.create(
            username=username,
            email=email,
            password=password
        )
        
        return redirect('login')
    
    return render(request, 'Loginify/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = UserDetails.objects.get(email=email, password=password)
            return render(request, 'Loginify/success.html', {
                'message': f'Welcome back, {user.username}! You have successfully logged in.'
            })
        except UserDetails.DoesNotExist:
            return render(request, 'Loginify/login.html', {'error': 'Invalid email or password!'})
    
    return render(request, 'Loginify/login.html')


# Get all users (READ)
def get_all_users(request):
    users = UserDetails.objects.all()
    user_list = []
    for user in users:
        user_list.append({
            'username': user.username,
            'email': user.email
        })
    return JsonResponse({'users': user_list})

# Get single user by email (READ)
def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        return JsonResponse({
            'username': user.username,
            'email': user.email
        })
    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

# Update user (UPDATE)
@csrf_exempt
def update_user(request, email):
    if request.method == 'PUT':
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)
            
            # Only update password for now (safest option)
            if 'password' in data:
                user.password = data['password']
                user.save()
                return JsonResponse({
                    'message': 'Password updated successfully',
                    'username': user.username,
                    'email': user.email
                })
            else:
                return JsonResponse({'error': 'No password provided'}, status=400)
                
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Database error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Delete user (DELETE)
@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email=email)
            username = user.username
            user.delete()
            return JsonResponse({'message': f'User {username} deleted successfully'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)