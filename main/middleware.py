from main.models import LoggingModel

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/api/cities/', '/api/weather/']:
            self.log_request(request)

        response = self.get_response(request)
        return response

    def log_request(self, request):
        ip_address = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        city_name = None
        if request.path == '/api/weather/' and request.method == 'POST':
            city_name = request.POST.get('city_name', None)

        LoggingModel.objects.create(
            user=user,
            ipaddress=ip_address,
            endpoint=request.path,
            http_method=request.method.lower(),
            city_name=city_name
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
