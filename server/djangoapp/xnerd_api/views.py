from django.shortcuts import render

# Create your views here.
# 1. Importe o get_user_model
from django.contrib.auth import get_user_model

# 2. Defina a variável User
User = get_user_model()

from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # Aqui você associaria ao usuário logado, 
        # mas para teste vamos pegar o primeiro usuário do banco
        serializer.save(user=User.objects.first())
        