from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)
        if password:  # Ensure password is hashed properly
            user.set_password(password)
        else:
            raise ValueError("Password must be set")

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)  # New field for phone verification
    email_verified_at = models.DateTimeField(null=True, blank=True)  # New field for email verification
    password = models.CharField(max_length=128)
    organization = models.CharField(max_length=255, null=True, blank=True)  # New field for organization
    profession = models.CharField(max_length=255, null=True, blank=True)  # New field for profession
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)  # New field for address
    city = models.CharField(max_length=255, null=True, blank=True)  # New field for city
    facebook_link = models.URLField(null=True, blank=True)  # New field for Facebook link
    x_link = models.URLField(null=True, blank=True)  # New field for X (formerly Twitter) link
    instagram_link = models.URLField(null=True, blank=True)  # New field for Instagram link
    linkedin_link = models.URLField(null=True, blank=True)  # New field for LinkedIn link
    youtube_link = models.URLField(null=True, blank=True)  # New field for YouTube link
    profile_image = models.ImageField(upload_to="users/", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "name"]

    def __str__(self):
        return self.username
    


class Category(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    category_level = models.IntegerField(default=1)  # Default to 1

    def __str__(self):
        return self.name
    

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    html_body = models.TextField()
    css_body = models.TextField()
    preview_image = models.ImageField(upload_to='documents/previews/', blank=True, null=True)
    mockup_image = models.ImageField(upload_to='documents/mockups/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.FileField(upload_to='documents/files/', blank=True, null=True)

    def __str__(self):
        return self.title


class DocumentCategory(models.Model):
    # Assuming Category with ID 1 exists
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="document_categories", default=1) 
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_id.title} - Level {self.level}"



class DocumentMeta(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    css = models.TextField(blank=True, null=True)
    attribute_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.key or 'No Key'}"
    

class Font(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    font_family = models.CharField(max_length=255)

    def __str__(self):
        return self.name
