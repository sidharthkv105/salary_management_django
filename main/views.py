from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.mail import send_mail
from .models import Salary
from django.utils.timezone import now
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
import random
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from reportlab.lib.styles import getSampleStyleSheet

from .models import Salary

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            login(request, user)

            messages.success(request, 'Registration successful! Welcome email sent.')

            # Send Welcome Email
            send_mail(
                subject='Welcome to Salary Management System!',
                message=f'Hi {username},\n\nThank you for signing up. Welcome aboard!',
                from_email='your-email@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect('login')

    return render(request, 'main/signup.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'main/login.html')

        # Authenticate using username (because Django auth works with username internally)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid password.')

    return render(request, 'main/login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            request.session['reset_code'] = code
            request.session['reset_email'] = email

            # Send email
            subject = 'Password Reset Code'
            message = f'Your password reset code is: {code}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')

    return render(request, 'main/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        new_password = request.POST.get('password')

        if entered_code == request.session.get('reset_code'):
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)

            user.password = make_password(new_password)
            user.save()

            # Clear session
            request.session.pop('reset_code', None)
            request.session.pop('reset_email', None)

            messages.success(request, 'Password reset successfully. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid code.')
            return redirect('reset_password')

    return render(request, 'main/reset_password.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

@login_required
def add_salary(request):
    if request.method == 'POST':
        salary = Salary(
            salary_date=request.POST.get('salary_date'),
            pay=float(request.POST.get('pay')),
            da=float(request.POST.get('da')),
            hra=float(request.POST.get('hra')),
            allowance=float(request.POST.get('allowance')),
            co_date=request.POST.get('co_date'),
            gpf=float(request.POST.get('gpf')),
            sli=float(request.POST.get('sli')),
            gis=float(request.POST.get('gis')),
            lic=float(request.POST.get('lic')),
            medisep=float(request.POST.get('medisep')),
            gpais=float(request.POST.get('gpais')),
            pro_tax=float(request.POST.get('pro_tax')),
            i_tax=float(request.POST.get('i_tax')),
        )
        salary.save()
        return redirect('view_salary')

    return render(request, 'main/add_salary.html')

@login_required
def view_salary(request):
    current_year = now().year

    # Get the selected year from the query parameter (default to current year)
    selected_year = request.GET.get('year', current_year)

    # Filter salaries by the selected year
    salaries = Salary.objects.filter(salary_date__year=selected_year).order_by('salary_date')

    # Get list of all available years in the table to populate dropdown
    all_years = Salary.objects.dates('salary_date', 'year')

    context = {
        'salaries': salaries,
        'selected_year': int(selected_year),
        'all_years': [date.year for date in all_years]
    }
    return render(request, 'main/view_salary.html', context)

@login_required
def download_salary_pdf(request, year):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="salary_records_{year}.pdf"'

    # Create the PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    
    # Styles for heading
    styles = getSampleStyleSheet()

    # Heading with year and username
    heading_text = f"<b>Salary Details - {year}</b><br/>{request.user.username}"
    heading = Paragraph(heading_text, styles['Title'])
    elements.append(heading)
    elements.append(Spacer(1, 12))  # Add some space after heading

    # Table Header
    table_data = [
        ["Salary Date", "C/O Date", "Pay", "DA", "HRA", "Allowance", "Gross", "GPF", "SLI", "GIS",
         "LIC", "MEDISEP", "GPAIS", "PRO TAX", "I TAX", "Deduction", "Net"]
    ]

    # Get salary records for the year
    salaries = Salary.objects.filter(salary_date__year=year).order_by('salary_date')

    for salary in salaries:
        table_data.append([
            salary.salary_date, salary.co_date, salary.pay, salary.da, salary.hra, salary.allowance,
            salary.gross, salary.gpf, salary.sli, salary.gis, salary.lic, salary.medisep, salary.gpais,
            salary.pro_tax, salary.i_tax, salary.deduction, salary.net
        ])

    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Build PDF
    pdf.build(elements)
    return response


@login_required
def edit_salary(request, id):
    salary = get_object_or_404(Salary, id=id)

    if request.method == 'POST':
        salary.salary_date = request.POST.get('salary_date')
        salary.co_date = request.POST.get('co_date')
        salary.pay = float(request.POST.get('pay'))
        salary.da = float(request.POST.get('da'))
        salary.hra = float(request.POST.get('hra'))
        salary.allowance = float(request.POST.get('allowance'))
        salary.gpf = float(request.POST.get('gpf'))
        salary.sli = float(request.POST.get('sli'))
        salary.gis = float(request.POST.get('gis'))
        salary.lic = float(request.POST.get('lic'))
        salary.medisep = float(request.POST.get('medisep'))
        salary.gpais = float(request.POST.get('gpais'))
        salary.pro_tax = float(request.POST.get('pro_tax'))
        salary.i_tax = float(request.POST.get('i_tax'))

        salary.gross = salary.pay + salary.da + salary.hra + salary.allowance
        salary.deduction = salary.gpf + salary.sli + salary.gis + salary.lic + salary.medisep + salary.gpais + salary.pro_tax + salary.i_tax
        salary.net = salary.gross - salary.deduction

        salary.save()
        messages.success(request, 'Salary updated successfully!')
        return redirect('view_salary')

    return render(request, 'main/edit_salary.html', {'salary': salary})

@login_required
def delete_salary(request, id):
    salary = get_object_or_404(Salary, id=id)
    salary.delete()
    messages.success(request, 'Salary deleted successfully!')
    return redirect('view_salary')

@login_required
def logout_view(request):
    logout(request)  # ✅ This logs the user out
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Redirect to the login page

