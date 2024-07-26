from django.http import HttpRequest
from django.conf import settings

def custom_context_processor(request: HttpRequest) -> dict:
    return {
        'categories': settings.CATEGORIES
    }
