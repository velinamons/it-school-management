from django.db import models


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Completed', 'Completed'),
    ]
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True, max_length=255)
    suggested_course = models.CharField(max_length=50, null=True)
    suggestion_details = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
