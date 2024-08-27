from django.db import models

class Licencas(models.Model):
    lice_id = models.AutoField(primary_key=True)
    lice_docu = models.CharField(max_length=60, blank=True, null=True)
    lice_nome = models.CharField(max_length=60, blank=True, null=True)
    lice_emai = models.CharField(max_length=150, blank=True, null=True)
    lice_nume_maqu = models.IntegerField(blank=True, null=True)
    lice_bloq = models.BooleanField(blank=True, null=True)
    lice_nume_empr = models.IntegerField(blank=True, null=True)
    lice_nume_fili = models.IntegerField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True) 
    usuarios = models.ManyToManyField('Usuarios', related_name='licencas', blank=True)

    class Meta:
        managed = False
        db_table = 'licencas'
    
    def __str__(self):
       return f"Licencas {self.lice_id} - {self.lice_docu}"
    

class Uctabusers(models.Model):
    uciduser = models.IntegerField(blank=True, null=True)
    ucusername = models.CharField(max_length=30, blank=True, null=True)
    uclogin = models.CharField(max_length=30, blank=True, null=True)
    ucpassword = models.CharField(max_length=250, blank=True, null=True)
    ucpassexpired = models.CharField(max_length=10, blank=True, null=True)
    ucuserexpired = models.IntegerField(blank=True, null=True)
    ucuserdayssun = models.IntegerField(blank=True, null=True)
    ucemail = models.CharField(max_length=150, blank=True, null=True)
    ucprivileged = models.IntegerField(blank=True, null=True)
    uctyperec = models.CharField(max_length=1, blank=True, null=True)
    ucprofile = models.IntegerField(blank=True, null=True)
    uckey = models.CharField(max_length=250, blank=True, null=True)
    ucinative = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uctabusers'


class Usuarios(models.Model):
    usua_codi = models.IntegerField(primary_key=True)
    usua_nome = models.CharField(max_length=30, blank=True, null=True)
    usua_data_nasc = models.DateField(blank=True, null=True)
    usua_sexo = models.CharField(max_length=1, blank=True, null=True)
    usua_emai = models.CharField(max_length=100, blank=True, null=True)
    usua_fone = models.CharField(max_length=14, blank=True, null=True)
    usua_senh = models.CharField(max_length=10, blank=True, null=True)
    usua_libe_clie_bloq = models.BooleanField(blank=True, null=True)
    usua_libe_pedi_comp = models.BooleanField(blank=True, null=True)
    usua_port = models.BooleanField(blank=True, null=True)
    usua_pisc = models.BooleanField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'usuarios'
