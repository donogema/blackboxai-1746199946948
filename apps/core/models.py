from django.db import models

class OrganizationProfile(models.Model):
    organization_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    enable_invoices = models.BooleanField(default=True)
    enable_customers = models.BooleanField(default=True)
    enable_reports = models.BooleanField(default=True)
    enable_leave = models.BooleanField(default=True)
    enable_timeoff = models.BooleanField(default=True)
    enable_salaryadvance = models.BooleanField(default=True)

    def __str__(self):
        return self.organization_name
