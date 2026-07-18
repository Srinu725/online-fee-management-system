from django.shortcuts import render,redirect
from django.http import HttpResponse
from FinalApp.forms import AccountantRegisterForm,StudentRegisterForm
from FinalApp.models  import AccountantProfile,StudentProfile
from django.contrib.auth import authenticate,login
from django.db.models import Sum
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User



# Create your views here.
def navbar(request):
    return render(request,'navbar.html',{})

def about(request):
    return render(request,'about.html',{})

def contact(request):
    return render(request,'contact.html',{})

def student(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(username=username, password=password)

        if u is not None and not u.is_staff and not u.is_superuser:
            login(request, u) 
            return redirect('/balance')  
        else:
            return HttpResponse("<h2>Invalid</h2>")

    return render(request, 'student.html')
def staff(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        u=authenticate(username=username,password=password)
        if u:
            return redirect('/dashboard')
        else:
            return HttpResponse("<h2>Invalid</h2>")
    return render(request,"staff.html",{})

def admin1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/') 
        else:
            return render(request, 'admin1.html', {'error': 'Invalid credentials or not an admin'})

    return render(request, 'admin1.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student')  
    else:
        form = StudentRegisterForm()  

    return render(request, 'register_student.html', {'form': form}) 

def register_accountant(request):
    if request.method == 'POST':
        form = AccountantRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return render(request, 'register_accountant.html', {'form': form})

            user = form.save()
            
          
            messages.success(request, "Accountant registered successfully!")
            return redirect('/staff') 
    else:
        form = AccountantRegisterForm()

    return render(request, 'register_accountant.html', {'form': form})
   

def dashboard(request):
    students = StudentProfile.objects.select_related('student_user')
    total_students = students.count()
    total_collected = students.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expected = students.aggregate(total=Sum('total_fee'))['total'] or 0
    total_balance = total_expected - total_collected

    context = {
        'students': students,
        'total_students': total_students,
        'total_collected': total_collected,
        'total_balance': total_balance
    }
    return render(request, 'dashboard.html', context)

class UpdateFeeForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['amount_paid', 'total_fee']


def update_fee(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        new_amount = float(request.POST.get('amount_paid'))
        student.amount_paid = new_amount
        student.save()
        messages.success(request, "Fee updated successfully!")
        return redirect('/dashboard')

    return render(request, 'update_fee.html', {'student': student})



def balance_view(request):
    if request.user.is_authenticated:
        student = get_object_or_404(StudentProfile, student_user=request.user)
        return render(request, 'balance.html', {'student': student})
    else:
        return redirect('/student')  

def make_payment(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0.")
        elif amount > student.balance():
            messages.error(request, "You cannot pay more than the balance.")
        else:
            student.amount_paid += amount
            student.save()
            messages.success(request, f"Payment of ₹{amount} successful!")
            return redirect('/balance', student_id=student.id)

    return render(request, 'make_payment.html', {'student': student})