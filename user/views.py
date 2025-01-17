from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Plan
from .serializers import UserSerializer, PlanSerializer


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

from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

@api_view(['POST'])
def choose_plan(request):
    dob = request.data.get('dob')

    if dob is None:
        return Response(data={'message': 'Date of birth is required'}, status=400)

    try:
        dob = datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        return Response(data={'message': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    days = (today - dob).days
    year = today.year

    plans = Plan.objects.filter(
        from_date__lte=today,
        to_date__gte=today,
        days__lte=days,
        year__lte=year
    )

    if not plans.exists():
        return Response(data={'message': 'No plans available'}, status=404)

    plan = plans.first().plan_type

    return Response(data={'plan': plan}, status=200)

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def query_plans(request):
    age = request.data.get('age')
    days = request.data.get('days')
    year = request.data.get('year')

    if age is None:
        return Response(data={'message': 'Age is required'}, status=400)

    try:
        age = int(age)
    except ValueError:
        return Response(data={'message': 'Invalid age format'}, status=400)

    if days is not None:
        try:
            days = int(days)
        except ValueError:
            return Response(data={'message': 'Invalid days format'}, status=400)

    if year is not None:
        try:
            year = int(year)
        except ValueError:
            return Response(data={'message': 'Invalid year format'}, status=400)

    plans = []

    if age < 18:
        plans.append('Child Plan')
    if 18 <= age < 30:
        plans.append('Young Adult Plan')
    if 30 <= age < 60:
        plans.append('Adult Plan')
    if age >= 60:
        plans.append('Senior Plan')

    if days is not None:
        plans = [plan + f' for {days} days' for plan in plans]
    if year is not None:
        plans = [plan + f' in year {year}' for plan in plans]

    return Response(data={'plans': plans}, status=200)

@api_view(['GET'])
def get_plans(request):
    dict = request.data.get('age')
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(data=serializer.data, status=200)
