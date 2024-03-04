from django.urls import path
from .views import *

app_name = 'jokes'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('api-token/', APIToken.as_view(), name='api-token'),
    path('', Joke.as_view(), name='api-token'),
    path('custom/create', CreateCustomJoke.as_view(), name='create-custom-joke'),
    path('custom/get/<str:api_keys>/<str:category>/', GetCustomJoke.as_view(), name='get-custom-joke'),
]