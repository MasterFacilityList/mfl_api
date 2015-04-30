from __future__ import unicode_literals

from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class MFLAuthenticationForm(AuthenticationForm):
    """Modified to use email instead of username"""
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        print self.cleaned_data  # TODO Remove before merging!!!!!!
        return self.cleaned_data
