from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import RegisterForm, LoginForm, EditProfileForm
from accounts.models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            print(f'username: {username}, password: {password}')
            new_user = CustomUser.objects.create_user(username=username, password=password)
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
            return redirect('accounts:login')
        
    return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            # user = CustomUser.objects.filter(username=username).first()
            # if user and check_password(password, user.password):
            #     messages.success(request, 'شما با موفقیت وارد شدید')

            #     return redirect('home')
            # else:
            #     messages.success(request, 'ثبت نام شما با شکست همراه شد')
            #     print('login failed')
            #     print(user.username, user.password)
            #     print(user)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید')

                return redirect('core:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'accounts/login.html', {'form':form})


def logout_view(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Display the user's profile."""
    return render(request, 'accounts/profile.html', {'profile': request.user})


@login_required
def edit_profile(request):
    """Allow the user to edit their profile."""
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'نمایه کاربری شما با موفقیت ویرایش شد.')
            return redirect('accounts:profile')
    else:
        # Prepopulate form with existing user data
        form = EditProfileForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})