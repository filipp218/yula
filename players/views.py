from django.shortcuts import render, redirect
from django.views.generic.base import View
from players.models import *
from players.forms import CommentForm
from django.db.models import Q
from django.db.models import Count

class AllPlayers(View):
    def get(self, request):
        """Все игроки"""
        empty = ''
        players = Player.objects.all()
        context = {"players":players}
        return render(request, "players/main.html" , context)

    def post(self, request):
        """Поиск игрока по фамалии и имени с учётом регистра"""
        query = request.POST['query']
        filter_players = Q()
        for word in query.split(' '):
            filter_players |= Q(name__icontains=word) | Q(lastname__icontains=word)
        players = Player.objects.filter(filter_players)
        return render(request, "players/main.html" , {"players": players, "query": query})


def get_new_visitor_id():
    """создаёт объект для нового посетителя и, чтобы добавить id к сессии куки"""
    return Visitor.objects.create().id

def log_visit(visitor_id, player_id):
    """создаёт объекты для записи visitora и игрока, чей профиль посетил"""
    return VisitHistory.objects.create(visitor_id=visitor_id, player_id=player_id).id

def unique_counts(player):
    """подсчитывает уникальных пользователей, DISTINCT не сработал с sqlite"""
    return VisitHistory.objects.filter(player=player).values('visitor').annotate(Count('player_id')).count()


class ProfilePlayer(View):
    def get(self, request, slug):
        """Страница профиля игрока"""
        if 'visitor_id' not in request.session:
            request.session['visitor_id'] = get_new_visitor_id()
        player = Player.objects.get(url=slug)
        log_visit(request.session['visitor_id'], player.id)
        unique_visits = unique_counts(player)

        comments = Comment.objects.filter(for_who=player.id)
        new_comment = CommentForm()
        context = {"player": player, "comments": comments, "new_comment": new_comment, "unique_visits":unique_visits}
        return render(request, "players/player.html" , context)


    def post(self, request, slug):
         """Комментарии"""
        form = CommentForm(request.POST, request.FILES)
        player = Player.objects.get(url=slug)
        new = form.save(commit=False)
        new.for_who = player
        new.save()
        return redirect(f'/{player.url}')
