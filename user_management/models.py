from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import re
class CustomUserManager(BaseUserManager):
    def create_user(self, email, student_id, gender, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email is required")
        if not student_id:
            raise ValueError("Student ID is required")
        if not gender:
            raise ValueError("Gender is required")

        # تحقق من أن الايميل ينتمي لنطاق جامعة "ses.yu.edu.jo"
        if not re.match(r'.+@ses\.yu\.edu\.jo$', email):
            raise ValueError("Email must be a university email (e.g., name@ses.yu.edu.jo)")

        if not student_id.isdigit():
            raise ValueError("Student ID must contain only digits")
        if len(student_id) != 10:
            raise ValueError("Student ID must be exactly 10 digits")

        email = self.normalize_email(email)
        user = self.model(email=email, student_id=student_id, gender=gender, **extra_fields)
        
        if not password:
            raise ValueError("Password is required")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, student_id, gender, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, student_id, gender, password, **extra_fields)


#Custom User Model : This model is used when you need to customize user data,
#rather than using the default model provided by Django.

#AbstractBaseUser : Provides basic user properties such as password and login.
#PermissionsMixin : Adds support for permissions and groups.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    )

    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True) #It is automatically generated when the user is created.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' #users login using email instead of traditional username
    REQUIRED_FIELDS = ['student_id', 'gender']

    def __str__(self):
        return self.email
