from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView


class Register(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/form.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)
        # return super(Login, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        # checking for email if is already taken or not
        # username is by default unique
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'That email is taken')
            return redirect('accounts:register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            user_form = UserRegistrationForm()
            return render(request, 'accounts/form.html', {'form': user_form})
