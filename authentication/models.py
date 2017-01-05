from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from app.models import Company


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
                
        return user

    def create_superuser(self, email, password):
        """
        Create and save a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    TITLES = (
        ('CIP Manager', 'CIP Manager'),
        ('Alternate CIP Manager', 'Alternate CIP Manager'),
        ('Access Control Engineer', 'Access Control Engineer'),
        ('Training Coordinator', 'Training Coordinator'),
        ('Human Resources', 'Human Resources')
    )

    email = models.EmailField(max_length=80, unique=True)

    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)

    company = models.ForeignKey(Company, null=True, blank=True)
    title = models.CharField(max_length=80, choices=TITLES, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
