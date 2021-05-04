"""Filters."""
import logging

import django_filters
from django.contrib.admin import widgets as admin_widgets
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import FilterSet

from ninetofiver import models

logger = logging.getLogger(__name__)


# Filters for reports
class AdminReportTimesheetContractOverviewFilter(FilterSet):
    """Timesheet contract overview admin report filter."""
    performance__contract = (django_filters.ModelMultipleChoiceFilter(
                             label='Contract', queryset=(models.Contract.objects
                                                         .filter(active=True)
                                                         .select_related('customer'))))
    performance__contract__polymorphic_ctype__model = (django_filters.MultipleChoiceFilter(
                                               label='Contract type',
                                               choices=[('projectcontract', _('Project')),
                                                        ('consultancycontract', _('Consultancy')),
                                                        ('supportcontract', _('Support'))],
                                               distinct=True))
    performance__contract__customer = (django_filters.ModelMultipleChoiceFilter(
                                       label='Contract customer', queryset=models.Company.objects.filter(),
                                       distinct=True))
    performance__contract__company = (django_filters.ModelMultipleChoiceFilter(
                                      label='Contract company', queryset=models.Company.objects.filter(internal=True),
                                      distinct=True))
    performance__contract__contract_groups = (django_filters.ModelMultipleChoiceFilter(
                                              label='Contract group', queryset=models.ContractGroup.objects.all(),
                                              distinct=True))
    month = django_filters.MultipleChoiceFilter(choices=lambda: [[x + 1, x + 1] for x in range(12)])
    year = django_filters.MultipleChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                                 .values_list('year', flat=True)
                                                                                 .order_by('year').distinct())])
    user = django_filters.ModelMultipleChoiceFilter(queryset=auth_models.User.objects.filter(is_active=True))
    user__employmentcontract__company = django_filters.ModelChoiceFilter(
                                        label='User company', queryset=models.Company.objects.filter(internal=True), distinct=True)

    class Meta:
        model = models.Timesheet
        fields = {
            'performance__contract': ['exact'],
            'performance__contract__polymorphic_ctype__model': ['exact'],
            'performance__contract__customer': ['exact'],
            'performance__contract__company': ['exact'],
            'performance__contract__contract_groups': ['exact'],
            'month': ['exact'],
            'year': ['exact'],
            'user': ['exact'],
            'user__employmentcontract__company': ['exact'],
            'status': ['exact'],
        }


class AdminReportTimesheetOverviewFilter(FilterSet):
    """Timesheet overview admin report filter."""
    user = django_filters.ModelChoiceFilter(queryset=auth_models.User.objects.filter(is_active=True))
    user__employmentcontract__company = django_filters.ModelChoiceFilter(
        label='Company', queryset=models.Company.objects.filter(internal=True), distinct=True)
    year = django_filters.ChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                         .values_list('year', flat=True)
                                                                         .order_by('year').distinct())])
    month = django_filters.ChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                          .values_list('month', flat=True)
                                                                          .order_by('month').distinct())])

    class Meta:
        model = models.Timesheet
        fields = {
            'user': ['exact'],
            'user__employmentcontract__company': ['exact'],
            'status': ['exact'],
            'year': ['exact'],
            'month': ['exact'],
        }


class AdminReportUserRangeInfoFilter(FilterSet):
    """User range info admin report filter."""
    user = django_filters.ModelChoiceFilter(queryset=auth_models.User.objects.filter(is_active=True))
    from_date = django_filters.DateFilter(label='From', widget=admin_widgets.AdminDateWidget())
    until_date = django_filters.DateFilter(label='Until', widget=admin_widgets.AdminDateWidget())

    class Meta:
        model = models.Timesheet
        fields = {
            'user': ['exact'],
        }


