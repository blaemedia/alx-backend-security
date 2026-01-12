from .models import RequestLog

class IPTrackingMiddleware:
    """
    Middleware to log the IP address, timestamp, and path of incoming requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Retrieves the client's IP address from the request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
