from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Image

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

# @login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request,'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request,'images/create.html',{'section': 'images','form': form})



def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    return render(request,'images/detail.html',{'section': 'images',

    'image': image})