from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player, TeamManager

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['user', 'email', 'team_name', 'game_name', 'password']
        
class TeamManagerSerializer(serializers.ModelSerializer):
    # Allow accepting a username instead of a user ID
    user = serializers.CharField()

    class Meta:
        model = TeamManager
        fields = ['user', 'team_name', 'game_name', 'password']

    def validate_user(self, value):
        from django.contrib.auth.models import User

        try:
            # Check if the user exists
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            # If the user does not exist, create a new one
            user = User.objects.create_user(username=value, password="defaultpassword")
            return user