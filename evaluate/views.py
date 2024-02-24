from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from evaluate.forms import EvaluationForm


@login_required(login_url="user:login")
def eval_request(request):
    context = {}

    if request.method == "POST":
        eval_form = EvaluationForm(request.POST)

        if eval_form.is_valid():
            evaluate = eval_form.save(commit=False)
            evaluate.user = request.user
            evaluate.save()

            return redirect("evaluate:request")

        context["form"] = eval_form

    return render(request, "evaluate/request.html", context=context)
