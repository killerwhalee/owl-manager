from django import forms

from user.models import User


class LoginForm(forms.Form):
    user_email = forms.EmailField(label="User Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password")
    confirm_password = forms.CharField(label="Confirm Password")

    class Meta:
        model = User
        fields = ["user_email"]

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
