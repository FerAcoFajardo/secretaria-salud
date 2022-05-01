from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Usuario(AbstractUser):
    cedula_profesional = models.CharField('Cedula profesional', max_length=50)
    huella = models.CharField('Huella', max_length=99999)
    nombre = models.CharField('Nombre', max_length=50)
    correo = models.EmailField('Correo', max_length=50)
    telefono = models.CharField('Telefono', max_length=50)


class Common(models.Model):
    created_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(Usuario, related_name='+', on_delete=models.CASCADE)
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
        HELICOPTERO_APACHE_DE_COMBATE = 'HELICOPTERO_APACHE_DE_COMBATE', 'Helicoptero Apache de combate'
    
    nombre = models.CharField('Nombre', max_length=50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', auto_now=False, auto_now_add=False)
    curp = models.CharField('CURP', max_length=50)
    huella = models.CharField('Huella dactila', max_length=999999)
    correo = models.EmailField('Correo', max_length=254)
    telefono = models.CharField('Telefono', max_length=50)
    tipo_sangre = models.CharField('Tipo de sangre', choices=TipoSangre.choices, max_length=3)
    sexo = models.CharField('Sexo', choices=Sexo.choices, null=True, blank=True, max_length=30)
    es_menor = models.BooleanField('Es menor', default=False)
    tutor = models.ForeignKey(verbose_name='Tutor', to='self', null=True, blank=True, on_delete=models.SET_NULL)
    

class Expediente(Common):
    paciente = models.OneToOneField(verbose_name='Paciente', to='Paciente', on_delete=models.CASCADE)


class Consulta(Common):
    comentarios_consulta = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Medico', to=Usuario, related_name='medico', related_query_name='medicos',
                                on_delete=models.CASCADE)


class Imagen(Common):
    comentarios_imagen = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Análista', to=Usuario, related_name='analista',
                                related_query_name='quimicos', on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen', upload_to='examenes/', max_length=255, blank=False, null=False)


class Laboratorio(Common):
    comentarios_laboratorio = models.CharField('Comentarios', max_length=255)
    usuario = models.ForeignKey(verbose_name='Quimico', to=Usuario, related_name='quimico',
                                related_query_name='quimicos', on_delete=models.CASCADE)
    resultadoPDF = models.FileField('Resultado', upload_to='resultados/', max_length=255, blank=False, null=False)


class Cita(Common):
    comentario = models.CharField('Comentario', max_length=255)
    fecha = models.DateTimeField('Fecha', auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(verbose_name='Medico', to=Usuario, related_name='medico_consulta',
                                related_query_name='medicos_consulta', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    servicio = GenericForeignKey('content_type', 'object_id')
