import functools
import uuid

from datetime import timedelta
from collections import OrderedDict
from django.apps import apps
from django.db.models import Sum
from django.db.models import Q
from django.utils import timezone

from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound, ValidationError

from facilities.models import (
    Facility,
    FacilityType,
    KephLevel,
    FacilityUpgrade, OwnerType, Owner)
from common.constants import TRUTH_NESS, FALSE_NESS
from common.models import (
    County, Constituency, Ward, SubCounty
)
from chul.models import CommunityHealthUnit, Status
from mfl_gis.models import FacilityCoordinates

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

    def _get_return_data(
            self, filter_field_name, model_instances, return_instance_name,
            return_count_name):
        data = []

        for instance in model_instances:
            filiter_data = {
                filter_field_name: instance
            }
            count = self.queryset.filter(**filiter_data).count()
            instance_name = instance.name
            data.append(
                {
                    return_instance_name: instance_name,
                    return_count_name: count
                }
            )
        return data

    def get_report_data(self, *args, **kwargs):
        """Route reports based on report_type param."""
        report_type = self.request.query_params.get(
            "report_type", "facility_count_by_county")
        if report_type == "facility_count_by_facility_type_detailed":
            return self._get_facility_type_data()

        if report_type == "facility_count_by_county":
            return self._get_facility_count_by_county()

        if report_type == "facility_keph_level_report":
            return self._get_facility_count(keph=True)

        if report_type == "facility_constituency_report":
            return self._get_facility_constituency_data()

        if report_type == "facility_count_by_sub_county":
            return self._get_facility_sub_county_data()

        if report_type == "individual_facility_beds_and_cots":
            return self._get_facilities_beds_and_cots()

        if report_type == "facility_count_by_owner_category":
            return self._get_facility_count(category=True)

        if report_type == "facility_count_by_owner":
            return self._get_facility_count(category=False)

        if report_type == "facility_count_by_facility_type":
            return self._get_facility_count(category=False, f_type=True)

        if report_type == "gis":
            return self._get_gis_report()

        if report_type == "beds_and_cots_by_county":
            return self._get_beds_and_cots({
                'ward__sub_county__county__name': 'county_name',
                'ward__sub_county__county': 'county'
            })

        if report_type == "beds_and_cots_by_constituency":
            county_id = self.request.query_params.get("county", None)
            filters = (
                {} if county_id is None
                else {"ward__sub_county__county": county_id}
            )
            return self._get_beds_and_cots(vals={
                'ward__sub_county__name': 'sub_county_name',
                'ward__sub_county': 'sub_county'
            }, filters=filters)

        if report_type == "beds_and_cots_by_ward":
            constituency_id = self.request.query_params.get(
                "constituency", None
            )
            filters = (
                {} if constituency_id is None
                else {"ward__sub_county": constituency_id}
            )
            return self._get_beds_and_cots(
                vals={'ward__name': 'ward_name', 'ward': "ward"},
                filters=filters
            )

        more_filters_params = self.request.query_params.get("filters", None)

        report_config = REPORTS.get(report_type, None)
        if report_config is None:
            raise NotFound(detail="Report not found.")

        group_by = report_config.get("group_by")
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
        if group_by:
            pass
        else:
            data = self._get_return_data(
                filter_field_name, model_instances, return_instance_name,
                return_count_name)
        return data, self.queryset.count()

    def _get_facility_type_data(self):
        owner_category = self.request.query_params.get("owner_category")
        facility_type = self.request.query_params.get("facility_type")

        data = []

        for county in County.objects.all():
            for facility_type in FacilityType.objects.all():
                if not owner_category:
                    count = Facility.objects.filter(
                        facility_type=facility_type,
                        ward__constituency__county=county).count()
                else:
                    count = Facility.objects.filter(
                        facility_type=facility_type,
                        ward__constituency__county=county,
                        owner__owner_type=owner_category).count()

                data.append(
                    {
                        "county": county.name,
                        "facility_type": facility_type.name,
                        "number_of_facilities": count
                    }
                )

        totals = []

        return data, totals

    def _get_facility_keph_level_data(self):
        owner_category = self.request.query_params.get("owner_category")

        data = []

        for county in County.objects.all():
            for level in KephLevel.objects.all():
                if not owner_category:
                    count = Facility.objects.filter(
                        keph_level=level,
                        ward__constituency__county=county).count()
                else:
                    count = Facility.objects.filter(
                        level=level,
                        ward__constituency__county=county,
                        owner__owner_type=owner_category).count()

                data.append({
                    "county": county.name,
                    "keph_level": level.name,
                    "number_of_facilities": count
                })

        totals = []
        return data, totals

    def _get_facility_constituency_data(self):
        owner_category = self.request.query_params.get("owner_category")

        data = []

        for county in County.objects.all():
            for const in Constituency.objects.filter(county=county):
                if not owner_category:
                    count = Facility.objects.filter(
                        ward__constituency=const).count()
                else:
                    count = Facility.objects.filter(
                        ward__constituency=const,
                        owner__owner_type=owner_category).count()

                data.append({
                    "county": county.name,
                    "constituency": const.name,
                    "number_of_facilities": count
                })

            totals = []
        return data, totals

    def _get_facility_sub_county_data(self):
        report_level = self.request.query_params.get('report_level', None)
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)

        data = []
        totals = []
        if report_level == 'national':

            for county in County.objects.all():
                count = Facility.objects.filter(
                    ward__sub_county__county=county).count()
                data_dict = {
                    "number_of_facilities": count,
                    "county_id": str(county.id),
                    "county": county.name,
                }
                data.append(data_dict)

        if report_level == 'county':
            for sub_county in SubCounty.objects.filter(
                    county_id__in=county.split(',')):
                count = Facility.objects.filter(
                    ward__sub_county=sub_county).count()
                data_dict = {
                    "number_of_facilities": count,
                    "sub_county_id": str(sub_county.id),
                    "sub_county": sub_county.name,
                }
                data.append(data_dict)

        if report_level == 'sub_county':
            for ward in Ward.objects.filter(
                    sub_county_id__in=sub_county.split(',')):
                count = Facility.objects.filter(
                    ward=ward).count()
                data_dict = {
                    "number_of_facilities": count,
                    "ward": ward.name,
                    "ward_id": str(ward.id)
                }
                data.append(data_dict)

        return data, totals

    def _get_facilities_beds_and_cots(self):
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)
        data = []
        queryset_filter = {}
        if county:
            county = County.objects.get(id=county)
            queryset_filter = {
                "ward__sub_county__county": county
            }
        if sub_county:
            sub_county = SubCounty.objects.get(id=sub_county)
            queryset_filter = {
                "ward__sub_county": sub_county
            }
        if ward:
            ward = Ward.objects.get(id=ward)
            queryset_filter = {
                "ward": ward
            }

        for facility in Facility.objects.filter(
                **queryset_filter).filter(
                Q(number_of_beds__gt=0) | Q(number_of_cots__gt=0)):
            record = {
                "facility_id": str(facility.id),
                "facility_name": facility.name,
                "facility_code": facility.code,
                "number_of_beds": facility.number_of_beds,
                "number_of_cots": facility.number_of_cots
            }
            data.append(record)

        return data, []

    def _get_beds_and_cots(self, vals={}, filters={}):
        fields = vals.keys()
        assert len(fields) == 2
        items = Facility.objects.values(*fields).filter(**filters).annotate(
            cots=Sum('number_of_cots'), beds=Sum('number_of_beds')
        ).order_by()

        total_cots, total_beds = functools.reduce(
            lambda x, y: (x[0] + y['cots'], x[1] + y['beds']),
            items, (0, 0)
        )

        return [
            {
                'cots': p['cots'],
                'beds': p['beds'],
                vals[fields[0]]: p[fields[0]],
                vals[fields[1]]: p[fields[1]]
            } for p in items
        ], {"total_cots": total_cots, "total_beds": total_beds}

    def _get_facility_count_by_county(self):
        data = []
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)

        obj_filter_param = {}
        area = None
        model = County
        facility_filter_str = "ward__sub_county__county"

        if county:
            obj_filter_param = {
                "county_id__in": county.split(',')
            }
            model = SubCounty
            facility_filter_str = "ward__sub_county"

        if sub_county:
            obj_filter_param = {
                "sub_county_id__in": sub_county.split(',')
            }
            model = Ward
            facility_filter_str = "ward"

        for area in model.objects.filter(**obj_filter_param):
            facility_filter = {
                facility_filter_str: area
            }
            fac_count = Facility.objects.filter(
                **facility_filter).count()
            data_dict = {
                "area_name": area.name,
                "area_id": str(area.id),
                "number_of_facilities": fac_count
            }
            data.append(data_dict)

        return data, []

    def _get_facility_count_by_sub_county_in_county(self):
        data = []
        for county in County.objects.all():
            fac_count = Facility.objects.filter(
                ward__sub_county__county=county).count()
            data_dict = {
                "county_name": county.name,
                "county_id": str(county.id),
                "number_of_facilities": fac_count
            }
            data.append(data_dict)

        return data, []

    def _get_gis_report(self):
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)
        constituency = self.request.query_params.get('ward', None)

        queryset = FacilityCoordinates.objects.all()

        if county:
            queryset = FacilityCoordinates.objects.filter(
                facility__ward__constituency__county_id__in=county.split(','))

        if sub_county:
            queryset =  FacilityCoordinates.objects.filter(
                facility__ward__sub_county_id__in=sub_county.split('.'))

        if constituency:
            queryset =  FacilityCoordinates.objects.filter(
                facility__ward__constituency_id__in=sub_county.split('.'))

        if ward:
            queryset =  FacilityCoordinates.objects.filter(
                facility__ward_id__in=ward.split('.'))


        cords = []
        if any([county, sub_county, constituency, ward]):
            for fac in  queryset:
                record = OrderedDict()
                record["facility_code"] = fac.facility.code
                record["facility_name"] = fac.facility.name
                record["facility_county"] = fac.facility.ward.constituency.county.name
                record["facility_ward"] = fac.facility.ward.name
                record["facility_constituency"] = fac.facility.ward.constituency.name
                record["facility_lat"] = fac.coordinates[1]
                record["facility_long"] =  fac.coordinates[0]
                record["facility_id"] = fac.facility.id

                if fac.facility.ward.sub_county:
                    record["facility_sub_county"] = fac.facility.ward.sub_county.name
                cords.append(record)


        return cords, [len(queryset)]

    def _get_facility_count(self, category=True, f_type=False, keph=False):
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)

        vals = []
        vals.append(county) if county else None
        vals.append(sub_county) if sub_county else None
        vals.append(ward) if ward else None

        for val in vals:
            try:
                for c in val.split(','):
                    uuid.UUID(c)
            except:
                raise ValidationError(
                    {
                        "Administrative area": [
                            "The area id provided is"
                            " in the wrong format"
                        ]
                    }
                )

        owner_model = OwnerType if category else Owner
        if f_type:
            owner_model = FacilityType
        if keph:
            owner_model = KephLevel

        admin_area_filter = {}
        if county:
            admin_area_filter = {
                "ward__sub_county__county_id__in": county.split(',')
            }
        if sub_county:
            admin_area_filter = {
                "ward__sub_county_id__in": sub_county.split(',')
            }
        if ward:
            admin_area_filter = {
                "ward_id__in": ward.split(',')
            }
        data = []

        for owner in owner_model.objects.all():
            if category:
                owner_filter = {
                    "owner__owner_type": owner
                }
                field_name = 'owner_category'
            else:
                owner_filter = {
                    "owner": owner
                }
                field_name = 'owner'
            if f_type:
                owner_filter = {
                    "facility_type": owner
                }
                field_name = 'type_category'

            if keph:
                owner_filter = {
                    "keph_level": owner
                }
                field_name = 'keph_level'

            data_dict = {
                field_name: owner.name,
                "id": str(owner.id),
                "number_of_facilities": Facility.objects.filter(
                    **owner_filter).filter(
                    **admin_area_filter).count()
            }
            data.append(data_dict)
        return data, []


