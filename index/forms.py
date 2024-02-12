from django import forms
from items.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in reversed(range(1, 6))], widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['rating', 'text', 'item']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # сохраняем request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.request.user  # устанавливаем пользователя
        if commit:
            instance.save()
        return instance