class AdminReportUserLeaveOverviewFilter(FilterSet):
    """User leave overview admin report filter."""
    user = django_filters.ModelChoiceFilter(field_name='leave__user',
                                            queryset=auth_models.User.objects.filter(is_active=True))
    from_date = django_filters.DateFilter(label='From', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                          lookup_expr='date__gte')
    until_date = django_filters.DateFilter(label='Until', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                           lookup_expr='date__lte')

    class Meta:
        model = models.LeaveDate
        fields = {}


class AdminReportUserWorkRatioByUserFilter(FilterSet):
    """User work ratio admin report filter."""
    user = django_filters.ModelChoiceFilter(queryset=auth_models.User.objects.filter(is_active=True))
    year = django_filters.MultipleChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                         .values_list('year', flat=True)
                                                                         .order_by('year').distinct())])

    class Meta:
        model = models.Timesheet
        fields = {}


class AdminReportUserWorkRatioByMonthFilter(FilterSet):
    """User work ratio admin report filter."""
    year = django_filters.ChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                                .values_list('year', flat=True)
                                                                                .order_by('year').distinct())],
                                                                                initial='2019')
    month = django_filters.ChoiceFilter(choices=lambda: [[x + 1, x + 1] for x in range(12)])

    class Meta:
        model = models.Timesheet
        fields = {}


class AdminReportUserWorkRatioOverviewFilter(FilterSet):
    """User work ratio overview admin report filter."""
    user = django_filters.ModelChoiceFilter(queryset=auth_models.User.objects.filter(is_active=True))
    year = django_filters.ChoiceFilter(choices=lambda: [[x, x] for x in (models.Timesheet.objects
                                                                         .values_list('year', flat=True)
                                                                         .order_by('year').distinct())])

    class Meta:
        model = models.Timesheet
        fields = {}


class AdminReportResourceAvailabilityOverviewFilter(FilterSet):
    """User leave overview admin report filter."""
    user = (django_filters.ModelMultipleChoiceFilter(label='User',
                                                     queryset=auth_models.User.objects.filter(is_active=True),
                                                     distinct=True))
    group = (django_filters.ModelMultipleChoiceFilter(label='Group',
                                                      queryset=auth_models.Group.objects.all(),
                                                      distinct=True))
    contract = (django_filters.ModelMultipleChoiceFilter(label='Contract',
                                                         queryset=models.Contract.objects.filter(active=True),
                                                         distinct=True))
    from_date = django_filters.DateFilter(label='From', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                          lookup_expr='date__gte')
    until_date = django_filters.DateFilter(label='Until', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                           lookup_expr='date__lte')

    class Meta:
        model = auth_models.User
        fields = {}


class AdminReportInternalAvailabilityOverviewFilter(FilterSet):
    """Internal availability overview report filter."""
    user = (django_filters.ModelMultipleChoiceFilter(label='User',
                                                     queryset=auth_models.User.objects.filter(is_active=True),
                                                     distinct=True))
    group = (django_filters.ModelMultipleChoiceFilter(label='Group',
                                                      queryset=auth_models.Group.objects.all(),
                                                      distinct=True))
    contract = (django_filters.ModelMultipleChoiceFilter(label='Contract',
                                                         queryset=models.Contract.objects.filter(active=True),
                                                         distinct=True))
    date = django_filters.DateFilter(label='Date', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                     lookup_expr='date__gte')

    class Meta:
        model = auth_models.User
        fields = {}


class AdminReportTimesheetMonthlyOverviewFilter(FilterSet):
    """Timesheet monthly overview admin report filter."""
    user = (django_filters.ModelMultipleChoiceFilter(label='User',
                                                     queryset=auth_models.User.objects.filter(is_active=True),
                                                     distinct=True))
    group = (django_filters.ModelMultipleChoiceFilter(label='Group',
                                                      queryset=auth_models.Group.objects.all(),
                                                      distinct=True))
    base_date = django_filters.DateFilter(label='Month', widget=admin_widgets.AdminDateWidget(), field_name='base_date',
                                          lookup_expr='date__gte')

    class Meta:
        model = auth_models.User
        fields = {}


