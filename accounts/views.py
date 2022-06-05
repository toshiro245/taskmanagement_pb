from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView, LogoutView,PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)

from .forms import (
    UserCreationForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, 
    UserEditForm
)

from taskmanagement.models import Memo



User = get_user_model()


class UserRegistView(CreateView):
    template_name = 'accounts/user_regist.html'
    form_class = UserCreationForm


    def form_valid(self, form):
        try:
            user = form.save()
        except ValidationError as e:
            form.add_error('password', e)
            return render(self.request, 'accounts/user_regist.html', context={
                'form': form
            })

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk), 
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/regist/subject.txt', context)
        message = render_to_string('accounts/mail_template/regist/message.txt', context)
        from_email = settings.DEFAULT_FROM_EMAIL

        user.email_user(subject, message, from_email)
        return redirect('accounts:user_create_done')

        

class UserCreateDoneView(TemplateView):
    template_name = 'accounts/user_create_done.html'


class UserCreateComplateView(TemplateView):
    template_name = 'accounts/user_create_complate.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*1)

    def get(self, request, **kwargs):
        error_message = []
        token = kwargs.get('token')

        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        
        except SignatureExpired:
            error_message.append('Expired. Please sign up again.')
        
        except BadSignature:
            error_message.append('Wrong URL. Please confirm your URL.')

        else:
            user = User.objects.get(pk=user_pk)
            if user:
                user.is_active = True
                user.save()
                Memo.objects.create(
                    memo=None,
                    user=user,
                )
                return super().get(request, **kwargs)
        
        return render(request, 'accounts/user_create_failed.html', context={
            'error_message': error_message,
        })


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/user_password_reset.html'
    form_class = UserPasswordResetForm
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    success_url = reverse_lazy('accounts:user_password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/user_password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/user_password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('accounts:user_password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/user_password_reset_complete.html'


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_edit.html'
    model = User
    form_class = UserEditForm


    def form_valid(self,form):
        messages.success(self.request, 'Update successfully done.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:user_edit', kwargs={'pk': self.request.user.id})