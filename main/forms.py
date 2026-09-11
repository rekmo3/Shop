from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': "Введіть ваше ім'я",
        }),
    )
    email = forms.EmailField(
        label='Ваш email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'name@example.com',
        }),
    )
    subject = forms.CharField(
        max_length=200,
        label='Тема повідомлення',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Коротко опишіть тему звернення',
        }),
    )
    message = forms.CharField(
        label='Повідомлення',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Введіть текст повідомлення',
            'rows': 6,
        }),
    )
