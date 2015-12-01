"""
Define the views used to render the AMP Logs pages.
"""

from app.utils.views.generic import SearchListView, SearchCSVView

from app.models import Log

class ListLogs(SearchListView):
    """
    List the logs that are generated by AMP.
    """
    queryset = Log.objects.all().order_by('-creation_time')
    paginate_by = 20
    template_name = 'logs/list.html'
    search_fields = {'category': 'exact', 'author': 'icontains', 'accessor': 'icontains'}

    def get_context_data(self, *args, **kwargs):
        """
        Add categories to the context.
        """
        context = super(ListLogs, self).get_context_data(*args, **kwargs)
        context['categories'] = Log.CATEGORIES
        return context

class CSVLogs(SearchCSVView):
    queryset = Log.objects.all().order_by('-creation_time')
    search_fields = {'category': 'exact', 'author': 'icontains', 'accessor': 'icontains'}
