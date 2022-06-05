from django.urls import path

from .views import (
    UserPasswordResetDoneView, UserRegistView, UserCreateDoneView, UserCreateComplateView, UserLoginView,
    UserLogoutView, UserPasswordResetView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, 
    UserEditView
)

app_name = 'accounts'

urlpatterns = [
    path('user_regist', UserRegistView.as_view(), name='user_regist'),
    path('user_create_done', UserCreateDoneView.as_view(), name='user_create_done'),
    path('user_create_complete/<token>', UserCreateComplateView.as_view(), name='user_create_complete'),
    path('user_login', UserLoginView.as_view(), name='user_login'),
    path('user_logout', UserLogoutView.as_view(), name='user_logout'),
    path('user_password_reset', UserPasswordResetView.as_view(), name='user_password_reset'),
    path('user_password_reset_done', UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('user_password_reset_confirm/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='user_password_reset_confirm'),
    path('user_password_reset_complete', UserPasswordResetCompleteView.as_view(), name='user_password_reset_complete'),
    path('user_edit/<int:pk>', UserEditView.as_view(), name='user_edit'),
]
