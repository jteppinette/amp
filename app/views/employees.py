from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DeleteView

from app.utils.views.generic import SearchListView, SearchCSVView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from app.models import Employee, Log

from app.forms.employees import NewEmployeeForm, UpdateEmployeeForm


class ListEmployees(SearchListView):
    paginate_by = 20
    template_name = 'employees/list.html'
    model = Employee
    search_fields = {'first_name': 'icontains', 'last_name': 'icontains'}

    def get_queryset(self, *args, **kwargs):
        orderby = self.request.GET.get('orderby', None)
        qs = super(ListEmployees, self).get_queryset(*args, **kwargs).filter(company=self.request.user.company)
        if orderby is None or orderby == '' or orderby == 'None':
            return qs
        else:
            return qs.order_by(str(orderby))

    def get_context_data(self, *args, **kwargs):
        context = super(ListEmployees, self).get_context_data(*args, **kwargs)
        context['options'] = [
            {'value': 'first_name', 'name': 'First Name'},
            {'value': 'last_name', 'name': 'Last Name'},
            {'value': 'last_training_date', 'name': 'Training Due Date'},
            {'value': 'last_background_check_date', 'name': 'Background Due Date'},
        ]
        context['orderby'] = self.request.GET.get('orderby', None)
        return context


class CSVEmployees(SearchCSVView):
    model = Employee
    search_fields = {'first_name': 'icontains', 'last_name': 'icontains'}

    def get_queryset(self, *args, **kwargs):
        orderby = self.request.GET.get('orderby', None)
        qs = super(CSVEmployees, self).get_queryset(*args, **kwargs).filter(company=self.request.user.company)
        if orderby is None or orderby == '' or orderby == 'None':
            return qs
        else:
            return qs.order_by(str(orderby))


class NewEmployee(SuccessMessageMixin, CreateView):
    template_name = 'employees/new.html'
    form_class = NewEmployeeForm
    success_url = reverse_lazy('list-employees')
    success_message = 'Employee %(first_name)s %(last_name)s was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewEmployee, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company.pk})
        return kwargs

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()
        Log.objects.create(author=self.request.user.email, **obj.creation_log())
        return super(NewEmployee, self).form_valid(form)


class UpdateEmployee(SuccessMessageMixin, UpdateView):
    template_name = 'employees/update.html'
    form_class = UpdateEmployeeForm
    model = Employee
    success_url = reverse_lazy('list-employees')
    success_message = 'Employee %(first_name)s %(last_name)s was successfully updated.'

    def form_valid(self, form):
        old_permissions = self.object.permissions.all()
        length = len(old_permissions)

        obj = form.save()
        Log.objects.create(author=self.request.user.email, **self.object.permission_change_log(old_permissions))
        return super(UpdateEmployee, self).form_valid(form)


class DeleteEmployee(DeleteView):
    model = Employee
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-employees')
