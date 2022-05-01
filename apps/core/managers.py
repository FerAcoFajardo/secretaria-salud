from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to deal with the custom user model
    """

    def create_user(self, cedula_profesional, huella=None, **kwargs):
        if not cedula_profesional:
            raise ValueError('Users must have a cedula_profesional')

        user = self.model(
            cedula_profesional=cedula_profesional,
            huella=huella
        )

        user.save()
        return user

    def create_superuser(self, cedula_profesional, huella=None, **kwargs):
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cedula_profesional, huella, **kwargs)
