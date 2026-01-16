from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import StandardResultsSetPagination
from main.models import Event, TicketType, Booking, BookingItem
from .serializers import (
    EventSerializer,
    TicketTypeSerializer,
    BookingSerializer,
    BookingItemSerializer
)
from .filters import EventFilter, TicketTypeFilter, BookingFilter, BookingItemFilter
from .permissions import IsBookingOwner, IsOrganizer, IsAdminOrReadOnly


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOrganizer()]
        return [AllowAny()]

    

class TicketTypeViewSet(ReadOnlyModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketTypeFilter
    

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsBookingOwner()]
        return [IsAuthenticated()]

    

class BookingItemViewSet(ModelViewSet):
    serializer_class = BookingItemSerializer

    def get_queryset(self):
        return BookingItem.objects.filter(
            booking__user=self.request.user
        )

    def get_permissions(self):
        return [IsAuthenticated()]