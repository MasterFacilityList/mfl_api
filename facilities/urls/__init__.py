from .facility_urls import urlpatterns as facility_url_patterns
from .practitioner_urls import urlpatterns as practitioner_url_patterns

urlpatterns = facility_url_patterns + practitioner_url_patterns
