from django.apps import apps

from facilities.models import Facility
from rest_framework.views import APIView, Response

from .report_config import REPORTS


class FIlterReportMixin(object):
    def get_report_data(self, *args, **kwargs):
        report_type = self.request.query_params.get(
            "report_type", "facility_count_by_county")

        report_config = REPORTS[report_type]
        app_label, model_name = report_config.get(
            "filter_fields").get("model").split('.')
        filter_field_name = report_config.get(
            "filter_fields").get("filter_field_name")
        model = apps.get_model(app_label, model_name)
        model_instances = model.objects.all()
        return_instance_name = report_config.get(
            "filter_fields").get("return_field")[0]
        return_count_name = report_config.get(
            "filter_fields").get("return_field")[1]
        data = []
        for instance in model_instances:
            filiter_data = {
                filter_field_name: instance
            }
            count = Facility.objects.filter(**filiter_data).count()
            instance_name = instance. name
            data.append(
                {
                    return_instance_name: instance_name,
                    return_count_name: count
                }
            )
        return data


class ReportView(FIlterReportMixin, APIView):
    def get(self, *args, **kwargs):
        data = self.get_report_data()
        return Response(data=data)
