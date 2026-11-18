
from django.views.generic import FormView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import (
    UserNotificationSettings,
    NotificationPreference,
    NotificationLog,
)
from .forms import (
    UserNotificationSettingsForm,
    NotificationPreferenceForm,
)


class NotificationSettingsView(LoginRequiredMixin, FormView):
    template_name = "notifications/settings.html"
    form_class = UserNotificationSettingsForm
    success_url = reverse_lazy("notification_settings")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        settings, created = UserNotificationSettings.objects.get_or_create(
            user=self.request.user
        )

        kwargs["instance"] = settings
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NotificationPreferenceListView(LoginRequiredMixin, ListView):
    model = NotificationPreference
    template_name = "notifications/preference_list.html"
    context_object_name = "preferences"

    def get_queryset(self):
        return NotificationPreference.objects.filter(
            user=self.request.user
        ).order_by("notification_type")


class NotificationPreferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = NotificationPreference
    form_class = NotificationPreferenceForm
    template_name = "notifications/preference_form.html"
    success_url = reverse_lazy("notification_preferences")

    def get_queryset(self):
        return NotificationPreference.objects.filter(
            user=self.request.user
        )


class NotificationLogListView(LoginRequiredMixin, ListView):
    model = NotificationLog
    template_name = "notifications/notification_log.html"
    context_object_name = "notification_logs"
    paginate_by = 20

    def get_queryset(self):
        return (
            NotificationLog.objects.filter(user=self.request.user)
            .order_by("-scheduled_for")
        )
