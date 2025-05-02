from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import TimeOffRequest
from .forms import TimeOffRequestForm

@login_required
def timeoff_list(request):
    if request.user.is_super_admin():
        requests = TimeOffRequest.objects.all().order_by('-submitted_at')
    else:
        requests = TimeOffRequest.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'timeoff/timeoff_list.html', {'requests': requests})

@login_required
def timeoff_apply(request):
    if request.method == 'POST':
        form = TimeOffRequestForm(request.POST)
        if form.is_valid():
            timeoff = form.save(commit=False)
            timeoff.user = request.user
            timeoff.save()
            messages.success(request, 'Time off request submitted successfully.')
            return redirect('timeoff:timeoff_list')
    else:
        form = TimeOffRequestForm()
    return render(request, 'timeoff/timeoff_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_super_admin())
def timeoff_review(request, pk):
    timeoff = get_object_or_404(TimeOffRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            timeoff.status = 'approved'
            timeoff.save()
            messages.success(request, 'Time off request approved.')
        elif action == 'reject':
            timeoff.status = 'rejected'
            timeoff.save()
            messages.success(request, 'Time off request rejected.')
        return redirect('timeoff:timeoff_list')
    return render(request, 'timeoff/timeoff_review.html', {'timeoff': timeoff})
