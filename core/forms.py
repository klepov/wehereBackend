from django import forms

class Login(forms.Form):
    login = forms.CharField(label='username', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password:'}))

class Reg_base(forms.Form):
    login = forms.CharField(required=True,label='username',
                            max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password:'}))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Retry password:'}))

    class Meta:
        abstract = True

class Reg(Reg_base):
    pass

class Reg_child(Reg_base):

    name_child = forms.CharField(required=True,label='name child',
                                 max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'name child'}))
