from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='users:dashboard', permanent=False)),
    path('users/', include('apps.users.urls')),
    # These will be implemented later
    # path('invoices/', include('apps.invoices.urls')),
    # path('customers/', include('apps.customers.urls')),
    # path('reports/', include('apps.reports.urls')),
    # path('leave/', include('apps.leave.urls')),
    # path('timeoff/', include('apps.timeoff.urls')),
    # path('salary-advance/', include('apps.salaryadvance.urls')),
    # path('core/', include('apps.core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
