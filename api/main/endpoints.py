from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .class_api import EventViewSet, TicketTypeViewSet, BookingViewSet, BookingItemViewSet

router = DefaultRouter()

router.register(r'events', EventViewSet, basename='event')
router.register(r'ticket-types', TicketTypeViewSet, basename='tickettype')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'booking-items', BookingItemViewSet, basename='bookingitem')

urlpatterns = [
    path('', include(router.urls)), 
]