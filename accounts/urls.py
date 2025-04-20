from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Authentication
    path('login/', views.auth_login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"), 
    
    
    # Email verification URLS
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name="email-verification"),
    path('email-verification-sent', views.email_verification_sent, name="email-verification-sent"),
    path('email-verification-success', views.email_verification_success, name="email-verification-success"),
    path('email-verification-failed', views.email_verification_failed, name="email-verification-failed"),
    
    #Password Reset
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset/password-reset.html"), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset/password-reset-sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset/password-reset-form.html"), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset/password-reset-complete.html"), name='password_reset_complete'),
    
    #User Profile
    path('profile/', views.user_profile, name="profile"),

]

from django.conf.urls import handler404, handler500, handler403

handler404 = 'account.views.custom_404'
handler500 = 'account.views.custom_500'
handler403 = 'account.views.custom_403'
