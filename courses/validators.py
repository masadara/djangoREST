from django.core.exceptions import ValidationError
from urllib.parse import urlparse

class VideoURLValidator:
    allowed_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value:
            return
        from urllib.parse import urlparse
        parsed_url = urlparse(value)
        domain = parsed_url.netloc.lower()
        if domain not in self.allowed_domains:
            raise ValidationError('Ссылка должна быть только с youtube.com или youtu.be')
