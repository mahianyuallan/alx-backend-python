import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse

# --- Logger Setup ---
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


# --- Task 1: Log Requests ---
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


# --- Task 2: Restrict Access by Time ---
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow only between 6AM (06:00) and 9PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat access restricted outside 6AM–9PM")
        return self.get_response(request)


# --- Task 3: Rate Limiting (5 messages per minute per IP) ---
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST" and "/chats/" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            if ip not in self.ip_tracker:
                self.ip_tracker[ip] = []

            # Keep only requests in the last 60 seconds
            self.ip_tracker[ip] = [t for t in self.ip_tracker[ip] if now - t < 60]

            if len(self.ip_tracker[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded (max 5 messages/min)"},
                    status=429
                )

            self.ip_tracker[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


# --- Task 4: Role Permission ---
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Only allow admin/moderator to delete chats
        if "/chats/delete/" in request.path:
            if not request.user.is_authenticated or getattr(request.user, "role", None) not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)
