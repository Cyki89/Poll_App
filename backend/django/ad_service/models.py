from django.db import models
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
)


class ADGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class ADUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        ADGroup,
        blank=True,
        related_name="users",
        related_query_name="user",
    )

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def __str__(self):
        return self.username
