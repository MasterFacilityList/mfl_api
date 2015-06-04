from rest_framework import generics
from rest_framework.mixins import DestroyModelMixin


class CustomDestroyModelMixin(DestroyModelMixin):
    """
    Overrides the perform_destroy method.
    """
    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class CustomRetrieveUpdateDestroyView(
        CustomDestroyModelMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
