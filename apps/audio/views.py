from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import AudioContent, AudioCategory, AudioSession
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest,HttpResponse
from django.utils import timezone

class AudioCategoryView(ListView):
    model = AudioCategory
    context_object_name = "audio_category"
    paginate_by = 10
    queryset = AudioCategory.objects.filter(is_active=True)


class AudioContentView(ListView):
    model = AudioContent
    context_object_name = "audio_content"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related("audio_category")
        category = self.request.GET.get("category")

        if category:
            queryset = queryset.filter(audio_category__name=category)

        return queryset


class AudioSessionView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user

        # Get POST data
        pk = request.POST.get("pk")
        audio_status = request.POST.get("audio_status")
        audio_position = request.POST.get("audio_position")

        # Validate audio position
        try:
            audio_position = int(audio_position)

            if audio_position < 0:
                raise ValueError

        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid audio position")

        # Get audio content
        audio_content = get_object_or_404(AudioContent, pk=pk)

        # Find latest session
        audio_session = (
            AudioSession.objects.filter(
                user=user,
                audio_content=audio_content,
            )
            .order_by("-started_at", "-pk")
            .first()
        )

        # PLAY
        if audio_status == AudioSession.Status.PLAYING:

            if audio_session is None:
                AudioSession.objects.create(
                    user=user,
                    audio_content=audio_content,
                    last_position=audio_position,
                )

            elif audio_session.status == AudioSession.Status.PAUSED:
                audio_session.status = AudioSession.Status.PLAYING
                audio_session.save(update_fields=["status"])

            elif audio_session.status in [
                AudioSession.Status.STOPPED,
                AudioSession.Status.COMPLETED,
                AudioSession.Status.INTERRUPTED,
            ]:
                AudioSession.objects.create(
                    user=user,
                    audio_content=audio_content,
                    last_position=audio_position,
                )

        # PAUSE
        elif audio_status == AudioSession.Status.PAUSED:

            if audio_session and audio_session.status == AudioSession.Status.PLAYING:
                audio_session.status = AudioSession.Status.PAUSED
                audio_session.last_position = audio_position

                audio_session.save(
                    update_fields=["status", "last_position"]
                )

        # STOP
        elif audio_status == AudioSession.Status.STOPPED:

            if audio_session and audio_session.status in [
                AudioSession.Status.PLAYING,
                AudioSession.Status.PAUSED,
            ]:
                audio_session.status = AudioSession.Status.STOPPED
                audio_session.last_position = audio_position
                audio_session.ended_at = timezone.now()

                audio_session.save(
                    update_fields=[
                        "status",
                        "last_position",
                        "ended_at",
                    ]
                )

        # COMPLETED
        elif audio_status == AudioSession.Status.COMPLETED:

            if audio_session and audio_session.status in [
                AudioSession.Status.PLAYING,
                AudioSession.Status.PAUSED,
            ]:
                audio_session.status = AudioSession.Status.COMPLETED
                audio_session.last_position = audio_position
                audio_session.ended_at = timezone.now()

                audio_session.save(
                    update_fields=[
                        "status",
                        "last_position",
                        "ended_at",
                    ]
                )

        # INTERRUPTED
        elif audio_status == AudioSession.Status.INTERRUPTED:

            if audio_session and audio_session.status in [
                AudioSession.Status.PLAYING,
                AudioSession.Status.PAUSED,
            ]:
                audio_session.status = AudioSession.Status.INTERRUPTED
                audio_session.last_position = audio_position
                audio_session.ended_at = timezone.now()

                audio_session.save(
                    update_fields=[
                        "status",
                        "last_position",
                        "ended_at",
                    ]
                )

        else:
            return HttpResponseBadRequest("Invalid audio status")

        return HttpResponse("Audio session updated successfully")