class AdminReportExpiringConsultancyContractOverviewFilter(FilterSet):
    """Expiring consultancy contract overview admin report filter."""
    company = (django_filters.ModelMultipleChoiceFilter(queryset=models.Company.objects.filter(internal=True),
                                                        distinct=True))
    filter_internal = django_filters.ChoiceFilter(label='Filter internal contracts',
                                                  empty_label="Show all project",
                                                  choices=(
                                                      ('show_noninternal', 'Show only non-internal consultancy contracts'),
                                                      ('show_internal', 'Show only internal consultancy contracts'),
                                                  ))

    class Meta:
        model = models.ConsultancyContract
        fields = {}


class AdminReportProjectContractOverviewFilter(FilterSet):
    """Project contract overview admin report filter."""
    contract_ptr = (django_filters.ModelMultipleChoiceFilter(label='Contract',
                                                             field_name='contract_ptr',
                                                             queryset=models.ProjectContract.objects.filter(active=True),
                                                             distinct=True))
    customer = (django_filters.ModelMultipleChoiceFilter(queryset=models.Company.objects.filter(),
                                                         distinct=True))
    company = (django_filters.ModelMultipleChoiceFilter(queryset=models.Company.objects.filter(internal=True),
                                                        distinct=True))
    contractuser__user = (django_filters.ModelMultipleChoiceFilter(label='User',
                                                                   queryset=auth_models.User.objects.filter(is_active=True),
                                                                   distinct=True))
    contract_groups = (django_filters.ModelMultipleChoiceFilter(queryset=models.ContractGroup.objects.all(),
                                                                distinct=True))

    class Meta:
        model = models.ProjectContract
        fields = {
            # TODO fix this!!!
            'contract_ptr': ['exact'],
            'name': ['icontains'],
            'contract_groups': ['exact'],
            'company': ['exact'],
            'customer': ['exact'],
            'contractuser__user': ['exact'],
        }


class AdminReportUserOvertimeOverviewFilter(FilterSet):
    """User overtime overview admin report filter."""
    user = django_filters.ModelChoiceFilter(field_name='leave__user',
                                            queryset=auth_models.User.objects.filter(is_active=True))
    from_date = django_filters.DateFilter(label='From', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                          lookup_expr='date__gte')
    until_date = django_filters.DateFilter(label='Until', widget=admin_widgets.AdminDateWidget(), field_name='starts_at',
                                           lookup_expr='date__lte')

    class Meta:
        model = models.LeaveDate
        fields = {}


class AdminReportExpiringSupportContractOverviewFilter(FilterSet):
    """Expiring support contract overview admin report filter."""
    company = (django_filters.ModelMultipleChoiceFilter(queryset=models.Company.objects.filter(internal=True),
                                                        distinct=True))
    filter_internal = django_filters.ChoiceFilter(label='Filter internal contracts',
                                                  empty_label="Show all project",
                                                  choices=(
                                                      ('show_noninternal', 'Show only non-internal consultancy contracts'),
                                                      ('show_internal', 'Show only internal consultancy contracts'),
                                                  ))

    class Meta:
        model = models.SupportContract
        fields = {}


class AdminReportInvoicedConsultancyContractOverviewFilter(FilterSet):

    from_date = django_filters.DateFilter(label='From', widget=admin_widgets.AdminDateWidget())
    until_date = django_filters.DateFilter(label='Until', widget=admin_widgets.AdminDateWidget())

    class Meta:
        model = models.ConsultancyContract
        fields = {
                'company',
        }


class AdminReportExpiringUserTrainingOverviewFilter(FilterSet):
    """Expiring support contract overview admin report filter."""
    ends_at_lte = django_filters.DateFilter(label='Ends before', widget=admin_widgets.AdminDateWidget(),
                                            field_name='ends_at', lookup_expr='lte')

    class Meta:
        model = models.Training
        fields = {}
