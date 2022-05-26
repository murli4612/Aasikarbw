from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer,Vendor
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
 password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
 password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
 email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
 class Meta:
  model = User
  fields = ['username', 'email', 'password1', 'password2']
  labels = {'email': 'Email'}
  widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
 username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
 password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
 old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))
 new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
 new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
 email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
 new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
 new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['name', 'locality', 'city', 'state', 'zipcode']
    widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}),
    'state':forms.Select(attrs={'class':'form-control'}),
    'zipcode':forms.NumberInput(attrs={'class':'form-control'})}

class VenderRegistrationForm(forms.ModelForm):
    User_name = forms.CharField(label=_('Username'),
                                error_messages={'required': _('Username is Required'),
                                                'invalid': _('This value must contain only letters, numbers and underscores.')}, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    First_name = forms.CharField(label=_('First Name'), required=True,
                                 error_messages={'required': _('First Name is Required'),
                                                 'invalid': _('This value must contain only letters')},
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    Last_name = forms.CharField(label=_('Last Name'), required=False,
                                error_messages={'required': _('Last Name is Required'),
                                                'invalid': _('This value must contain only letters')},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('Email'), required=True,
                           error_messages={'required': _('Email is Required'),
                                           'invalid': _('This value must contain email type')},
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label=_('Phone'), required=True,
                            error_messages={'required': _('Phone is Required'),
                                            'invalid': _('This value must contain only numbers')},
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))

    state = forms.CharField(label=_('State'), required=True,
                            error_messages={'required': _('State is Required'),
                                            'invalid': _('This value must contain only number and character')},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label=_('City'), required=True,
                            error_messages={'required': _('city is Required'),
                                            'invalid': _('This value must contain only number and character')},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    locality = forms.CharField(label=_('Locality'), required=True,
                            error_messages={'required': _('Stae is Required'),
                                            'invalid': _('This value must contain only number and character')},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(label=_('Pin'), required=True,
                          error_messages={'required': _('Personal ID is Required'),
                                          'invalid': _('Enter Valid ID, This value must contain only numbers')},
                          widget=forms.NumberInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
                               error_messages={'required': _('Password is Required'),
                                               'invalid': _('This value must contain only letters, numbers and underscores.')})
    conform_password = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
                                       error_messages={'required': _('Confirm Password is Required'),
                                                       'invalid': _('This value must contain only letters, numbers and underscores.')})




    class Meta:
        model = Vendor
        fields = ('User_name', 'First_name', 'Last_name', 'email', 'phone', 'state', 'city', 'locality',
                  'zipcode', 'password', 'conform_password',)

    def clean_User_name(self):
        username = self.cleaned_data.get('User_name')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_('Username already exists, Please enter other username'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            Vendor.objects.get(email=email)
        except Vendor.DoesNotExist:
            return email
        raise forms.ValidationError(_('Email Already exists!, Please enter other Email'))

    def clean_zip_code(self):
        pin = self.cleaned_data.get('pin')
        if not isinstance(pin, int) and len(pin) < 11:
            raise forms.ValidationError(_('Personal ID is Wrong, This value must contain only numbers'))
        try:
            Vendor.objects.get(pin=pin)
        except Vendor.DoesNotExist:
            return pin
        raise forms.ValidationError(_('Personal ID Already exists!, Please enter valid Personal ID'))



    def clean(self):
        if not self.cleaned_data.get('password') or not self.cleaned_data.get('conform_password'):
            raise forms.ValidationError(_('Password does not match.'))
        if self.cleaned_data.get('password') != self.cleaned_data.get('conform_password'):
            raise forms.ValidationError(_('Password does not match the conform password.'))
        return self.cleaned_data