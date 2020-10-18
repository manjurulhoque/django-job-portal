from typing import Dict, Optional, Union

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(
        self, email: str, password: str, **extra_fields: Dict[str, Union[str, bool]]
    ) -> object:
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Dict[str, Union[str, bool]]
    ) -> object:
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)  # type: ignore
        extra_fields.setdefault("is_superuser", False)  # type: ignore
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: Dict[str, Union[str, bool]]
    ) -> object:
        """Create and save a SuperUser with the given email and password."""
        # extra_fields: Dict[str, Union[str, bool]]
        extra_fields.setdefault("is_staff", True)  # type: ignore
        extra_fields.setdefault("is_superuser", True)  # type: ignore

        if extra_fields.get("is_staff") is not True:  # type: ignore
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:  # type: ignore
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
