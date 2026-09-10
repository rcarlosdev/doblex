from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware ASGI para inyectar cabeceras de seguridad HTTP profesionales
    y eliminar cabeceras que divulguen detalles técnicos del servidor.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # 1. Protección contra MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 2. Protección contra Clickjacking (no permitir embebido en iframes)
        response.headers["X-Frame-Options"] = "DENY"

        # 3. Protección heredada contra XSS en navegadores compatibles
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 4. Política de Referencia estricta
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 5. Política de Permisos (Sensores de hardware restringidos a origen propio)
        response.headers["Permissions-Policy"] = "geolocation=(self), camera=(self), microphone=(), payment=()"

        # 6. Content-Security-Policy adaptada para API REST y documentación (Swagger / ReDoc)
        is_docs_route = request.url.path.startswith(("/docs", "/redoc", "/openapi.json"))
        if is_docs_route:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "img-src 'self' data: blob: http: https: https://fastapi.tiangolo.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "font-src 'self' data: https://cdn.jsdelivr.net; "
                "connect-src 'self' http: https: ws: wss:; "
                "frame-ancestors 'none'; "
                "object-src 'none';"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "img-src 'self' data: blob: http: https:; "
                "style-src 'self' 'unsafe-inline'; "
                "script-src 'self'; "
                "font-src 'self' data:; "
                "connect-src 'self' http: https: ws: wss:; "
                "frame-ancestors 'none'; "
                "object-src 'none';"
            )

        # 7. Strict-Transport-Security (HSTS) para asegurar HTTPS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # 8. Eliminar cabeceras que revelen tecnología de servidor
        if "server" in response.headers:
            del response.headers["server"]
        if "x-powered-by" in response.headers:
            del response.headers["x-powered-by"]

        return response
