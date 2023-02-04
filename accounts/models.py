from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
import uuid

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=False)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    # theme = models.CharField(max_length=30, default="light")
    # profile_pic = models.ImageField(null=True, blank=True, default="images/default.png", upload_to=upload_path)

    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # @classmethod
    # def get_activate_url(cls, request, user):
    #     site = "bitwatch.net"
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     token = accounts_activation_token.make_token(user)
    #     return f"{site}/api/account/activate/{uid}/{token}"
    
    # @classmethod
    # def get_password_reset_url(cls, request, user):
    #     site = "bitwatch.net"
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     token = accounts_activation_token.make_token(user)
    #     return f"{site}/resetpassword?uid={uid}&token={token}"