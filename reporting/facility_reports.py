from django.apps import apps

from facilities.models import Facility
from rest_framework.views import APIView, Response

from .report_config import REPORTS


class FilterReportMixin(object):
    queryset = Facility.objects.all()

    def _prepare_filters(self, filtering_data):
        filtering_data = filtering_data.split('=')
        return filtering_data[0], filtering_data[1]

    def _build_dict_filter(self, filter_field_name, value):
        return {
            filter_field_name: value
        }

    def _filter_queryset(self, filter_dict):
        return self.queryset.filter(**filter_dict)

    def _filter_relation_obj(self, model, field_name, value):
        filter_dict = {
            field_name: value
        }
        return model.objects.filter(**filter_dict)

    def _filter_by_extra_params(
            self, report_config, more_filters_params, model):
        more_filters = self._prepare_filters(more_filters_params)

        requested_filters = report_config.get(
            'extra_filters')[more_filters[0]]
        requested_filters_filter_field_name = requested_filters.get(
            "filter_field_name")
        filtering_dict = self._build_dict_filter(
            requested_filters_filter_field_name, more_filters[1])

        self.queryset = self._filter_queryset(filtering_dict)
        model_instances = self._filter_relation_obj(
            model, more_filters[0], more_filters[1])
        return model_instances

    def get_report_data(self, *args, **kwargs):
        report_type = self.request.query_params.get(
            "report_type", "facility_count_by_county")

        more_filters_params = self.request.query_params.get("filters", None)

        report_config = REPORTS[report_type]
        app_label, model_name = report_config.get(
            "filter_fields").get("model").split('.')
        filter_field_name = report_config.get(
            "filter_fields").get("filter_field_name")
        model = apps.get_model(app_label, model_name)
        model_instances = model.objects.all()

        if more_filters_params:
            model_instances = self._filter_by_extra_params(
                report_config, more_filters_params, model)

        return_instance_name = report_config.get(
            "filter_fields").get("return_field")[0]
        return_count_name = report_config.get(
            "filter_fields").get("return_field")[1]
        data = []

        for instance in model_instances:
            filiter_data = {
                filter_field_name: instance
            }
            count = self.queryset.filter(**filiter_data).count()
            instance_name = instance. name
            data.append(
                {
                    return_instance_name: instance_name,
                    return_count_name: count
                }
            )
        return {
            "results": data,
            "total": self.queryset.count()
        }


class ReportView(FilterReportMixin, APIView):
    def get(self, *args, **kwargs):
        data = self.get_report_data()
        return Response(data=data)
