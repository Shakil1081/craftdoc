from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from django.contrib.contenttypes.models import ContentType
from rolepermissions.roles import assign_role
from django.db import models
from customadmin.roles import Admin, Staff

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='staff', **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", role == 'admin')  # Only admins are staff

        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Save the user first

        # Assign role (convert role string to class)
        self.assign_role_and_permissions(user, role)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, role='admin', **extra_fields)

    def assign_role_and_permissions(self, user, role):
        """Assigns a role, permissions, and ensures the user is added to the correct group."""
        if role == 'staff':
            assign_role(user, Staff)
            self.assign_permissions(user, ["view_users"])
            self.assign_group(user, "Staff")  # Ensure the user is added to the 'Staff' group

        elif role == 'admin':
            assign_role(user, Admin)
            self.assign_permissions(user, ["view_users", "add_user", "edit_user", "delete_user"])
            self.assign_group(user, "Admin")  # Ensure the user is added to the 'Admin' group

        user.save()

    def assign_permissions(self, user, permissions):
        """Assigns Django built-in permissions to user"""
        content_type = ContentType.objects.get_for_model(User)  # Get user model content type
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm, content_type=content_type)
                user.user_permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"⚠️ Warning: Permission '{perm}' does not exist!")

        user.save()

    def assign_group(self, user, group_name):
        """Assigns user to a Django auth group"""
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
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
    is_staff = models.BooleanField(default=False)  # Only admins are staff by default

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "name"]

    def save(self, *args, **kwargs):
        """Ensure users get a role and group upon creation but prevent infinite recursion."""
        is_new = self.pk is None  # Check if the user is being created for the first time
        super().save(*args, **kwargs)  # Save first before assigning role

        if is_new:  # Assign roles and permissions only for new users
            User.objects.assign_role_and_permissions(self, self.role)


    def __str__(self):
        return self.username
