from rest_framework import throttling


class ThrottlingBySession(throttling.SimpleRateThrottle):
    """
    Limits the rating of facility service to only 10 per day per IP.
    This rate is configurable at the DRF settings.DEFAULT_THROTTLE_RATES.

    The rate will apply to both the publc user and other authenticated users.
    """
    scope = 'rating'
    scope_attr = 'throttle_scope'

    def get_cache_key(self, request, view):
        """
        Override this method in order to have an IP based cache key
        for authenticated users instead of the usual user.pk based cache key.
        """
        resource_identity = request.data.get('facility_service', None)
        chu_rating_identity = request.data.get('chu', None)
        if not resource_identity and chu_rating_identity:
            resource_identity = chu_rating_identity
        if resource_identity:
            machine = self.get_ident(request)
            ident = machine + resource_identity
            return self.cache_format % {
                'scope': self.scope,
                'ident': ident
            }
        else:
            return None
