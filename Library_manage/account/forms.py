from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import User, Payment, UserNote

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        required=False
    )
    role = forms.ChoiceField(choices=User.ROLES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'phone_number')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'payment_method', 'notes')

class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = ('note',) 