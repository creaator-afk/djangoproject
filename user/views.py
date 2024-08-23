from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

# Create your views here.
@api_view(['GET','POST','DELETE'])
def signup(request):
    if request.method == 'POST':
        user_name = request.data.get('username')
        password = request.data.get('password')

        user = User(name=user_name, password=password)
        if(User.objects.filter(name=user_name).exists()):
            return Response(data={'message': 'User already exists'},status=400)
        
        user.save()

        return Response(data={'message': 'User created successfully'},status=201)
    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=200)
    
    if request.method == 'DELETE':
        user_name = request.data.get('username')
        user = User.objects.get(name=user_name)
        user.delete()
        return Response(data={'message': 'User deleted successfully'}, status=200)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        user_name = request.data.get('username')
        password = request.data.get('password')
        if password == User.objects.get(name=user_name).password:
            return Response(data={'message': 'User logged in'}, status=200)
        else:
            return Response(data={'message': 'Invalid credentials'}, status=401)

