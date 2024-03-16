from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from evaluate.forms import EvaluationForm
from evaluate.models import Evaluation


@login_required(login_url="user:login")
def eval_request(request):
    context = {}

    if request.method == "POST":
        eval_form = EvaluationForm(request.POST)

        if eval_form.is_valid():
            evaluate = eval_form.save(commit=False)
            evaluate.user = request.user
            evaluate.save()

            return redirect("evaluate:index")

        context["form"] = eval_form

    return render(request, "evaluate/request.html", context=context)


@login_required(login_url="user:login")
def eval_delete(request, eval_id):
    evaluate = Evaluation.objects.get(id=eval_id)

    if request.user == evaluate.user:
        evaluate.delete()

        return redirect("evaluate:index")

    return redirect("evaluate:index")


@login_required(login_url="user:login")
def eval_index(request):
    # Check if user is staff. If so, fetch all data.
    if request.user.is_staff:
        evaluate_list = Evaluation.objects.all()
    else:
        evaluate_list = Evaluation.objects.filter(user=request.user)

    context = {"evaluate_list": evaluate_list}
    return render(request, "evaluate/index.html", context=context)
