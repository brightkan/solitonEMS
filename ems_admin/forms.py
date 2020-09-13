from django.forms import ModelForm, EmailField, TextInput

from ems_auth.models import User, SolitonUser


class UserForm(ModelForm):
    email = EmailField(
        label='',
        required=True,
        widget=TextInput(attrs={'placeholder': 'Enter Email', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'is_superuser', 'is_staff', 'is_active', 'is_hr', 'is_hod', 'is_cfo', 'is_ceo',
                  'is_supervisor']


class SolitonUserForm(ModelForm):
    class Meta:
        model = SolitonUser
        fields = ['employee']


class SolitonUserEditForm(ModelForm):
    class Meta:
        model = SolitonUser
        fields = ['employee', 'user']


class EMSPermissionForm(ModelForm):
    # class Meta:
    #     model = EMSPermission
    #     fields = ['full_auth', 'view_only']
    pass
