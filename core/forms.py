from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Listing, FIELD_CHOICES


FIELD_NAME_CHOICES = [(f[0], f[0]) for f in FIELD_CHOICES]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'نام کاربری',
        }


class ProfileForm(forms.ModelForm):
    fields = forms.MultipleChoiceField(
        choices=FIELD_NAME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='فیلدها',
    )

    class Meta:
        model = Profile
        fields = ('role', 'name', 'org', 'contact', 'bio', 'fields')
        labels = {
            'role': 'نوع کاربری',
            'name': 'نام',
            'org': 'سازمان / دانشگاه',
            'contact': 'راه تماس',
            'bio': 'درباره من',
        }


class ListingForm(forms.ModelForm):
    fields = forms.MultipleChoiceField(
        choices=FIELD_NAME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='فیلدها',
    )

    class Meta:
        model = Listing
        fields = ('title', 'org', 'extra', 'desc', 'contact', 'fields')


class ChemForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'cat', 'cas', 'grade', 'qty', 'price', 'city',
                  'desc', 'org', 'contact', 'ok')