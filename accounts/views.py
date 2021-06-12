from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = "accounts/employee/register.html"
    success_url = "/"

    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/employee/register.html", {"form": form})


class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = "accounts/employer/register.html"
    success_url = "/"

    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/employer/register.html", {"form": form})


class LoginView(FormView):
    """
    Provides the ability to login as a user with an email and password
    """

    success_url = "/"
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"] != "":
            return self.request.GET["next"]
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """

    url = "/login"

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return super(LogoutView, self).get(request, *args, **kwargs)
    
    
  #reset password functionalities
def RequestResetEmail(request):

    if request.method == 'POST':
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']


            user = User.objects.filter(email=email)

            if user.exists():
                uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
                domain = get_current_site(request).domain #gives us the domain
                link = reverse('accounts:reset-password', 
                                kwargs={
                                    'uidb64':uidb64, 
                                    'token':PasswordResetTokenGenerator().make_token(user[0])
                                        })
                reset_password_url = f"http://{domain+link}"

                mail_subject = "Reset Password"

                """
                message = render_to_string('auth/activate.html', {
                    'user':user.username,
                    'url':activate_url,
                })
                """

                mail_body = f"hi {user[0].username} click the link below to reset your password\n {reset_password_url}"
                mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
                messages.success(request, "Check your Email for the reset link")
                return redirect('accounts:login')
            else:
                messages.error(request, "Sorry, there is no user with that email")
                return redirect('accounts:request-reset-email')
    form = ResetEmailForm()
    return render(request, 'accounts/reset_email_form.html', {'form':form})

def ResetPasswordView(request, uidb64, token):
    context = {
        'uidb64':uidb64, 
        'token':token
        }
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.error(request, "Opps, The link has expired")
            return render(request, 'accounts/reset_email_form.html', {})


        messages.success(request, "password changed successfully")
        return redirect('user:login')
    except DjangoUnicodeDecodeError as identifier:
        messages.error(request, "oops! something went wrong")
        return render(request, 'accounts/reset_password.html', context)


    if request.method == 'POST':
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == "":
            messages.error(request, "Password is required")
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return render(request, 'accounts/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'accounts/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'accounts/reset_password.html', context)  

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "password changed successfully")
            return redirect('user:login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "oops! something went wrong")
            return render(request, 'accounts/reset_password.html', context)
    return render(request, 'accounts/reset_password.html', context)
