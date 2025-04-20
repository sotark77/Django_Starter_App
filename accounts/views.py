from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, CreateUserForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .token import user_tokenizer_generate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import Users
from django.core.exceptions import ValidationError


#----Login view------
def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)  # Authenticate using email
            if user is not None:  # Ensure the user exists
                login(request, user)  # Log the user in
                messages.success(request, 'Welcome back!')
                return redirect('home')  # Redirect to admin dashboard
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

#---Logout view---
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "See you soon!")
    return redirect('login')


#---Register view---
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account until it is confirmed
                user.save()

                # Send verification email
                current_site = get_current_site(request)
                subject = 'Account verification'
                message = render_to_string('accounts/registration/email-verification.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user),
                })

                user.email_user(subject=subject, message=message)
                messages.success(request, 'Registration successful! Please check your email for the verification link.')
                return redirect('email-verification-sent')

            except ValidationError as ve:
                for field, errors in ve.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            except Exception as e:
                messages.error(request, f'An unexpected error occurred during registration: {e}')
        else:
            # Display field-specific errors
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

            # Display non-field errors
            for error in form.non_field_errors():
                messages.error(request, f"Error: {error}")

    context = {'form': form}
    return render(request, 'accounts/registration/register.html', context)


#---Email verfication---
def email_verification(request, uidb64, token):
    try:
        # Decode the UID
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=unique_id)

        if user is None:
            messages.error(request, 'No user associated with this verification link.')
            return redirect('email-verification-failed')

        # Check the token
        if user_tokenizer_generate.check_token(user, token):
            if user.is_active:
                messages.info(request, 'Your account is already verified.')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Your email has been successfully verified. Your account is now active.')
            return redirect('email-verification-success')
        else:
            messages.error(request, 'The verification link is invalid or has expired. Please request a new one.')
            return redirect('email-verification-failed')

    except Users.DoesNotExist:
        messages.error(request, 'The user could not be found. Please check the verification link.')
        return redirect('email-verification-failed')
    except (TypeError, ValueError, OverflowError, ValidationError) as e:
        messages.error(request, 'There was an issue processing your verification link. Please try again.')
        # Optional: log the actual error for admin/debugging
        # logger.exception("Email verification error: %s", e)
        return redirect('email-verification-failed')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        # Optional: log the actual error
        # logger.exception("Unexpected error during email verification: %s", e)
        return redirect('email-verification-failed')


#---Email verfication sent---
def email_verification_sent(request):
    return render(request, 'accounts/registration/email-verification-sent.html')


#---Email verfication success---
def email_verification_success(request):
    return render(request, 'accounts/registration/email-verification-success.html')


#---Email verfication fail---
def email_verification_failed(request):
    return render(request, 'accounts/registration/email-verification-failed.html')

#---User profile---
@login_required(login_url='login')
def user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated")
            return redirect('home')
    else:
        user_form = UpdateUserForm(instance=request.user)

    context = {'user_form': user_form}
    return render(request, 'accounts/profile.html', context)