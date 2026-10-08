from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        # set_password hashes the password automatically (replacing your password_hash field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, full_name, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Note: password and last_login fields are automatically provided by AbstractBaseUser

    objects = UserManager()

    USERNAME_FIELD = 'email'  # This tells SimpleJWT and Django to use email for login
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_status = models.BooleanField(default=False)
    currency_preference = models.CharField(max_length=10, default='USD')
    notification_preference = models.CharField(max_length=50)
    profile_image = models.URLField(blank=True, null=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):

    class PaymentModes(models.TextChoices):
        CASH = "CS", _("Cash")
        CARD = "CD", _("Card")
        CHECK = "CK", _("Check")
        ETRANSFER = "ET", _("E-Transfer")

    class TransactionTypes(models.TextChoices):
        EXPENSE = "EX", _("Expense")
        INCOME = "IN", _("Income")

    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50) # e.g., income, expense
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    payment_mode = models.CharField(max_length=50, choices = PaymentModes)
    receipt_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    alert_threshold = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 80.00 for 80%
    created_at = models.DateTimeField(auto_now_add=True)

class SavingsGoal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    target_date = models.DateField()
    monthly_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    date_range = models.CharField(max_length=100)
    generated_on = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField()

class LearningContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100)
    body = models.TextField()
    difficulty_level = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class SupportQuery(models.Model):
    query_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50, default='Open')
    admin_response = models.TextField(blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)