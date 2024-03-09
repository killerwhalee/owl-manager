from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tools.forms import ImageCutterForm
from tools.utils import *


@login_required(login_url="user:login")
def index(request):
    return render(request, "tools/index.html")


@login_required(login_url="user:login")
def image_cutter(request):
    context = {}

    if request.method == "POST":
        form = ImageCutterForm(request.POST)
        
        if form.is_valid():
            file_type = form.cleaned_data["file_type"]
            file_source = form.cleaned_data["file_source"]

    return render(request, "tools/image-cutter.html")
