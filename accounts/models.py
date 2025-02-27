from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular User with the given email and password."""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_recruiter(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_recruiter', True)
        return self.create_user(email, password, **extra_fields)

    def create_candidate(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_candidate', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'))
    username = None
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=255, null=True, unique=True)
    mobile_regex = RegexValidator(
        regex=r'^[6-9][0-9]{9}$',
        message="Phone number must be entered in the format: '8080809804'. \
             Only 10 digits allowed.")
    mobile = models.CharField(
        validators=[mobile_regex], max_length=15, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='other')
    dob = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'first_name', 'last_name']
    objects = UserManager()

    def _str_(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
