
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum, Q, F, ExpressionWrapper, DurationField
from django.utils import timezone
from django.views.generic import TemplateView

from apps.mood.models import Mood
from apps.breathing.models import BreathingSession
from apps.audio.models import AudioSession
from apps.games.models import GameSession


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "reports/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        allowed_periods = [7, 30, 90]

        try:
            period = int(self.request.GET.get("period", 30))
        except (TypeError, ValueError):
            period = 30

        if period not in allowed_periods:
            period = 30

        now = timezone.now()
        start_datetime = now - timedelta(days=period)
        start_date = timezone.localdate() - timedelta(days=period - 1)

        context["period"] = period

        moods = Mood.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=timezone.localdate(),
        )

        context["mood_report"] = moods.aggregate(
            total_entries=Count("id"),
            average_mood=Avg("score"),
            average_stress=Avg("stress_level"),
            average_sleep=Avg("sleep_quality"),
        )

        breathing_sessions = BreathingSession.objects.filter(
            user=user,
            started_at__gte=start_datetime,
            started_at__lte=now,
        )

        context["breathing_report"] = breathing_sessions.aggregate(
            total_sessions=Count("id"),
            completed_sessions=Count(
                "id",
                filter=Q(status=BreathingSession.Status.COMPLETED),
            ),
            total_duration=Sum(
                "actual_duration",
                filter=Q(status=BreathingSession.Status.COMPLETED),
            ),
        )


        audio_sessions = AudioSession.objects.filter(
            user=user,
            started_at__gte=start_datetime,
            started_at__lte=now,
        )

        context["audio_report"] = audio_sessions.aggregate(
            total_sessions=Count("id"),
            completed_sessions=Count(
                "id",
                filter=Q(status=AudioSession.Status.COMPLETED),
            ),
        )

        game_sessions = GameSession.objects.filter(
            user=user,
            started_at__gte=start_datetime,
            started_at__lte=now,
        )

        game_duration = ExpressionWrapper(
            F("ended_at") - F("started_at"),
            output_field=DurationField(),
        )

        context["game_report"] = game_sessions.aggregate(
            total_sessions=Count("id"),
            completed_sessions=Count(
                "id",
                filter=Q(status=GameSession.Status.COMPLETED),
            ),
            total_duration=Sum(
                game_duration,
                filter=Q(ended_at__isnull=False),
            ),
        )

        return context
