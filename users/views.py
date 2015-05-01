from rest_framework import generics

from .models import MflUser
from .serializers import UserSerializer
from .filters import MFLUserFilter


class UserList(generics.ListCreateAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer
    filter_class = MFLUserFilter
    ordering_fields = ('first_name', 'last_name', 'email', 'username',)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer


# TODO Add proper OAuth support
# TODO Add view to register an application, and a suitable docstring
# The docstring should explain how to register an application
# Protect this view with is_staff and is_superuser

# TODO Sort out ConfirmEmailView ( see rest-auth FAQs )
# TODO Document API login vis session
# TODO Document API login via OAuth2
# TODO Remove token authentication
# TODO Document API logout
# TODO Document password reset
# TODO Document password reset confirmation
# TODO Document password change
# TODO Document GET of user details ( if it overlaps with ours, remove one )
# TODO Document updating user details vis PUT and PATCH
# TODO Document user registration
# TODO Document retrieval of user permisions and how to use them
# TODO Document email verification in registration
# TODO Document future possibility of social media auth
# TODO Add and document APIs for role setup
# TODO Document national vs county stuff
# TODO Implement and test custom permissions that operate on national / county and use object permissions ( for facilities )
# TODO Create in demo data default roles for each county and national
# TODO Define general public role
# TODO Define public role with GIS access
# TODO Document GIS ( map plotting APIs ); enhance if needed
# TODO Map current facilities to GIS and make report of unmapped ones
# TODO Borrow @ngash's introductory API docs
# TODO Write out an overview of the goals and architecture of MFL v2
# TODO Write out a section of the docs that talks about how to use e.g what client, what browser extension
# TODO Add Swagger compatible docstrings to every view
# ( first line summary, detailed description, params from filters including base filter )
