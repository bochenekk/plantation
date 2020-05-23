from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .models import Category, Plant, Room, UserPlant
from .serializers import (
    CategorySerializer,
    AdminCategorySerializer,
    RoomSerializer,
    PlantSerializer,
    UserPlantSerializer,
    UserSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):  # 1
    # queryset = Category.objects.filter(user=self.request.user)
    # gdyby ta metoda zostałaby wywołana przed wstaniem serwera,
    # to nie moglibyśmy mieć dostępu do żądania użytkownika!
    # nie da się sprawdzić statusu/żądania użytkownika zanim wstanie serwer!

    # serializer_class = CategorySerializer  # 2
    lookup_field = 'slug'

    def get_serializer_class(self):  # żeby admin miał dostęp do pola
        # pola user ale user nie
        if self.request.user.is_superuser:
            return AdminCategorySerializer
        return CategorySerializer

    def get_queryset(self):  # 3 ale deklaracja metody się nie wykona
        # w trakcie czytania pliku
        if self.request.user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)
        # to się nie wykonuje na etapie startu serwera


class RoomViewSet(viewsets.ModelViewSet):  # 4...
    serializer_class = RoomSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(user=self.request.user)


class PlantViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Plant.objects.all()
        return Plant.objects.filter(user=self.request.user)


class UserPlantViewSet(viewsets.ModelViewSet):
    serializer_class = UserPlantSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserPlant.objects.all()
        return UserPlant.objects.filter(user=self.request.user)


class ProfileRetrieveView(RetrieveAPIView):
    def retrieve(self, request, pk=None):
        User = get_user_model()
        serializer = UserSerializer(User.objects.get(pk=request.user.pk))
        return Response(serializer.data)
