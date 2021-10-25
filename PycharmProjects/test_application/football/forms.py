
from django import forms

class MatchForm(forms.Form):
    matchId = forms.IntegerField()