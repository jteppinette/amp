"""
Define generic utility views.
"""

from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView, ListView

class MultipleObjectSearchMixin(MultipleObjectMixin):

    def get_queryset(self):
        search = dict(self.request.GET.iteritems())
        try:
            del search['orderby']
        except:
            pass
        for term in search.keys():
            if search[term] is None or search[term] == '':
                del search[term]
            else:
                filter_type = self.search_fields[term]
                complete_filter = '%s__%s' % (term, filter_type)
                search[complete_filter] = search[term]
                del search[term]

        if self.queryset:
            return self.queryset.filter(**search)
        else:
            return self.model.objects.filter(**search)


class BaseSearchListView(BaseListView, MultipleObjectSearchMixin):
    pass


class SearchListView(MultipleObjectTemplateResponseMixin, BaseSearchListView):

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        for field in self.search_fields:
            context[field] = self.request.GET.get(field, '')
        return context
