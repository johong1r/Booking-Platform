from django.db import models
from accounts.models import User


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=1500, verbose_name='Описание')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=150, verbose_name='Локация')
    is_online = models.BooleanField(verbose_name='Действует', default=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f"{self.id} - {self.title}"
    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class TicketType(models.Model):
    STATUS_CHOICES = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),
        ('student', 'Student'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='standard')
    price = models.PositiveIntegerField(verbose_name='Цена')
    total_quantity = models.IntegerField(verbose_name='Общее количество')
    def __str__(self):
        return f"{self.id} - {self.event}"
    
    class Meta:
        verbose_name = 'Тип билета'
        verbose_name_plural = 'типы билетов'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('basket', 'Basket'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='basket')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user}"
    
    class Meta:
        verbose_name = 'Бронирования'
        verbose_name_plural = 'Бронирование'


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.id} - {self.booking}"
    
    class Meta:
        verbose_name = 'Элемент бронирования'
        verbose_name_plural = 'Элементы бронирования'