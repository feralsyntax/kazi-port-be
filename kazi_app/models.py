from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager
)
from django.utils import timezone
import uuid

# Create your models here.

class CustomAccountManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with an email, and password.
        """

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with an email and password.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, 
            password, 
            **extra_fields
        )

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with an email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            email, 
            password, 
            **extra_fields
        )
        

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email and password authentication.
    """

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    university = models.CharField(
        _("university"), 
        max_length=255, 
        blank=True, 
    )
    course = models.CharField(
        _("course"), 
        max_length=255, 
        blank=True, 
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomAccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        
    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return self.email