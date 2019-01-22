from django.views.generic.base import View
from django.views.generic.list import (
    BaseListView,
    MultipleObjectMixin,
    MultipleObjectTemplateResponseMixin,
)
from djqscsv import render_to_csv_response


class MultipleObjectSearchMixin(MultipleObjectMixin):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        query = {}
        for field, value in self.request.GET.items():
            lookup = self.search_fields.get(field)
            if not value or not lookup:
                continue

            query[f"{field}__{lookup}"] = value

        return queryset.filter(**query) if query else queryset


class BaseSearchListView(MultipleObjectSearchMixin, BaseListView):
    pass


class SearchCSVView(MultipleObjectSearchMixin, View):
    def get(self, *args, **kwargs):
        return render_to_csv_response(self.get_queryset().values())


class SearchListView(MultipleObjectTemplateResponseMixin, BaseSearchListView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for field in self.search_fields:
            context[field] = self.request.GET.get(field, "")
        return context
