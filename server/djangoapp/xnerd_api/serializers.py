from rest_framework import serializers
from .models import User, Post

class UserMinifiedSerializer(serializers.ModelSerializer):
    """Retorna apenas o essencial para mostrar no card do Post"""
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'profile_image']


class PostSerializer(serializers.ModelSerializer):
    # Usamos o serializer acima para "aninhá-lo" aqui
    user = UserMinifiedSerializer(read_only=True)
    
    # Campos calculados (Count)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    # Verifica se o usuário logado curtiu este post (útil para pintar o coração de vermelho no React)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'content', 'midia', 
            'creation_at', 'likes_count', 'replies_count', 'is_liked'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False
