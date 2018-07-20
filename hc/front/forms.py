from django import forms
from hc.api.models import Channel


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)
    department = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        tag_list = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                tag_list.append(part.lower())

        # Remove duplicate entries by converting to a set then back to  a list
        tag_list = list(set(tag_list))
        return " ".join(tag_list)

    def clean_department(self):
        """Extract list of departments from departments input field in 'update name' form"""
        dept_list = []

        for part in self.cleaned_data["department"].split(" "):
            part = part.strip()
            if part != "":
                dept_list.append(part.lower())
        
        # Remove duplicate entries by converting to a set then back to  a list
        dept_list = list(set(dept_list))
        return " ".join(dept_list)

class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=7776000)
    grace = forms.IntegerField(min_value=60, max_value=7776000)


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)


class NagUserForm(forms.Form):
    """Form to edit nag user function"""
    nag = forms.BooleanField(required=False)