class ReportView(FilterReportMixin, APIView):

    def get(self, *args, **kwargs):
        data, totals = self.get_report_data()

        return Response(data={
            "results": data,
            "total": totals
        })


class FacilityUpgradeDowngrade(APIView):

    def get(self, *args, **kwargs):
        county = self.request.query_params.get('county', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)
        see_facilities = self.request.query_params.get('see_facilities', None)
        upgrade = self.request.query_params.get('upgrade', None)

        right_now = timezone.now()
        last_week = self.request.query_params.get('last_week', None)
        last_month = self.request.query_params.get('last_month', None)
        last_three_months = self.request.query_params.get(
            'last_three_months', None)
        three_months_ago = right_now - timedelta(days=90)
        last_one_week = right_now - timedelta(days=7)
        last_one_month = right_now - timedelta(days=30)

        if upgrade in TRUTH_NESS:
            all_changes = FacilityUpgrade.objects.filter(
                is_upgrade=True)
        elif upgrade in FALSE_NESS:
            all_changes = FacilityUpgrade.objects.filter(
                is_upgrade=False)
        else:
            all_changes = FacilityUpgrade.objects.all()

        if last_week:
            all_changes = all_changes.filter(created__gte=last_one_week)
        if last_month:
            all_changes = all_changes.filter(created__gte=last_one_month)
        if last_three_months:
            all_changes = all_changes.filter(created__gte=three_months_ago)

        facilities_ids = [change.facility.id for change in all_changes]
        changed_facilities = Facility.objects.filter(id__in=facilities_ids)

        if not county and not sub_county:
            results = []
            for county in County.objects.all():
                facility_count = changed_facilities.filter(
                    ward__constituency__county=county).count()
                data = {
                    "area": county.name,
                    "area_id": county.id,
                    "changes": facility_count
                }
                results.append(data)
            return Response(data={
                "total_number_of_changes": len(facilities_ids),
                "results": results
            })
        if county and not sub_county:
            results = []
            for sub in SubCounty.objects.filter(county_id__in=county.split(',')):
                facility_count = changed_facilities.filter(
                    ward__sub_county=sub).count()
                data = {
                    "area": sub.name,
                    "area_id": sub.id,
                    "changes": facility_count
                }
                results.append(data)
            return Response(data={
                "total_number_of_changes": len(facilities_ids),
                "results": results
            })

        if county and sub_county:
            results = []
            sub_counties = sub_county.split(',')
            ward_filter = {
                "sub_county_id__in": sub_counties
            }
            if ward:
                wards = ward.split(',')
                ward_filter = {
                    "id__in": wards
                }
            for ward in Ward.objects.filter(**ward_filter):
                facility_count = changed_facilities.filter(
                    ward=ward).count()
                data = {
                    "area": ward.name,
                    "area_id": ward.id,
                    "changes": facility_count
                }
                results.append(data)
            return Response(data={
                "total_number_of_changes": len(facilities_ids),
                "results": results
            })

        if not county:
            facilities = changed_facilities.filter(ward__constituency__county_id=county)
            records = []
            for facility in facilities:
                latest_facility_change = FacilityUpgrade.objects.filter(facility=facility)[0]
                data = {
                    "name": facility.name,
                    "code": facility.code,
                    "current_keph_level":
                        latest_facility_change.keph_level.name,
                    "previous_keph_level":
                        latest_facility_change.current_keph_level_name,
                    "previous_facility_type":
                        latest_facility_change.current_facility_type_name,
                    "current_facility_type":
                        latest_facility_change.facility_type.name,
                    "reason": latest_facility_change.reason.reason
                }
                records.append(data)

            return Response(data={
                "total_facilities_changed": len(facilities),
                "results": records
            })


