from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import News
from .forms import NewsForm

class NewsListView(ListView):
    model = News
    template_name = "news/list_articles.html"
    context_object_name = "news"
    
    def get_queryset(self):
        return News.objects.filter(created_by=self.request.user)

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = "news/write_article.html"
    success_url = reverse_lazy("news:news_list") 

    def form_valid(self, form):
        form.instance.created_by = self.request.user  
        messages.success(self.request, "Your article have been successfully published.")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class NewsDetailView(DetailView):
    model = News
    template_name = "news/article.html"
    context_object_name = "article"

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/delete_article.html'
    success_url = reverse_lazy('news:news_list')

class NewsUpdateView(UpdateView):
    model = News
    fields = ['title', 'content', 'image']
    template_name = 'news/edit_article.html'
    
    def get_success_url(self):
        return reverse_lazy('news:news_list')
    