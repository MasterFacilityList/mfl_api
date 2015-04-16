from .facility_urls import urlpatterns as facility_url_patterns

from .rating_urls import urlpatterns as rating_url_patterns

urlpatterns = facility_url_patterns + rating_url_patterns
