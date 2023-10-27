from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from fuzzywuzzy import fuzz
from .models import Order
from .forms import UpdateOrder, OrderSearchForm


@login_required
def create_order(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        date = request.POST["date"]
        pr_tag = request.POST["pr_tag"]
        order = Order(
            user=request.user, title=title, desc=desc, date=date, pr_tag=pr_tag
        )
        order.save()
        return redirect(reverse("orders:order-list"))
    return render(request, "create_order.html")


@login_required
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    search_form = OrderSearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query").lower()
        if search_query:
            orders = [
                order
                for order in orders
                if fuzz.partial_ratio(search_query, order.title.lower()) >= 75
            ]
            context = {"orders": orders, "search_form": search_form}
            return render(
                request,
                "search_results.html",
                context,
            )
    return render(
        request,
        "list_orders.html",
        {"orders": Order.objects.filter(user=request.user), "search_form": search_form},
    )


@login_required
def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user == request.user:
        order.delete()
    return redirect("orders:order-list")


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        return HttpResponseForbidden(
            "You cannot edit this order (Reason: Invalid Credentials)"
        )
    if request.method == "POST":
        form = UpdateOrder(
            request.POST,
            instance=order,
        )
        if form.is_valid():
            form.save()
            return redirect("orders:order-list")
    else:
        form = UpdateOrder(
            instance=order,
            initial={
                "title": order.title,
                "desc": order.desc,
                "date": order.date,
                "pr_tag": order.pr_tag,
            },
        )
    context = {"form": form}
    return render(request, "update_order.html", context)
