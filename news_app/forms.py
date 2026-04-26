from django import forms
from django.core.exceptions import ValidationError


class NewsForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Заголовок",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок новости'
        })
    )

    summary = forms.CharField(
        max_length=200,
        label="Краткое описание",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Краткое описание новости'
        })
    )

    content = forms.CharField(
        label="Текст новости",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Полный текст новости'
        })
    )

    date = forms.DateField(
        label="Дата публикации",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Заголовок должен содержать минимум 3 символа')
        return title

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) < 5:
            raise ValidationError('Краткое описание должно содержать минимум 5 символов')
        return summary

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise ValidationError('Текст новости должен содержать минимум 10 символов')
        return content