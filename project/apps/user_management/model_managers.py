from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, secondary_email, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username and not password:
            raise ValueError("The given username or password must be set")
        email = self.normalize_email(email)
        secondary_email = self.normalize_email(secondary_email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            secondary_email=secondary_email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, username, email=None, password=None, secondary_email=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("email_confirmed", False)
        return self._create_user(
            username, email, password, secondary_email, **extra_fields
        )

    def create_superuser(
        self, username, email=None, password=None, secondary_email=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_confirmed", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            username, email, password, secondary_email, **extra_fields
        )
