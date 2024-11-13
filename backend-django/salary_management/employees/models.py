from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_joining = models.DateField()
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class AdminProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=255)
    image = models.ImageField(upload_to='admin_images/', null=True, blank=True)

    def __str__(self):
        return f"Admin Profile of {self.user.username}"