class CommunityHealthUnitReport(APIView):
    queryset = CommunityHealthUnit.objects.all()

    def get_county_reports(self, queryset=queryset):
        data = []
        counties = County.objects.all()
        total_chus = 0
        for county in counties:
            chu_count = queryset.filter(
                facility__ward__constituency__county=county).count()
            total_chus += chu_count
            data.append(
                {
                    "county_name": county.name,
                    "county_id": county.id,
                    "number_of_units": chu_count
                }
            )
        return data, total_chus

    def get_constituency_reports(self, county=None, queryset=queryset):
        data = []
        constituencies = Constituency.objects.all()

        if county:
            constituencies = constituencies.filter(county_id=county)
        total_chus = 0
        for const in constituencies:
            chu_count = queryset.filter(
                facility__ward__constituency=const).count()
            total_chus += chu_count
            data.append(
                {
                    "constituency_name": const.name,
                    "constituency_id": const.id,
                    "number_of_units": chu_count
                }
            )
        return data, total_chus

    def get_sub_county_reports(self, county=None, queryset=queryset):
        data = []
        sub_county = SubCounty.objects.all()

        if county:
            sub_county = sub_county.filter(county_id=county)
        total_chus = 0
        for sub in sub_county:
            chu_count = queryset.filter(
                facility__ward__sub_county=sub).count()
            total_chus += chu_count
            data.append(
                {
                    "sub_county_name": sub.name,
                    "sub_county_id": sub.id,
                    "number_of_units": chu_count
                }
            )
        return data, total_chus

    def get_ward_reports(self, constituency=None, queryset=queryset):
        data = []
        wards = Ward.objects.all()
        if constituency:
            wards = wards.filter(sub_county_id=constituency)

        total_chus = 0
        for ward in wards:
            chu_count = queryset.filter(
                facility__ward=ward).count()
            total_chus += chu_count
            data.append(
                {
                    "ward_name": ward.name,
                    "ward_id": ward.id,
                    "number_of_units": chu_count
                }
            )
        return data, total_chus

    def get_date_established_report(
            self, county=None, constituency=None):
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        queryset = self.queryset.filter(created__gte=three_months_ago)

        if county:
            return self.get_constituency_reports(
                county=county, queryset=queryset)
        elif constituency:
            return self.get_ward_reports(
                constituency=constituency, queryset=queryset)
        else:
            return self.get_county_reports(queryset=queryset)

    def get_status_report(self, constituency=None, county=None, chu_list=False,
            ward=None, sub_county=None):
        data = []
        if county:
            self.queryset = self.queryset.filter(
                facility__ward__constituency__county_id=county)

        if constituency:
            self.queryset = self.queryset.filter(
                facility__ward__constituency_id=constituency)

        if sub_county:
            self.queryset = self.queryset.filter(
                facility__ward__sub_county_id=sub_county)

        if ward:
            self.queryset = self.queryset.filter(
                facility__ward_id=ward)

        total_chus = 0
        status_filter = {}
        status_id = self.request.query_params.get('status', None)
        chu_list = self.request.query_params.get('chu_list', False)
        ward = self.request.query_params.get('ward', None)

        if ward:
            self.queryset = self.queryset.filter(
                facility__ward_id=ward)

        if status_id:
            status_filter = {
                "id__in": status_id.split(',')
            }
        if not chu_list:
            for status in Status.objects.filter(**status_filter):
                chu_count = self.queryset.filter(
                    status=status).count()
                total_chus += chu_count
                data.append(
                    {
                        "status_name": status.name,
                        "id": str(status.id),
                        "number_of_units": chu_count
                    }
                )
        else:
            if status_id:
                status_filter = {
                    "status_id__in": status_id.split(',')
                }
            for chu in self.queryset.filter(**status_filter):
                chu = {
                    "name": chu.name,
                    "id": str(chu.id),
                    "code": chu.code,
                    "facility_name": chu.facility.name,
                    "county": chu.facility.ward.constituency.county.name,
                    "sub_county": chu.facility.ward.constituency.name,
                    "ward": chu.facility.ward.name,
                    "date_established": chu.date_established.isoformat(),
                    "status": chu.status.name,
                    "number_of_chvs": chu.number_of_chvs
                }
                data.append(chu)
        return data, self.queryset.count()

    def get(self, *args, **kwargs):
        county = self.request.query_params.get('county', None)
        constituency = self.request.query_params.get('constituency', None)
        sub_county = self.request.query_params.get('sub_county', None)
        ward = self.request.query_params.get('ward', None)
        report_type = self.request.query_params.get('report_type', None)
        last_quarter = self.request.query_params.get('last_quarter', None)
        chu_list = self.request.query_params.get('chu_list', False)

        if report_type == 'constituency' and county:
            report_data = self.get_constituency_reports(county=county)

            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'sub_county':
            report_data = self.get_sub_county_reports(county=county)

            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'constituency' and not county:
            report_data = self.get_constituency_reports()
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'ward' and not constituency:
            report_data = self.get_ward_reports()
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'ward' and constituency:
            report_data = self.get_ward_reports(constituency=constituency)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'ward' and chu_list:
            report_data = self.get_status_report()
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)


        if last_quarter and county and not constituency:
            report_data = self.get_date_established_report(county=county)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if last_quarter and constituency:
            report_data = self.get_date_established_report(
                constituency=constituency)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if last_quarter and not county and not constituency:
            report_data = self.get_date_established_report()
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'status' and not county and not constituency:
            if not chu_list:
                report_data = self.get_status_report()
                data = {
                    "total": report_data[1],
                    "results": report_data[0]
                }
            else:
                report_data = self.get_status_report(chu_list=True)
                data = {
                    "total": report_data[1],
                    "results": report_data[0]
                }
            return Response(data)

        if report_type == 'status' and county and not constituency and not sub_county:
            report_data = self.get_status_report(county=county)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'status' and not county and constituency:

            report_data = self.get_status_report(constituency=constituency)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'status' and  county and sub_county:

            report_data = self.get_status_report(sub_county=sub_county)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        if report_type == 'status' and  county and ward:

            report_data = self.get_status_report(ward=ward)
            data = {
                "total": report_data[1],
                "results": report_data[0]
            }
            return Response(data)

        data = {
            "total": self.get_county_reports()[1],
            "results": self.get_county_reports()[0]
        }
        return Response(data)
