"""
Define generic utility views.
"""

from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView, ListView

from djqscsv import render_to_csv_response

class MultipleObjectSearchMixin(MultipleObjectMixin):

    def get_queryset(self):
        search = dict(self.request.GET.iteritems())

        search.pop('orderby', None)
        search.pop('page', None)

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

class SearchCSVView(MultipleObjectSearchMixin, View):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {'class_name': self.__class__.__name__})

        return render_to_csv_response(self.object_list.values())


class SearchListView(MultipleObjectTemplateResponseMixin, BaseSearchListView):

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        for field in self.search_fields:
            context[field] = self.request.GET.get(field, '')
        return context
