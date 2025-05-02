from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LeaveApplication
from .forms import LeaveApplicationForm

@login_required
def leave_list(request):
    if request.user.is_super_admin():
        leaves = LeaveApplication.objects.all().order_by('-submitted_at')
    else:
        leaves = LeaveApplication.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'leave/leave_list.html', {'leaves': leaves})

@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, 'Leave application submitted successfully.')
            return redirect('leave:leave_list')
    else:
        form = LeaveApplicationForm()
    return render(request, 'leave/leave_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_super_admin())
def leave_review(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = 'approved'
            leave.save()
            messages.success(request, 'Leave application approved.')
        elif action == 'reject':
            leave.status = 'rejected'
            leave.save()
            messages.success(request, 'Leave application rejected.')
        return redirect('leave:leave_list')
    return render(request, 'leave/leave_review.html', {'leave': leave})
