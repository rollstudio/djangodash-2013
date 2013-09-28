from django import forms


class GeneratorForm(forms.Form):
    def __init__(self, cookie, *args, **kwargs):
        self.cookie = cookie

        super(GeneratorForm, self).__init__(*args, **kwargs)

        for question in cookie.questions:
            c = forms.CharField(label=question, widget=forms.TextInput(attrs={
                'placeholder': question.default
            }))

            self.fields[question.name] = c

