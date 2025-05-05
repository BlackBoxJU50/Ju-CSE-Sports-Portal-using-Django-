from django.shortcuts import render, redirect
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from .models import (
    BadmintonPlayer,
    CricketPlayer,
    FootballPlayer,
    BadmintonManager,
    CricketManager,
    FootballManager,
    Fixture
)
from django.contrib.auth.models import User


# Registration Views for Players



class RegisterPlayerView(APIView):
    def post(self, request):
        game = request.data.get('game_name')
        username = request.data.get('user')
        team_name = request.data.get('team_name')
        email = request.data.get('email')

        # Create the user if it doesn't exist
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password("defaultpassword")  # Optional: Set a default password
            user.save()

        try:
            if game == "Badminton":
                BadmintonPlayer.objects.update_or_create(
                    user=user,
                    defaults={'team_name': team_name, 'email': email}
                )
            elif game == "Cricket":
                CricketPlayer.objects.update_or_create(
                    user=user,
                    defaults={'team_name': team_name, 'email': email}
                )
            elif game == "Football":
                FootballPlayer.objects.update_or_create(
                    user=user,
                    defaults={'team_name': team_name, 'email': email}
                )
            else:
                return Response({'error': 'Invalid game name.'}, status=HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': f"Player for user '{username}' already exists."}, status=HTTP_400_BAD_REQUEST)

        return Response({'message': f"Player registered successfully for {game}."}, status=HTTP_201_CREATED)

# Registration Views for Managers
from .models import Game

class RegisterManagerView(APIView):
    def post(self, request):
        game_name = request.data.get('game_name')
        username = request.data.get('user')
        team_name = request.data.get('team_name')

        # Ensure game exists in Game model
        game, created = Game.objects.get_or_create(name=game_name)

        # Create or retrieve user
        user, _ = User.objects.get_or_create(username=username)
        user.set_password("defaultpassword")  # Optional: Set a password
        user.save()

        # Check if the manager already exists for this team
        if BadmintonManager.objects.filter(team_name=team_name).exists() or \
           CricketManager.objects.filter(team_name=team_name).exists() or \
           FootballManager.objects.filter(team_name=team_name).exists():
            return Response({'error': f"A manager for '{team_name}' already exists."}, status=HTTP_400_BAD_REQUEST)

        # Register manager and update game registration count
        if game_name == "Badminton":
            BadmintonManager.objects.create(user=user, team_name=team_name)
        elif game_name == "Cricket":
            CricketManager.objects.create(user=user, team_name=team_name)
        elif game_name == "Football":
            FootballManager.objects.create(user=user, team_name=team_name)
        else:
            return Response({'error': 'Invalid game name.'}, status=HTTP_400_BAD_REQUEST)

        # Increment the team count for the game
        game.team_count += 1
        game.save()

        return Response({'message': f"Manager registered successfully for {game_name}. Total teams: {game.team_count}."}, status=HTTP_201_CREATED)

# View for Fetching Fixtures and Associated Players/Managers
def fixture_view(request):
    # Get the selected game from the query parameters (default to Badminton)
    selected_game = request.GET.get('game', 'Badminton')

    # Fetch players and managers based on the selected game
    if selected_game == "Badminton":
        players = BadmintonPlayer.objects.all()
        managers = BadmintonManager.objects.all()
    elif selected_game == "Cricket":
        players = CricketPlayer.objects.all()
        managers = CricketManager.objects.all()
    elif selected_game == "Football":
        players = FootballPlayer.objects.all()
        managers = FootballManager.objects.all()
    else:
        players = []
        managers = []

    # Fetch fixtures for the selected game
    fixtures = Fixture.objects.filter(game=selected_game)

    context = {
        'game': selected_game,
        'fixtures': fixtures,
        'players': players,
        'managers': managers,
    }
    return render(request, 'fixtures.html', context)
# View for Registration Page
def registration_view(request):
    return render(request, 'registration.html')


# View for Home Page
def home_view(request):
    games = Game.objects.all()  # Fetch all registered games
    return render(request, 'home.html', {'games': games})
