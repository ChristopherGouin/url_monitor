from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Verification
from urls.models import Url

@login_required
def verification_list(request, url_id):
    url = Url.objects.get(id = url_id)
    if request.user == url.user:
        verifications = Verification.objects.filter(url = url).order_by('-created', )
        return render(
            request,
            'verifications/verifications_list.html',
            {
                'verifications': verifications,
                'url': url
            }
        )
    else:
        HttpResponseRedirect(reverse('urls:urls_list'))