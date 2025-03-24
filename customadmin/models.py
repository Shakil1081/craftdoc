from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from django.contrib.contenttypes.models import ContentType
from rolepermissions.roles import assign_role
from django.db import models
from customadmin.roles import Admin, Staff

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Save the user first

        # Assign the user to selected groups and their associated permissions
        self.assign_groups_and_permissions(user)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

    def assign_groups_and_permissions(self, user):
        """Assign permissions to user based on selected groups."""
        # Get all groups the user is part of
        groups = user.groups.all()

        # Loop through all selected groups and assign permissions
        for group in groups:
            self.assign_permissions(user, group)

    def assign_permissions(self, user, group):
        """Assign permissions of a group to the user."""
        permissions = group.permissions.all()
        for permission in permissions:
            user.user_permissions.add(permission)

        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="users/", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "name"]

    def save(self, *args, **kwargs):
        """Ensure user is assigned to groups and permissions on creation"""
        is_new = self.pk is None  # Check if the user is being created for the first time
        super().save(*args, **kwargs)  # Save first

        if is_new:  # Assign permissions and groups only for new users
            User.objects.assign_groups_and_permissions(self)

    def __str__(self):
        return self.username
