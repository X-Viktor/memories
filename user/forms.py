from django import forms

from .models import Memory


class MemoryCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'max_length': 125}),
        required=True,
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
        required=True,
    )

    class Meta:
        model = Memory
        fields = ('name', 'comment')
