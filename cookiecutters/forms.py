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


class CookieCutterForm(forms.Form):

    repo_name = forms.CharField(label="Repo name")

    def __init__(self, cookie, *args, **kwargs):
        super(CookieCutterForm, self).__init__(*args, **kwargs)
        
        self.cookie = cookie
        for opt, default in cookie.options.items():
            field = forms.CharField(initial=default, required=False,
                label=opt.replace('_', ' ').capitalize())
            self.fields[opt] = field

    def clean(self):
        data = super(CookieCutterForm, self).clean()
        data.update({k: self.cookie.options.get(k)
                    for k in data if data[k] is None})
        return data

    @property
    def use_github(self):
        return '_github' in self.data
