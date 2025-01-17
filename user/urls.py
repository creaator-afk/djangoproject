from django.urls import path
from .views import signup, login, choose_plan, query_plans

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('age', choose_plan),
    path('plan',query_plans)
]