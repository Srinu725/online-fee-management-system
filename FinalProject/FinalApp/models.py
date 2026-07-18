from django.db import models
from django.contrib.auth.models import User

class AccountantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.employee_id})"

class StudentProfile(models.Model):
    student_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=25000)

    def __str__(self):
        return f"{self.student_user.username} - Student"

    def balance(self):
        return self.total_fee - self.amount_paid