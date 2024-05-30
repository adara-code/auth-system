from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserRegistration
import re


class UserRegistrationSerializer(ModelSerializer):
    email = serializers.EmailField(
        label = "",
        style={'placeholder': "Email"},
    )
    full_name = serializers.CharField(
        label = "",
        style={'placeholder': "Full Name"},
    )
    password = serializers.CharField(
        label = "",
        style={'placeholder': 'Password', 'input_type': 'password'},
        help_text = "Password should have a mix of letters, numbers and symbols",
        write_only = True
    )
    
    
    def validate_email(self,value):
        """
        This function compares user input with data retrieved from the database's email column. The email field has a 
        unique constraint preventing users from making multiple accounts with the same email address. If there is an
        existing email, it throws an error; otherwise, it saves to the database.
        """
        check_email_exists = UserRegistration.objects.filter(email=value)
        if check_email_exists:
            raise serializers.ValidationError("Email already exists")
        # else:
        #     new_value = value.strip().lower()
        return value.strip().lower()
    
   
    def validate_full_name(self,value):
        """
        This function looks for alphabets in the user's input using the regex pattern. Apostrophes and
        hyphens in names have been taken into consideration. An error is raised for any other input minus html elements. 
        In terms of second names, it verifies that the user entered a minimum of one to three names that correspond to the middle 
        and surnames. Additionally, at least two of the names must be written in its entirety, and not initials.
        """
        fullname = re.search('([a-zA-Z\'\-]{2,15}+)( [a-zA-Z\'\-]{2,15}+){1,3}', value)
        if fullname == None:
            raise serializers.ValidationError("Enter valid names i.e Jane Doe")
        else:
            new_value = value.strip().title()
        return new_value
    
    
    def validate_password(self, value):
        """
        This function uses the regex search function to identify the first occurence/match of the given pattern.
        It checks for password length, at least 1 occurence of small caps and full caps characters, a digit and any symbol.
        It displays a customized error message if any of the match cases equate to True (that is, no matches are found) and 
        returns the value if all the cases are found to be False.
        """
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must have at least 8 or more characters")
        elif re.search('[a-z]', value) == None:
            raise serializers.ValidationError("Password must have at least 1 or more small letters")
        elif re.search('[A-Z]',value) == None:
            raise serializers.ValidationError("Password must have at least 1 or more capital letters")
        elif re.search('[0-9]', value) == None:
            raise serializers.ValidationError("Password must have at least 1 or more numbers")
        elif re.search('[^a-zA-Z0-9]',value) == None:
            raise serializers.ValidationError("Password must have at least 1 or more symmbols")
        else:
            return value
        
    def create(self, validated_data):
        """
        This in-built function creates an instance of the validated data that's been input by the user.
        It then takes the password and calls the set_password method on it so that it can hash
        the password. The save() method will save the hashed password alongside the other validated 
        data into the database.
        """
        user = UserRegistration(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
   
    class Meta:
        model = UserRegistration
        fields = ['email','full_name','password']
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label = "",
        style={'placeholder': "Email"},)
    password = serializers.CharField(
        label = "",
        style={'placeholder': 'Password', 'input_type': 'password'},
        write_only = True
    )
    
    def validate_email(self,value):
        check_email_exists = UserRegistration.objects.filter(email=value).exists()
        if not check_email_exists:
            raise serializers.ValidationError("Email does not exist")
        return value
    
    class Meta:
        model = UserRegistration
        fields = ['email', 'password']
