from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class Index(TemplateView):
    success_url = reverse_lazy('main')
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        get = super().get(request, *args, **kwargs)

        if self.request.user.is_authenticated:
            return redirect("profile_main")

        return get
