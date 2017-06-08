from __future__ import unicode_literals
import os
from django.db import models
from django import forms
import datetime
from django.forms import ModelForm
#import registro.views.sendMail
from  django.utils.encoding import smart_text
from django.contrib.admin.widgets import AdminDateWidget
# Create your models here.

def fin_default(): 
	return datetime.datetime.now() + datetime.timedelta(days = 7)


class Userio(models.Model):
	aidi = models.CharField(max_length=20, null=False, primary_key=True, blank=False)
	passw = models.CharField(max_length=30, null=False, blank=False)
	admini = 'ad'
	regul = 're'
	ELEC_TIPOS = (
		(admini, 'Administrador'),
		(regul, 'Regular'),
	)
	tipo = models.CharField(max_length=2, choices=ELEC_TIPOS, default=regul)
	correo = models.EmailField()


class UserForm(ModelForm):
	passw = forms.CharField(widget=forms.PasswordInput, required=True)
	passw1 = forms.CharField(widget=forms.PasswordInput, required=True)

	class Meta:
		model = Userio
		fields = ['aidi', 'correo', 'passw', 'passw1', 'tipo']

	def clean(self):
		password1 = self.cleaned_data.get('passw')
		password2 = self.cleaned_data.get('passw1')

		if password1 and password1 != password2:
			raise forms.ValidationError("Las contraseñas no coinciden.")

		return self.cleaned_data


class UserAut(ModelForm):
	passw = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = Userio
		fields = '__all__'
		exclude = ['tipo', 'correo']


class UserChangePass(ModelForm):
	passw = forms.CharField(widget=forms.PasswordInput, required=True)
	passw1 = forms.CharField(widget=forms.PasswordInput, required=True)

	class Meta:
		model = Userio
		fields = ['passw', 'passw1']

	def clean(self):
		password1 = self.cleaned_data.get('passw')
		password2 = self.cleaned_data.get('passw1')

		if password1 and password1 != password2:
			raise forms.ValidationError("Las contraseñas no coinciden.")

		return self.cleaned_data


class Anunc(models.Model):
	fecha_crea = models.DateField()
	fecha_inicio = models.DateField()
	fecha_aut = models.DateField()
	fecha_fin = models.DateField()
	pendiente = 'pe'
	aprobado = 'ap'
	negado = 'ne'
	expirado = 'ex'
	ELEC_ESTADO = (
		(pendiente, 'Pendiente'),
		(aprobado, 'Aprobado'),
		(negado, 'Negado'),
		(expirado, 'Expirado'),
	)
	estado = models.CharField(max_length=2, choices=ELEC_ESTADO, default=pendiente)
	imagen = models.ImageField(upload_to="imgs/", blank=True)
	mensaje = models.TextField(max_length=1000, blank=True)
	muy_baja = 'nn'
	baja = 'ni'
	media = 'me'
	alta = 'al'
	muy_alta = 'aa'
	ELEC_PRIORI = (
		(muy_baja, 'Muy Baja'),
		(baja, 'Baja'),
		(media, 'Media'),
		(alta, 'Alta'),
		(muy_alta, 'Muy Alta'),
	)
	prioridad = models.CharField(max_length=2, choices=ELEC_PRIORI, default=media)
	autorizador = models.ForeignKey(Userio, related_name='user_aut', null=True)
	creador = models.ForeignKey(Userio, related_name='user_crea')
	urli = models.URLField(null=True, blank=True)


class AnuForm(ModelForm):
	fecha_inicio = forms.DateField(widget = forms.SelectDateWidget)
	fecha_fin = forms.DateField(widget = forms.SelectDateWidget)

	class Meta:
		model = Anunc
		fields = '__all__'
		exclude = ['fecha_crea', 'fecha_aut', 'autorizador', 'prioridad', 'estado', 'creador']


class AnuFormAd(ModelForm):
	fecha_inicio = forms.DateField(widget = forms.SelectDateWidget)
	fecha_fin = forms.DateField(widget = forms.SelectDateWidget)

	class Meta:
		model = Anunc
		fields = '__all__'
		exclude = ['fecha_crea', 'fecha_aut', 'autorizador', 'estado', 'creador']


class EditAd(ModelForm):
	fecha_inicio = forms.DateField(widget = forms.SelectDateWidget)
	fecha_fin = forms.DateField(widget = forms.SelectDateWidget)

	class Meta:
		model = Anunc
		fields = '__all__'
		exclude = ['fecha_crea', 'fecha_aut', 'autorizador', 'estado', 'creador']
