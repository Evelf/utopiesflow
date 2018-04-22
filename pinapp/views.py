from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import DetailView, ListView, UpdateView

from pinapp.models import Board, Pin


class BoardList(LoginRequiredMixin, ListView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super(BoardList, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context


class BoardDetail(LoginRequiredMixin, DetailView):
    model = Board
    paginate_by = 42

    def get_context_data(self, **kwargs):
        context = super(BoardDetail, self).get_context_data(**kwargs)
        pins = self.get_object().pin_set.order_by('-created_at').all()
        paginator = Paginator(pins, self.paginate_by)
        page = self.request.GET.get('page')
        user = self.request.user

        try:
            page_pins = paginator.page(page)
        except PageNotAnInteger:
            page_pins = paginator.page(1)
        except EmptyPage:
            page_pins = paginator.page(paginator.num_pages)

        context['page_pins'] = page_pins
        return context

class PinDetail(LoginRequiredMixin, DetailView):
    model = Pin

class PinUpdate(LoginRequiredMixin, UpdateView):
    model = Pin
    fields = ['local_note']
