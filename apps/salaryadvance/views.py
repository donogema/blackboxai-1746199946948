from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SalaryAdvance
from .forms import SalaryAdvanceForm

@login_required
def salaryadvance_list(request):
    if request.user.is_super_admin():
        advances = SalaryAdvance.objects.all().order_by('-submitted_at')
    else:
        advances = SalaryAdvance.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'salaryadvance/salaryadvance_list.html', {'advances': advances})

@login_required
def salaryadvance_request(request):
    if request.method == 'POST':
        form = SalaryAdvanceForm(request.POST)
        if form.is_valid():
            advance = form.save(commit=False)
            advance.user = request.user
            advance.save()
            messages.success(request, 'Salary advance request submitted successfully.')
            return redirect('salaryadvance:salaryadvance_list')
    else:
        form = SalaryAdvanceForm()
    return render(request, 'salaryadvance/salaryadvance_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_super_admin())
def salaryadvance_review(request, pk):
    advance = get_object_or_404(SalaryAdvance, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            advance.status = 'approved'
            advance.save()
            messages.success(request, 'Salary advance request approved.')
        elif action == 'reject':
            advance.status = 'rejected'
            advance.save()
            messages.success(request, 'Salary advance request rejected.')
        return redirect('salaryadvance:salaryadvance_list')
    return render(request, 'salaryadvance/salaryadvance_review.html', {'advance': advance})
