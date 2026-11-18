
from django import forms

from .models import Mood, MoodFactor, DailyActivity


class MoodForm(forms.Form):

    score = forms.IntegerField(min_value=1, max_value=5)
    stress_level = forms.IntegerField(min_value=1, max_value=5)
    sleep_quality = forms.IntegerField(min_value=1, max_value=5)

    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    factors = forms.ModelMultipleChoiceField(
        queryset=MoodFactor.objects.filter(is_active=True),
        required=False,
    )

    activities = forms.ModelMultipleChoiceField(
        queryset=DailyActivity.objects.filter(is_active=True),
        required=False,
    )

    def __init__(self, *args, user=None, instance=None, **kwargs):
        self.user = user
        self.instance = instance

        super().__init__(*args, **kwargs)

        if instance:
            self.initial.update({
                "score": instance.score,
                "stress_level": instance.stress_level,
                "sleep_quality": instance.sleep_quality,
                "description": instance.description,
                "date": instance.date,
                "factors": instance.factors.all(),
                "activities": instance.activities.all(),
            })

    def clean_date(self):
        date = self.cleaned_data["date"]

        existing_mood = Mood.objects.filter(
            user=self.user,
            date=date,
        )

        if self.instance:
            existing_mood = existing_mood.exclude(pk=self.instance.pk)

        if existing_mood.exists():
            raise forms.ValidationError(
                "You have already registered your mood for this date."
            )

        return date

    def save(self):
        mood = self.instance or Mood(user=self.user)

        mood.score = self.cleaned_data["score"]
        mood.stress_level = self.cleaned_data["stress_level"]
        mood.sleep_quality = self.cleaned_data["sleep_quality"]
        mood.description = self.cleaned_data["description"]
        mood.date = self.cleaned_data["date"]

        mood.save()

        mood.factors.set(self.cleaned_data["factors"])
        mood.activities.set(self.cleaned_data["activities"])

        return mood
