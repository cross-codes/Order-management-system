from django.shortcuts import render, redirect
from .forms import UserCreationFormCustom


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
