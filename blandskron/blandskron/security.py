class SecurityHeadersMiddleware:
    """Apply browser security policies not covered by Django defaults."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; base-uri 'self'; form-action 'self'; "
            "object-src 'none'; frame-ancestors 'none'; img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "script-src 'self' https://www.googletagmanager.com https://*.googletagmanager.com "
            "https://www.clarity.ms https://*.clarity.ms https://cdn.jsdelivr.net; "
            "connect-src 'self' https://www.google-analytics.com https://region1.google-analytics.com "
            "https://www.clarity.ms https://*.clarity.ms; upgrade-insecure-requests",
        )
        return response
