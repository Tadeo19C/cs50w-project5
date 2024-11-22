from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

'''
    --> It is used to create form Based On Room Model(Database)

    --> model = Room ( From Which Model Do You Want to Create Form)

    --> fields = '__all__' ( Which Column Do you want to add in Form)

        --> We can specify column_name like below 

        --> fields = ['column_name1', 'column_name1','column_name1','column_name1']
                
    --> exclude = ['host', 'participants'] (Which Column Do you Want to exclude in All Columns(__all__))

'''
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2']
