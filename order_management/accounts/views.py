from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserCreationFormCustom, UserUpdationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationFormCustom(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        print(form.errors)
    else:
        form = UserCreationFormCustom()
    context = {"form": form}
    return render(request, "signup.html", context)


@login_required
def update_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user != request.user:
        return HttpResponseForbidden(
            "You cannot edit this user (Reason: Invalid credentials)"
        )

    if request.method == "POST":
        form = UserUpdationForm(
            request.POST,
            instance=user,
        )
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserUpdationForm(
            instance=user,
            initial={
                "First Name": user.first_name,
                "Last Name": user.last_name,
                "Email": user.email,
            },
        )
    context = {"form": form}
    return render(request, "update_user.html", context)


@login_required
def remove_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        user.delete()
    return redirect("home")
