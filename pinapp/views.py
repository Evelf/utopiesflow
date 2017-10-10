from django.views.generic import DetailView, ListView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from pinapp.models import Board, Pin


class BoardList(ListView):
    model = Board


class BoardDetail(DetailView):
    model = Board
    paginate_by = 42

    def get_context_data(self, **kwargs):
        context = super(BoardDetail, self).get_context_data(**kwargs)
        pins = self.get_object().pin_set.order_by('-created_at').all()
        paginator = Paginator(pins, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            page_pins = paginator.page(page)
        except PageNotAnInteger:
            page_pins = paginator.page(1)
        except EmptyPage:
            page_pins = paginator.page(paginator.num_pages)

        context['page_pins'] = page_pins
        return context

class PinDetail(DetailView):
    model = Pin

class PinUpdate(UpdateView):
    model = Pin
    fields = ['local_note']

