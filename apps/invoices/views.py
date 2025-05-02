from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet
import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import openpyxl

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_date')
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.subtotal = 0
            invoice.tax = 0
            invoice.discount = 0
            invoice.total = 0
            invoice.save()
            formset.instance = invoice
            formset.save()
            # Calculate totals
            subtotal = sum(item.total_price for item in invoice.items.all())
            invoice.subtotal = subtotal
            invoice.total = subtotal + invoice.tax - invoice.discount
            invoice.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoices:invoice_list')
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    return render(request, 'invoices/invoice_form.html', {'form': form, 'formset': formset})

@login_required
def export_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    template_path = 'invoices/invoice_pdf.html'
    context = {'invoice': invoice}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def export_invoice_excel(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.invoice_number}.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Invoice"
    ws.append(['Invoice Number', invoice.invoice_number])
    ws.append(['Customer', invoice.customer.name])
    ws.append(['Date', invoice.created_date.strftime('%Y-%m-%d')])
    ws.append([])
    ws.append(['Description', 'Quantity', 'Unit Price', 'Total Price'])
    for item in invoice.items.all():
        ws.append([item.description, item.quantity, float(item.unit_price), float(item.total_price)])
    ws.append([])
    ws.append(['Subtotal', float(invoice.subtotal)])
    ws.append(['Tax', float(invoice.tax)])
    ws.append(['Discount', float(invoice.discount)])
    ws.append(['Total', float(invoice.total)])
    wb.save(response)
    return response
