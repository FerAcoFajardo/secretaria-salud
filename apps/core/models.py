from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .managers import CustomUserManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    cedula_profesional = models.CharField('Cedula profesional', max_length=50, unique=True)
    huella = models.ImageField('Huella',upload_to='huellas/', max_length=10485760)
    nombre = models.CharField('Nombre', max_length=50)
    correo = models.EmailField('Correo', max_length=50, unique=True)
    telefono = models.CharField('Telefono', max_length=50)
    is_superuser = models.BooleanField('Es superusuario', default=False)
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Es staff', default=False)

    USERNAME_FIELD = 'cedula_profesional'
    REQUIRED_FIELDS = ['nombre', 'correo', 'telefono']

    objects = CustomUserManager()

    def __str__(self):
        return self.cedula_profesional

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['cedula_profesional']


class Common(models.Model):
    """Modelo base para todos los modelos
    
    Este modelo hereda de models.Model, que es el modelo base de Django.
    
    ``created_by``
        Una llave foranea que apunta a la tabla ``Usuario``.

    """
    created_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class Paciente(Common):
    
    class TipoSangre(models.TextChoices):
        AP = 'AP', 'A+'
        AN = 'AN', 'A-'
        BP = 'BP', 'B+'
        BN = 'BN', 'B-'
        ABP = 'ABP', 'AB+'
        OP = 'OP', 'O+'
        ON = 'ON', 'O-'
    
    class Sexo(models.TextChoices):
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMENINO = 'FEMENINO', 'Femenino'
        OTRO = 'OTRO', 'Otro'
    
    nombre = models.CharField('Nombre', max_length=50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', auto_now=False, auto_now_add=False)
    curp = models.CharField('CURP', max_length=50)
    huella = models.ImageField('Huella',upload_to='huellas/', max_length=10485760)
    correo = models.EmailField('Correo', max_length=254)
    telefono = models.CharField('Telefono', max_length=50)
    tipo_sangre = models.CharField('Tipo de sangre', choices=TipoSangre.choices, max_length=3)
    sexo = models.CharField('Sexo', choices=Sexo.choices, null=True, blank=True, max_length=30)
    es_menor = models.BooleanField('Es menor', default=False)
    tutor = models.ForeignKey(verbose_name='Tutor', to='self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nombre']
    

class Expediente(Common):
    paciente = models.OneToOneField(verbose_name='Paciente', to='Paciente', on_delete=models.CASCADE)

    def __str__(self):
        return self.paciente.nombre

    class Meta:
        db_table = 'expediente'
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'
        ordering = ['paciente']


class Consulta(Common):
    comentarios_consulta = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Medico', to=Usuario, related_name='medico', related_query_name='medicos',
                                on_delete=models.CASCADE)
    cita = models.ForeignKey(verbose_name='Cita', to='Cita', related_name='consulta', related_query_name='consultas', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentarios_consulta

    class Meta:
        db_table = 'consulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'


class Imagen(Common):
    comentarios_imagen = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Análista', to=Usuario, related_name='analista',
                                related_query_name='quimicos', on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen', upload_to='examenes/', max_length=255, blank=False, null=False)
    cita = models.ForeignKey(verbose_name='Cita', to='Cita', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentarios_imagen

    class Meta:
        db_table = 'imagen'
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'


class Laboratorio(Common):
    comentarios_laboratorio = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Quimico', to=Usuario, related_name='quimico',
                                related_query_name='quimicos', on_delete=models.CASCADE)
    resultado_PDF = models.FileField('Resultado', upload_to='resultados/', max_length=255, blank=False, null=False)
    cita = models.ForeignKey(verbose_name='Cita', to='Cita', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentarios_laboratorio

    class Meta:
        db_table = 'laboratorio'
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        ordering = ['id']


class Cita(Common):
    comentario = models.CharField('Comentario', max_length=255)
    fecha = models.DateTimeField('Fecha', auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(verbose_name='Medico', to=Usuario, related_name='medico_consulta',
                                related_query_name='medicos_consulta', on_delete=models.CASCADE)
    expediente = models.ForeignKey(verbose_name='Expediente', to='Expediente', on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # servicio = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.comentario

    class Meta:
        db_table = 'cita'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha']
