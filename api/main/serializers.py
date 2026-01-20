from rest_framework import serializers
from main.models import Event, TicketType, Booking, BookingItem
from django.db.models import Sum


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True, source='tickettype_set')

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        start = attrs.get('start_datetime')
        end = attrs.get('end_datetime')
        if start and end and start >= end:
            raise serializers.ValidationError("Дата начала должна быть раньше конца")
        return attrs



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = '__all__'

    def validate(self, attrs):
        ticket_type = attrs.get('ticket_type')
        quantity = attrs.get('quantity')

        if ticket_type and quantity:
            total_booked = BookingItem.objects.filter(ticket_type=ticket_type).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            if total_booked + quantity > ticket_type.total_quantity:
                raise serializers.ValidationError("Недостаточно билетов")
        return attrs
