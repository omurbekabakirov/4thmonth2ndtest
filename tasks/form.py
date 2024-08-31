from django import forms
from tasks.models import Category


class SearchForm(forms.Form):
    search = forms.CharField(required=False,
                             max_length=100,
                             min_length=1,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'Search'}
                             ))
    tag = forms.ModelMultipleChoiceField(
        required=False, queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    orderings = (
        ('title', 'title'),
        ('-title', 'title(in backwards)'),
    )
    ordering = forms.ChoiceField(choices=orderings,
                                 required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'})
                                 )


class TaskForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
