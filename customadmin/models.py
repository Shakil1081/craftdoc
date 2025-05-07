from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from django.utils.crypto import get_random_string
from decimal import Decimal
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
    phone = models.CharField(max_length=15, null=True, blank=True)
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
    email_verify_token = models.CharField(max_length=150, null=True, blank=True)
    password_reset_token = models.CharField(max_length=150, null=True, blank=True)
    user_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "name"]

    def generate_verification_token(self):
        """Generate and store a 150-character verification token"""
        self.email_verify_token = get_random_string(100)
        self.save()
        return self.email_verify_token
    
    def generate_password_reset_token(self):
        """Generate and store a 150-character verification token"""
        self.password_reset_token = get_random_string(100)
        self.save()
        return self.password_reset_token
    
    def verify_email(self):
        """Mark email as verified and clear the token"""
        self.email_verified_at = timezone.now()
        self.is_active = True  # Activate account if not already active
        self.save()

    def __str__(self):
        return self.username
    
    def change_credit(self, amount, description="", target_type="", target_id=None, allow_negative=False):
        """
        Change user credit by adding or deducting.
        """
        if self.user_credit is None:
            self.user_credit = Decimal("0.00")

        new_credit = self.user_credit + Decimal(amount)

        if not allow_negative and new_credit < 0:
            raise ValueError("Insufficient credit.")

        self.user_credit = new_credit
        self.save()

        if amount > 0:
            CreditEarnHistory.objects.create(
                user=self,
                earned_credit=Decimal(amount),
                description=description,
                target_type=target_type,
                target_id=target_id or 0
            )
        else:
            CreditUsesHistory.objects.create(
                user=self,
                usage_credit=abs(Decimal(amount)),
                description=description,
                target_type=target_type,
                target_id=target_id or 0
            )


    def earn_credit(self, setting_key, allow_negative=False):
        """
        Earn credit using a value from Setting by key.
        """
        setting = Setting.objects.get(key=setting_key)
        self.change_credit(
            amount=abs(Decimal(setting.value)),
            description=setting.title,
            target_type=setting.key,
            target_id=setting.id,
            allow_negative=allow_negative
        )


    def use_credit(self, setting_key, allow_negative=False):
        """
        Use credit using a value from Setting by key.
        """
        setting = Setting.objects.get(key=setting_key)
        self.change_credit(
            amount=-abs(Decimal(setting.value)),
            description=setting.title,
            target_type=setting.key,
            target_id=setting.id,
            allow_negative=allow_negative
        )

class Category(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    category_level = models.IntegerField(default=1)  # Default to 1

    def __str__(self):
        return self.name
    

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo_path = models.FileField(upload_to='documents/files/')
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class DocumentCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="document_categories", default=1)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  # This is the renamed field
    level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.document.title} - Level {self.level}"


class DocumentMeta(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  # This should be the renamed field
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
    url = models.URLField(max_length=1000)
    font_family = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CreditEarnHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=100)
    target_id = models.IntegerField()
    description = models.TextField()
    earned_credit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.earned_credit}"

class CreditUsesHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=100)
    target_id = models.IntegerField()
    description = models.TextField()
    usage_credit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.usage_credit}"
    
class DocumentHeaderFooterImage(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='header_footer_images')
    color = models.CharField(max_length=50, blank=True, null=True)
    css = models.CharField(blank=True, null=True)
    header = models.ImageField(upload_to='documents/previews/')
    footer = models.ImageField(upload_to='documents/previews/')
    preview_image = models.ImageField(upload_to='documents/previews/', blank=True, null=True)
    is_default = models.BooleanField(null=True)

    def __str__(self):
        return f"Header/Footer for {self.document.title}"

    
class SettingManager(models.Manager):
    def get_value(self, key, default=None):
        try:
            return self.get(key=key).value
        except Setting.DoesNotExist:
            return default

class Setting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    objects = SettingManager()

    def __str__(self):
        return f"{self.title} ({self.key})"

class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    document_hf = models.ForeignKey(DocumentHeaderFooterImage, on_delete=models.CASCADE)
    logo_path = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    css = models.TextField(blank=True)
    header_path = models.CharField(max_length=255, blank=True)
    footer_path = models.CharField(max_length=255, blank=True)
    download_type = models.CharField(max_length=10)  # 'pdf', 'jpg', 'png'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.created_at})"