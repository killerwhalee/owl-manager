from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Custom User Manager

    """

    use_in_migrations = True

    def create_user(self, user_email, user_code, password=None):
        user = self.model(user_email=user_email, user_code=user_code.upper())
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, user_email, password):
        user = self.create_user(user_email, "passwd", password)

        # Set admin permissions
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model

    User email is used as username. It means email should be unique.

    """

    import uuid

    objects = UserManager()

    # Core user informations for authentication
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_email = models.EmailField(max_length=254, null=False, unique=True)
    user_code = models.CharField("User Code", max_length=2, blank=True)

    # Basic permissions overwritten
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "user_email"
    EMAIL_FIELD = "user_email"


class Profile(models.Model):
    """
    User Profile Model

    Any field which does NOT related to user authentication goes here.

    """

    from towel.utils import uuid_filepath

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(
        "Profile image",
        upload_to=uuid_filepath,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
