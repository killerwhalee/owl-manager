from django import forms

from evaluate.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["name", "concept", "pros", "cons", "attack", "defense"]
