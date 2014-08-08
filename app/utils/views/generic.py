"""
Define generic utility views.
"""

from django.views.generic import ListView


class SearchListView(ListView):
    """
    Searches on the provided values.
    """

    def get_queryset(self):
        """
        Refine the queryset.
        """
        search = dict(self.request.GET.iteritems())
        for term in search.keys():
            if search[term] is None or search[term] == '':
                del search[term]
            else:
                filter_type = self.search_fields[term]
                complete_filter = '%s__%s' % (term, filter_type)
                search[complete_filter] = search[term]
                del search[term]

        return self.model.objects.filter(**search)

    def get_context_data(self, **kwargs):
        """
        Add search terms.
        """
        context = super(ListView, self).get_context_data(**kwargs)
        for field in self.search_fields:
            context[field] = self.request.GET.get(field, '')
        return context
