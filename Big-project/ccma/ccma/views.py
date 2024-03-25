from django.shortcuts import render
from django.views.generic import TemplateView

def index(request):
    return render(request, 'index.html')

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'
    
def library_view(request):
    return render(request, 'library.html')