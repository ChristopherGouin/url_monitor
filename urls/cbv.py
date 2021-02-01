from django.urls import reverse
from django import http

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Url, UserProfile

class UrlCreateView(UserPassesTestMixin, CreateView):

    template_name = "utils/forms.html"
    model = Url
    fields= ['name', 'url', 'description', 'http_code', 'display_time', 'is_content_empty', 'ssl_expiration', 'is_auto_check', 'is_mail_report', ]

    def test_func(self):
        return self.request.user.is_authenticated

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', "Valider", css_class="btn btn-lg btn-primary btn-block"))
        return form
    
    def get_form_kwargs(self):
        kwargs = super(UrlCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Url()
        user = UserProfile.objects.get(pk = self.request.user.pk)
        kwargs['instance'].user = user
        return kwargs
    
    def get_success_url(self):
        return reverse("urls:urls_list")


class UrlUpdateView(UserPassesTestMixin, UpdateView):

    template_name = "utils/forms.html"
    model = Url
    fields= ['name', 'url', 'description', 'http_code', 'display_time', 'is_content_empty', 'ssl_expiration', 'is_auto_check', 'is_mail_report', ]

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.is_authenticated and self.object.user == self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', "Valider", css_class="btn btn-lg btn-primary btn-block"))
        return form
    
    def get_success_url(self):
        return reverse("urls:urls_list")


class UrlDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "utils/delete_view.html"
    model = Url

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.is_authenticated and self.object.user == self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden('Cannot delete this url')
    
    def get_success_url(self):
        return reverse("urls:urls_list")