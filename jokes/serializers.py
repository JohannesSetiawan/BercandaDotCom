from rest_framework import serializers
from .models import Jokes, AppUser

class JokesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]
    
    class Meta:
        model = Jokes
        fields = ['id','joke', 'creator', 'categories']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'api_keys']