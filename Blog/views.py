from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import AllNews




def home(request):
    data = {
        'news': AllNews.objects.all(),
        'title': 'Main page'
    }
    return render(request, 'Blog/home.html', data)

class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = AllNews
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class ShowNewsView(ListView):
    model = AllNews
    template_name = 'Blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']

    def get_context_data(self, **kwards):
        ctx = super(ShowNewsView, self).get_context_data(**kwards)
        ctx['title'] = "Главная страница блога"
        return ctx

class NewsDetailView(DetailView):
    model = AllNews

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = AllNews.objects.filter(pk=self.kwargs['pk']).first()
        return ctx
    
class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = AllNews
    fields = ['title', 'text']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = AllNews
    fields = ['title', 'text']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def contacts(request):
    return render(request, 'Blog/contacts.html', {'title': 'Contacts'})
