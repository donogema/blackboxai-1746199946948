from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('SUPER', 'Super Admin'),
        ('ADMIN', 'Administrator'),
        ('STAFF', 'Staff Member'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def is_super_admin(self):
        return self.role == 'SUPER'
        
    def is_admin(self):
        return self.role in ['SUPER', 'ADMIN']
