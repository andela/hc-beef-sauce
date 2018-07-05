from django import forms
from hc.api.models import Check

class LowercaseEmailField(forms.EmailField):

    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class EmailPasswordForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField(required=False)


class ReportSettingsForm(forms.Form):
    reports_allowed = forms.BooleanField(required=False)


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    """Represents invite member form."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        
        choices = list()
        for check in Check.objects.filter(user=self.request.user):
            choices.append((check.name, check.code))
        super(InviteTeamMemberForm, self).__init__(*args, **kwargs)
        self.fields['checks'] = forms.MultipleChoiceField(choices=choices)
    
    email = LowercaseEmailField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)
