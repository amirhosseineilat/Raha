
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Mood, MoodFactor, DailyActivity
from .forms import MoodForm


class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    template_name = "mood/mood_list.html"
    context_object_name = "moods"
    paginate_by = 10

    def get_queryset(self):
        return (
            Mood.objects.filter(user=self.request.user)
            .prefetch_related("factors", "activities")
            .order_by("-date")
        )


class MoodDetailView(LoginRequiredMixin, DetailView):
    model = Mood
    template_name = "mood/mood_detail.html"
    context_object_name = "mood"

    def get_queryset(self):
        return (
            Mood.objects.filter(user=self.request.user)
            .prefetch_related("factors", "activities")
        )


class MoodCreateView(LoginRequiredMixin, FormView):
    template_name = "mood/mood_form.html"
    form_class = MoodForm
    success_url = reverse_lazy("mood_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MoodUpdateView(LoginRequiredMixin, FormView):
    template_name = "mood/mood_form.html"
    form_class = MoodForm
    success_url = reverse_lazy("mood_list")

    def dispatch(self, request, *args, **kwargs):
        self.mood = get_object_or_404(
            Mood,
            pk=kwargs["pk"],
            user=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["instance"] = self.mood
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MoodFactorListView(LoginRequiredMixin, ListView):
    model = MoodFactor
    template_name = "mood/mood_factor_list.html"
    context_object_name = "mood_factors"

    def get_queryset(self):
        return MoodFactor.objects.filter(is_active=True)


class DailyActivityListView(LoginRequiredMixin, ListView):
    model = DailyActivity
    template_name = "mood/daily_activity_list.html"
    context_object_name = "daily_activities"

    def get_queryset(self):
        return DailyActivity.objects.filter(is_active=True)
