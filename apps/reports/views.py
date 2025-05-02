from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from apps.invoices.models import Invoice
from apps.customers.models import Customer
from .forms import ReportFilterForm
import openpyxl
from django.template.loader import render_to_string
from xhtml2pdf import pisa

@login_required
def report_dashboard(request):
    form = ReportFilterForm(request.GET or None)
    invoices = Invoice.objects.all()
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        customer_name = form.cleaned_data.get('customer')
        if start_date:
            invoices = invoices.filter(created_date__gte=start_date)
        if end_date:
            invoices = invoices.filter(created_date__lte=end_date)
        if customer_name:
            invoices = invoices.filter(customer__name__icontains=customer_name)
    income = invoices.aggregate(total_income=Sum('total'))['total_income'] or 0
    context = {
        'form': form,
        'invoices': invoices,
        'income': income,
    }
    return render(request, 'reports/report_dashboard.html', context)

@login_required
def export_report_pdf(request):
    form = ReportFilterForm(request.GET or None)
    invoices = Invoice.objects.all()
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        customer_name = form.cleaned_data.get('customer')
        if start_date:
            invoices = invoices.filter(created_date__gte=start_date)
        if end_date:
            invoices = invoices.filter(created_date__lte=end_date)
        if customer_name:
            invoices = invoices.filter(customer__name__icontains=customer_name)
    context = {'invoices': invoices}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    html = render_to_string('reports/report_pdf.html', context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF report')
    return response

@login_required
def export_report_excel(request):
    form = ReportFilterForm(request.GET or None)
    invoices = Invoice.objects.all()
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        customer_name = form.cleaned_data.get('customer')
        if start_date:
            invoices = invoices.filter(created_date__gte=start_date)
        if end_date:
            invoices = invoices.filter(created_date__lte=end_date)
        if customer_name:
            invoices = invoices.filter(customer__name__icontains=customer_name)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(['Invoice Number', 'Customer', 'Date', 'Total'])
    for invoice in invoices:
        ws.append([invoice.invoice_number, invoice.customer.name, invoice.created_date.strftime('%Y-%m-%d'), float(invoice.total)])
    wb.save(response)
    return response
