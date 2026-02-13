from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # O Django já fornece: id, username, email, password, first_name, last_name
    # Adicionamos 'name' para ser o "Nome de Exibição" (Display Name) do X
    name = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Sistema de Seguidores:
    # symmetrical=False permite que eu siga você sem você me seguir de volta
    following = models.ManyToManyField(
        "self", 
        symmetrical=False, 
        related_name="followers", 
        blank=True
    )

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280, blank=True)
    midia = models.FileField(upload_to='posts/', null=True, blank=True)
    creation_at = models.DateTimeField(auto_now_add=True)
    
    # Relacionamento para Likes
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    
    # Se 'parent' estiver preenchido, o post é um comentário de outro post
    parent = models.ForeignKey(
        "self", 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="replies"
    )

    class Meta:
        ordering = ['-creation_at'] # Posts mais recentes no topo

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."
    