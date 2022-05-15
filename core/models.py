from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.managers import CustomUserManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    """ Modelo para el usuario

        Argumentos:
            cedula_profesional: cedula del profesional
            huella: huella digital del profesional
            nombre: nombre del profesional
            correo: correo del profesional
            telefono: telefono del profesional
            is_active: Si es un usuario activo
            is_staff: Si es un usuario de staff
            is_superuser: Si es un usuario superusuario
    
    """
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
    """ Modelo base para todos los modelos
    
        Este modelo hereda de models.Model, que es el modelo base de Django.
        
        Argumentos:
            created_by: Una llave foranea que apunta a la tabla ``Usuario``.
            updated_by: Una llave foranea que apunta a la tabla ``Usuario``.
            created_at: Fecha de creacion del registro.
            updated_at: Fecha de actualizacion del registro.

    """
    created_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class Paciente(Common):
    """ Modelo de paciente
    
        Argumentos:
            nombre (str): nombre del paciente
            fecha_nacimiento (date): fecha de nacimiento del paciente
            curp (str): curp del paciente
            huella (str): huella digital del paciente
            correo (str): correo del paciente
            telefono (str): telefono del paciente
            tipo_sangre (TipoSangre): tipo de sangre del paciente
            sexo (Sexo): sexo del paciente
            es_menor (bool): si es menor de edad
            tutor (Paciente): Referencia a sí mismo en caso de tuto, llave foranea a la tabla ``Paciente``
    """
    class TipoSangre(models.TextChoices):
        """ Enumerador de tipo de sange

            Constantes:
                AP: A+
                AN: A-
                BP: B+
                BN: B-
                ABP: AB+
                OP: O+
                ON: O-
        """
        AP = 'AP', 'A+'
        AN = 'AN', 'A-'
        BP = 'BP', 'B+'
        BN = 'BN', 'B-'
        ABP = 'ABP', 'AB+'
        OP = 'OP', 'O+'
        ON = 'ON', 'O-'
    
    class Sexo(models.TextChoices):
        """ Enumerador de sexo
        
            Constantes:
                MASCULINO: Masculino
                FEMENINO: Femenino
                OTRO: Otro
        
        """
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMENINO = 'FEMENINO', 'Femenino'
        OTRO = 'OTRO', 'Otro'
    
    nombre = models.CharField('Nombre', max_length=50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', auto_now=False, auto_now_add=False)
    curp = models.CharField('CURP', max_length=18, unique=True)
    huella = models.ImageField('Huella',upload_to='huellas/', max_length=10485760)
    correo = models.EmailField('Correo', max_length=254, unique=True)
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
    

@receiver(post_save, sender=Paciente)
def create_expediente(sender, instance, created, **kwargs):
    if created:
        Expediente.objects.create(paciente=instance)


class Expediente(Common):
    """ Modelo de expediente
    
        Argumentos:
            paciente (Paciente): una llave foranea que apunta a la tabla ``Paciente``.

    """
    paciente = models.OneToOneField(verbose_name='Paciente', to='Paciente', on_delete=models.CASCADE)

    def __str__(self):
        return self.paciente.nombre

    class Meta:
        db_table = 'expediente'
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'
        ordering = ['paciente']


class Consulta(Common):
    """ Modelo de consulta

        Argumentos:
            comentarios_consulta (str): comentarios de la consulta
            usuario (Usuario): una llave foranea que apunta a la tabla ``Usuario``.
            cita (Cita): una llave foranea que apunta a la tabla ``Cita``.
    """
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
    """ Modelo de imagenes, para resultados de análisis que involucran imagenes

        Argumentos:
            comentarios_imagen (str): comentarios de la imagen
            usuario (Usuario): una llave foranea que apunta a la tabla ``Usuario``.
            imagen (str): imagen de resultado de análisis
            cita (Cita): una llave foranea que apunta a la tabla ``Cita``.
    """
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
    """ Modelo de resultados de laboratorio
    
        Argumentos:
            comentarios_laboratorio (str): comentarios de los resultados
            usuario (Usuario): una llave foranea que apunta a la tabla ``Usuario``.
            resultado_PDF (str): resultados de laboratorio en formato PDF
            cita (Cita): una llave foranea que apunta a la tabla ``Cita``.
    """
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
    """ Modelo de citas
    
        Argumentos:
            comentario (str): comentarios de la cita
            fecha (date): fecha de la cita
            usuario (Usuario): una llave foranea que apunta a la tabla ``Usuario``.
            expediente (Expediente): una llave foranea que apunta a la tabla ``Expediente``.

    """
    comentario = models.CharField('Comentario', max_length=255)
    fecha = models.DateTimeField('Fecha', auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(verbose_name='Medico', to=Usuario, related_name='medico_consulta',
                                related_query_name='medicos_consulta', on_delete=models.CASCADE)
    expediente = models.ForeignKey(verbose_name='Expediente', to='Expediente', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    class Meta:
        db_table = 'cita'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha']
