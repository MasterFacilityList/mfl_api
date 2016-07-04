from rest_framework import generics
from rest_framework.exceptions import ValidationError

from django.db.models.deletion import Collector, ProtectedError


def delete_child_instances(instance):
    try:
        collector = Collector(using='default')
        collector.collect(objs=[instance], collect_related=True)
    except ProtectedError as error:
        raise ValidationError({

               "Error": ["cannot deleted the record since there are"
               " other records that depend on it"]

            })

class CustomDestroyModelMixin(object):

    def perform_destroy(self, instance):
        delete_child_instances(instance)

        instance.deleted = True
        instance.save()


class CustomRetrieveUpdateDestroyView(
        CustomDestroyModelMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
