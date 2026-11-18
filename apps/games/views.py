
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from .models import (
    Game,
    GameCategory,
    GameSession,
)

class GameListView(ListView):
    model = Game
    template_name = "games/game_list.html"
    context_object_name = "games"
    paginate_by = 12

    def get_queryset(self):
        return (
            Game.objects.filter(
                is_active=True,
                game_categories__is_active=True,
            )
            .prefetch_related("game_categories")
            .distinct()
            .order_by("-created_at")
        )


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Game.objects.filter(
                is_active=True,
                game_categories__is_active=True,
            )
            .prefetch_related(
                Prefetch(
                    "game_categories",
                    queryset=GameCategory.objects.filter(is_active=True),
                )
            )
            .distinct()
        )

class GameCategoryListView(ListView):
    model = GameCategory
    template_name = "games/game_category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return (
            GameCategory.objects.filter(
                is_active=True,
                games__is_active=True,
            )
            .distinct()
            .order_by("name")
        )


class GameCategoryDetailView(DetailView):
    model = GameCategory
    template_name = "games/game_category_detail.html"
    context_object_name = "category"
    pk_url_kwarg = "category_id"

    def get_queryset(self):
        return GameCategory.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["games"] = (
            Game.objects.filter(
                is_active=True,
                game_categories=self.object,
            )
            .prefetch_related("game_categories")
            .order_by("-created_at")
        )

        return context

class GameSessionStartView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game = get_object_or_404(
            Game.objects.filter(
                is_active=True,
                game_categories__is_active=True,
            ).distinct(),
            slug=kwargs["slug"],
        )

        # Get an existing active session or create a new one
        session, created = GameSession.objects.get_or_create(
            user=request.user,
            game=game,
            status=GameSession.Status.IN_PROGRESS,
        )

        # Redirect according to game type
        if game.game_type == Game.GameType.EXTERNAL:
            return HttpResponseRedirect(game.game_url)

        return redirect("game_detail", slug=game.slug)


class GameSessionFinishView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        session = get_object_or_404(
            GameSession,
            pk=request.POST.get("session_id"),
            user=request.user,
            status=GameSession.Status.IN_PROGRESS,
        )

        status = request.POST.get("status")

        allowed_statuses = [
            GameSession.Status.COMPLETED,
            GameSession.Status.ABANDONED,
            GameSession.Status.INTERRUPTED,
        ]

        if status not in allowed_statuses:
            return redirect("game_list")

        session.status = status
        session.ended_at = timezone.now()

        session.save(
            update_fields=["status", "ended_at"]
        )

        return redirect("game_list")
