from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Player, TeamManager
from .serializers import PlayerSerializer, TeamManagerSerializer

# Registration Views
class RegisterPlayerView(APIView):
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f"Player {serializer.data['user']} registered successfully!"})
        return Response(serializer.errors, status=400)

class RegisterTeamManagerView(APIView):
    def post(self, request):
        serializer = TeamManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Team Manager registered successfully!"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Guest Views
def home_view(request):
    return render(request, 'home.html')

def fixture_view(request):
    # Fetch all players and teams from the database
    boys_teams = TeamManager.objects.filter(managed_team__icontains="boys")
    girls_teams = TeamManager.objects.filter(managed_team__icontains="girls")
    players = Player.objects.all()  # Fetch all players
def fixture_view(request):
    players = Player.objects.all()
    managers = TeamManager.objects.all()

    context = {
        'players': players,
        'managers': managers,
    }
    return render(request, 'fixtures.html', context)

from django.shortcuts import render

def registration_view(request):
    # Always return the registration page, no matter if the user is authenticated or not
    return render(request, 'registration.html')

   
