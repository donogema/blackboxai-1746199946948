from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import OrganizationProfile
from .forms import OrganizationProfileForm

@login_required
@user_passes_test(lambda u: u.is_super_admin())
def organization_profile(request):
    profile, created = OrganizationProfile.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = OrganizationProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization profile updated successfully.')
            return redirect('core:organization_profile')
    else:
        form = OrganizationProfileForm(instance=profile)
    return render(request, 'core/organization_profile.html', {'form': form})
