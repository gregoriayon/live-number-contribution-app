from django.urls import path
from app_number.views import (
    main,
    dashboard
)

app_name = "app_number"

urlpatterns = [
    path('', main, name='home'),
    path('dashboard/<str:slug>/', dashboard, name='dashboard'),
]
