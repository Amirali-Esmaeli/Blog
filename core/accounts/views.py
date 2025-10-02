from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.


class RegisterPage(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("blog:post-list")
        return super(RegisterPage, self).get(*args, **kwargs)
