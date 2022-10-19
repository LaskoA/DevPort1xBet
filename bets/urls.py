from django.urls import path, include
from rest_framework import routers

from .views import GameAPI

router = routers.DefaultRouter()
router.register("games", GameAPI)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'game'
