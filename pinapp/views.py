from django.views.generic import DetailView, ListView
from pinapp.models import Board


class BoardList(ListView):
    model = Board


class BoardDetail(DetailView):
    model = Board
