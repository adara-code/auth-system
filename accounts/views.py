from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import UserRegistration
from .serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class SignUp(APIView):
    renderer_classes = [TemplateHTMLRenderer]  
    
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }  
    
    def get(self, request):
        form = UserRegistration()
        serializer = UserRegistrationSerializer(form)
        return Response({'serializer': serializer}, template_name='signup.html')
    
    def post(self, request):
        form_input = UserRegistrationSerializer(data=request.data)
        if form_input.is_valid():
            user_validated_input = form_input.save()
            token = SignUp.get_tokens_for_user(user_validated_input)
            token_sent = {"token": token['access']}
            username_sent = {"username":user_validated_input}
            
            response = redirect("dashboard")
            response.set_cookie(key="token", value=token_sent, httponly=True)
            response.set_cookie(key="username", value=username_sent, httponly=True)
            return response
        else:
            return Response({'serializer':form_input},template_name='signup.html')
        

class Dashboard(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]  
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # message = request.get_signed_cookie("messages")
        username = request.COOKIES['username']
        if username.isalpha():
            first_name = username
        else:
            names = username.split()    
            first_name = names[2]    
        data = {"name":first_name}
        
        return Response(data,template_name='dashboard.html')
    

class UserLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    
    def get(self, request):
        login_form = LoginSerializer()
        return Response({'serializer':login_form})
        
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user is None:
                message = {"error": "Invalid username or password"}
                return Response({'serializer':serializer, 'error': message})
            else:
                login(request, user)
                token = SignUp.get_tokens_for_user(user)
                token_sent = {"token": token['access']}
                full_name = str(user).split()
                first_name = full_name[0]
                
                response = redirect("dashboard")
                response.set_cookie(key="token", value=token_sent, httponly=True)
                response.set_cookie(key="username", value=first_name, httponly=True)
                return response
            
        return Response({'serializer': serializer})
       
    
class UserLogout(APIView):
    def post(self, request):
        response = redirect("login")
        response.delete_cookie('token')
        response.delete_cookie('username')
        
        logout(request)
        
        return response



class ResetPassword(APIView):
    ...
