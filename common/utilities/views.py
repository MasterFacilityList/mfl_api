from rest_framework import generics


class CustomDestroyModelMixin(object):

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class CustomRetrieveUpdateDestroyView(
        CustomDestroyModelMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
