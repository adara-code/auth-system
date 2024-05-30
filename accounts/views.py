from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import UserRegistration
from .serializers import UserRegistrationSerializer




# Create your views here.
class SignUp(APIView):
    renderer_classes = [TemplateHTMLRenderer]    
    
    def get(self, request):
        form = UserRegistration()
        serializer = UserRegistrationSerializer(form)
        return Response({'serializer': serializer}, template_name='signup.html')