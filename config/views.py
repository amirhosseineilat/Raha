from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'pages/landing.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


