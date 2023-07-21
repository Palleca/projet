from django.forms import ModelForm

from .models import Formateur, Formation


class FormationForm(ModelForm):
    class Meta:
        model = Formation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = Formateur.objects.filter(formation__isnull=True)


class FormateurForm(ModelForm):
    class Meta:
        model = Formateur
        fields = '__all__'