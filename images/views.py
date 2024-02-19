from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Image


# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
PageNotAnInteger
from actions.utils import create_action

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
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


from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
                response = {'status': 'ok'}
            else:
                
                image.users_like.remove(request.user)
                create_action(request.user, 'Unlikes', image)
                response = {'status': 'ok'}
        except Image.DoesNotExist:
            response = {'message': 'id and action missisng'}
    return JsonResponse(response)



@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page')
    print("page",page)
    images_only = request.GET.get('images_only')
    print("images_only",images_only)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
    images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request,'images/list_images.html',{'section': 'images',
        'images': images})

    return render(request,'images/list.html',{'section': 'images',
    'images': images})


