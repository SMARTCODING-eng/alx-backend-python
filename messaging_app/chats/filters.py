# filters for messaging app

import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender', 'content']