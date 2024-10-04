from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'login'
    redirect_field_name = 'next'
    # model = Article
    # context_object_name = 'articles'
    # ordering = ('created_at',)
    # paginate_by = 2
    # paginate_orphans = 1

#     def get(self, request, *args, **kwargs):
#         self.form = self.get_search_form()
#         self.search_value = self.get_search_value()
#         return super().get(request, *args, **kwargs)
#
#     def get_search_form(self):
#         return SearchForm(self.request.GET)
#
#     def get_search_value(self):
#         if self.form.is_valid():
#             return self.form.cleaned_data['search']
#         return None
#
#     def get_queryset(self):
#         queryset = super().get_queryset().exclude(is_deleted=True)
#         if self.search_value:
#             query = Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
#             queryset = queryset.filter(query)
#         return queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context['form'] = self.form
#         context['favorite_form'] = FavoriteForm()
#         if self.search_value:
#             context['query'] = urlencode({'search': self.search_value})
#         return context
#
#
# class IndexRedirectView(RedirectView):
#     pattern_name = 'index'
