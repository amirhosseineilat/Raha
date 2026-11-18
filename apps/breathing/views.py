
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseBadRequest

from .models import BreathingExercise, BreathingSession


class BreathingExerciseView(ListView):
    model = BreathingExercise
    template_name = "breathing/breathing_exercise.html"
    context_object_name = "breathing_exercises"
    paginate_by = 10


class BreathingExerciseDetailView(DetailView):
    model = BreathingExercise
    template_name = "breathing/detail_breathing_exercise.html"
    context_object_name = "breathing_exercise"


class BreathingSessionStartView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user

        pk = request.POST.get("pk")
        planned_duration = request.POST.get("planned_duration")

        breathing_exercise = get_object_or_404(
            BreathingExercise,
            pk=pk,
        )

        # Validate planned duration
        try:
            planned_duration = int(planned_duration)

            if planned_duration <= 0:
                raise ValueError

        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid planned duration")

        # Check existing active session
        existing_session = BreathingSession.objects.filter(
            user=user,
            breathing_exercise=breathing_exercise,
            status=BreathingSession.Status.IN_PROGRESS,
        ).first()

        if existing_session:
            return render(
                request,
                "breathing/breathing_session_in_progress.html",
                {"session": existing_session},
            )

        # Create new session
        new_session = BreathingSession.objects.create(
            user=user,
            breathing_exercise=breathing_exercise,
            planned_duration=planned_duration,
        )

        return render(
            request,
            "breathing/breathing_session_started.html",
            {"session": new_session},
        )


class BreathingSessionFinishView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user

        session_id = request.POST.get("session_id")
        breathing_status = request.POST.get("breathing_status")

        # Find active session belonging to current user
        breathing_session = get_object_or_404(
            BreathingSession,
            pk=session_id,
            user=user,
            status=BreathingSession.Status.IN_PROGRESS,
        )

        allowed_statuses = [
            BreathingSession.Status.COMPLETED,
            BreathingSession.Status.ABANDONED,
            BreathingSession.Status.INTERRUPTED,
        ]

        if breathing_status not in allowed_statuses:
            return HttpResponseBadRequest("Invalid breathing status")

        # Calculate actual duration
        ended_at = timezone.now()

        actual_duration = int(
            (ended_at - breathing_session.started_at).total_seconds()
        )

        # Update session
        breathing_session.status = breathing_status
        breathing_session.ended_at = ended_at
        breathing_session.actual_duration = actual_duration

        breathing_session.save(
            update_fields=[
                "status",
                "ended_at",
                "actual_duration",
            ]
        )

        template_map = {
            BreathingSession.Status.COMPLETED:
                "breathing/breathing_session_completed.html",

            BreathingSession.Status.ABANDONED:
                "breathing/breathing_session_abandoned.html",

            BreathingSession.Status.INTERRUPTED:
                "breathing/breathing_session_interrupted.html",
        }

        return render(
            request,
            template_map[breathing_status],
            {"session": breathing_session},
        )


class BreathingSessionFeedbackView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user

        session_id = request.POST.get("session_id")
        feedback = request.POST.get("feedback")
        feedback_note = request.POST.get("feedback_note", "").strip()

        # Find completed session belonging to current user
        breathing_session = get_object_or_404(
            BreathingSession,
            pk=session_id,
            user=user,
            status=BreathingSession.Status.COMPLETED,
        )

        # Validate feedback
        if feedback not in BreathingSession.Feedback.values:
            return HttpResponseBadRequest("Invalid feedback")

        # Save feedback
        breathing_session.feedback = feedback
        breathing_session.feedback_note = feedback_note

        breathing_session.save(
            update_fields=[
                "feedback",
                "feedback_note",
            ]
        )

        return render(
            request,
            "breathing/breathing_session_feedback_saved.html",
            {"session": breathing_session},
        )


class BreathingSessionListView(LoginRequiredMixin, ListView):
    model = BreathingSession
    template_name = "breathing/breathing_session_list.html"
    context_object_name = "breathing_sessions"
    paginate_by = 10

    def get_queryset(self):
        return (
            BreathingSession.objects.filter(user=self.request.user)
            .select_related("breathing_exercise")
            .order_by("-started_at")
        )
