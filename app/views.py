from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

from rest_framework_simplejwt.tokens import RefreshToken

from app.task import send_welcome_email
from app.models import Message

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
def is_admin(user):
    return user.is_superuser

def home(request):
    return render(request, 'home.html')

def singup(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, 'reg.html')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'reg.html')

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            
            # Generate JWT tokens
            tokens = get_tokens_for_user(user)
            
            # Automatically log in the user after successful registration
            login(request, user)
            # Send welcome email via Celery task
            send_welcome_email.delay(email, username)
            
            messages.success(request, "Registration successful! Please log in.")
            return redirect('chat', room_name='general')

    return render(request, 'reg.html')

def singin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat', room_name='general') # Redirect to chat app URL

        messages.error(request, "Invalid username or password.")
        return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/singin/')


@login_required
def chat(request, room_name):
    # Retrieve messages for the room
    messages = Message.objects.filter(room_name=room_name, deleted=False)
    return render(request, 'chat.html', {'room_name': room_name, 'messages': messages})

@user_passes_test(is_admin)
def delete_message(request, message_id):
    # Admin deletes the message by marking it as deleted
    message = get_object_or_404(Message, id=message_id)
    message.deleted = True
    message.save()
    return redirect('chat', room_name=message.room_name)

@user_passes_test(is_admin)
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        message.content = new_content
        message.save()
        return redirect('chat', room_name=message.room_name)

    return render(request, 'edit_message.html', {'message': message})