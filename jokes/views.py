from django.shortcuts import render
from django.contrib.auth import authenticate
from jokes.models import AppUser, Jokes, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import JokesSerializer, UserSerializer
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string


class Register(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        print(email)
        try:
            new_user = AppUser.objects.create(username=username,password=password, email=email)
            api_keys_existed = True
            while api_keys_existed:
                api_keys = generate_random_string(60)
                if not AppUser.objects.filter(api_keys=api_keys).exists():
                    api_keys_existed=False
            new_user.api_keys = generate_random_string(15)
            new_user.save()
            serializer = UserSerializer(new_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error = str(e)
            if "UNIQUE" in error:
                return Response({'error': 'Username or email already exist!'}, status=status.HTTP_400_BAD_REQUEST)
            if "NULL" in error:
                return Response({'error': 'Some fields are empty!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class APIToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            if username is not None:
                if AppUser.objects.get(password=password) == AppUser.objects.get(username=username):
                    user = AppUser.objects.get(username=username)
                    return Response({'api_keys':user.api_keys}, status=status.HTTP_200_OK)
                else :
                    raise Exception("Username or password is wrong!")
            elif email is not None:
                if AppUser.objects.get(password=password) == AppUser.objects.get(email=email):
                    user = AppUser.objects.get(email=email)
                    return Response({'api_keys':user.api_keys}, status=status.HTTP_200_OK)
                else :
                    raise Exception("Email or password is wrong!")
            else:
                raise Exception("Some fields are empty!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Joke(APIView):
    def get(self, request):
        user = AppUser.objects.get(username='admin')
        category = Category.objects.get(name='random')
        jokes = Jokes.objects.filter(creator = user, categories=category)
        serializer = JokesSerializer(jokes, many=True)
        serialized_jokes = serializer.data
        joke = random.choice(serialized_jokes)
        return Response(joke, status=status.HTTP_200_OK)

class CreateCustomJoke(APIView):
    def post(self, request):
        api_keys = request.data.get('api_keys')
        joke = request.data.get('joke')
        categories = request.data.get('categories')
        try:
            creator = AppUser.objects.get(api_keys = api_keys)
            print(creator.id)
            new_joke = Jokes.objects.create(creator = creator,joke=joke)
            for category_name in categories:
                try:
                    category_name=category_name.lower()
                    category = Category.objects.create(name=category_name.lower())
                    category.save()
                    category = Category.objects.get(name=category_name)
                    new_joke.categories.add(category)
                except:
                    category_name=category_name.lower()
                    category = Category.objects.get(name=category_name)
                    new_joke.categories.add(category)
            new_joke.save()
            serializer = JokesSerializer(new_joke)
            serialized_jokes = serializer.data
            return Response(serialized_jokes, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetCustomJoke(APIView):
    def get(self, request, api_keys, category):
        try:
            user = AppUser.objects.get(api_keys=api_keys)
            category = Category.objects.get(name=category)
            jokes = Jokes.objects.filter(creator = user, categories=category)
            serializer = JokesSerializer(jokes, many=True)
            serialized_jokes = serializer.data
            joke = random.choice(serialized_jokes)
            return Response(joke, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCustomJoke(APIView):
    def put(self, request):
        return 'Modified Jokes'

class DeleteCustomJoke(APIView):
    def delete(self, request):
        return "Deleted Jokes"
