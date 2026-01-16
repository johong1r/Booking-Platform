from django.contrib import admin
from .models import Event, TicketType, Booking, BookingItem


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_datetime', 'end_datetime', 'location', 'is_online', 'organizer')
    search_fields = ('title', 'location', 'organizer__username')
    list_filter = ('is_online', 'start_datetime')
    ordering = ('-start_datetime',)


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'status', 'price', 'total_quantity')
    search_fields = ('event__title', 'status')
    list_filter = ('status',)
    ordering = ('event',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):   
    list_display = ('id', 'user', 'status', 'created_at')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'ticket_type', 'quantity')
    search_fields = ('booking__user__username', 'ticket_type__event__title')
    ordering = ('-id',)


    