from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    display_name = models.CharField(max_length=64, blank=True)

    @property
    def shown_name(self) -> str:
        return self.display_name or self.get_full_name() or self.get_username()

    @property
    def profile_initials(self) -> str:
        parts = self.shown_name.replace(".", " ").split()
        letters = "".join(part[0] for part in parts[:2])
        return (letters or self.get_username()[:1] or "?").upper()
