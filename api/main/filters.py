from django_filters import FilterSet
from main.models import Event, TicketType, Booking, BookingItem
from django_filters import DateTimeFromToRangeFilter, CharFilter, NumberFilter


class EventFilter(FilterSet):
    start_datetime = DateTimeFromToRangeFilter()
    title = CharFilter(field_name='title', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['is_online', 'start_datetime', 'title', 'location']


class TicketTypeFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = TicketType
        fields = ['event', 'status', 'price_min', 'price_max']


class BookingFilter(FilterSet):
    status = CharFilter(field_name='status', lookup_expr='iexact')
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Booking
        fields = ['user', 'status', 'created_at']


class BookingItemFilter(FilterSet):
    quantity_min = NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_max = NumberFilter(field_name='quantity', lookup_expr='lte')

    class Meta:
        model = BookingItem
        fields = ['booking', 'ticket_type', 'quantity_min', 'quantity_max']