from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import Url
# Create your views here.

@login_required()
def urls_list(request):
    urls = Url.objects.filter(
        user = request.user
    ).order_by(
        '-created',
    )

    return render(
        request,
        'urls/urls_list.html',
        {
            'urls': urls
        }
    )