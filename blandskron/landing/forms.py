from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tu nombre",
            }
        ),
    )

    email = forms.EmailField(
        max_length=150,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "tu@email.com",
            }
        ),
    )

    message = forms.CharField(
        max_length=4000,
        label="Mensaje",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Cuéntame sobre tu proyecto o necesidad...",
                "rows": 4,
            }
        ),
    )
