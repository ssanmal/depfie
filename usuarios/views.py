# -*- coding: utf-8 -*-
from django.shortcuts import render
import datetime
from django.http import HttpResponse
from .models import *
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.db.models import Q
from django.core.mail import send_mail
# from smtplib import SMTP
# Create your views here.

### Fecha predefinida para el fin de la publicación de anuncios
def fin_default(): 
    return datetime.datetime.now() + datetime.timedelta(days = 7)


### Fecha predefinida para la eliminación automática de anuncios
def fecha_del(): 
    return datetime.datetime.now() - datetime.timedelta(days = 30)


### Formulario para creación de usuarios
def formulario(request):
    farm = UserForm()
    farm.fields['aidi'].label = "Identificador único de usuario"
    farm.fields['correo'].label =  "Correo electrónico"
    farm.fields['passw'].label = "Contraseña"
    farm.fields['passw1'].label = "Confirmación de contraseña"
    farm.fields['tipo'].label = "Tipo de usuario"
    return render(request, 'registro/form.html',
                  {"titulo": "Registro de Usuarios",
                   "farm": farm})


### Formulario para realizar inicio de sesión
def logon(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 'ad':
            return render(request, 'admin/main.html')
        if request.session['tipo'] == 're':
            return render(request, 'regular/main.html')
    farm = UserAut()
    farm.fields['aidi'].label = "ID"
    farm.fields['passw'].label = "Contraseña"
    return render(request, 'login/login.html',
                  {"titulo": "Inicio de Sesión",
                   "farm": farm})


### Formulario para usuarios regulares para cambiar contraseña
def cambiopass(request):
    form = UserChangePass()
    form.fields['passw'].label = "Nueva contraseña"
    form.fields['passw1'].label = "Confirmación de contraseña"
    return render(request, 'regular/changepass.html',
                  {"titulo": "Cambio de Contraseña",
                   "form": form})


### Formulario para usuarios administradores para cambiar contraseña
def cambiopassad(request):
    form = UserChangePass()
    form.fields['passw'].label = "Nueva contraseña"
    form.fields['passw1'].label = "Confirmación de contraseña"
    return render(request, 'admin/changepass.html',
                  {"titulo": "Cambio de Contraseña",
                   "form": form})


### Función para finalizar sesión
def logot(request):
    request.session.flush()
    return redirect('logon')


### Función para mostrar los usuarios actuales registrados en la base de datos
def userque(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 're':
            return redirect(logon)
    else:
        return redirect(logon)
    que_usuarios = Userio.objects.all()
    return render(request, 'vista/usuarios.html', {"titulo": "Usuarios Registrados",
                  "que_usuarios": que_usuarios})


### Función para borrar un usuario
def borraus(request):
    if request.method == "POST":
        delid = request.POST['id']
        if delid == request.session['id']:
            return HttpResponse("No se puede eliminar a sí mismo")
        delus = Userio.objects.get(aidi=delid)
        delus.delete()
        return redirect(userque)


### Función para borrar anuncios
def borraan(request):
    if request.method == "POST":
        delid = request.POST['id']
        delan = Anunc.objects.get(id=delid)
        delan.delete()
        return redirect(anuque)


### Función para aprobar un anuncio
def aproban(request):
    if request.method == "POST":
        upid = request.POST['id']
        upan = Anunc.objects.get(id=upid)
        upan.fecha_aut = datetime.datetime.today().strftime("%Y-%m-%d")
        upan.autorizador = Userio.objects.get(aidi=request.session['id'])
        upan.estado = 'ap'
        usid = upan.creador.aidi
        upan.save()
        autor = Userio.objects.get(aidi=usid)
        send_mail(
            'Aprobación de Anuncio',
            'El anuncio que propuso ha sido aprobado para aparecer en el carrusel.',
            'from@example.com',
            [autor.correo],
            fail_silently=False,
        )
        return redirect(anuque)


### Formulario para realizar un cambio a un anuncio
def edian(request):
    if request.method == "POST":
        edid = request.POST['id']
        edan = Anunc.objects.get(id=edid)
        data = {'fecha_inicio': edan.fecha_inicio,
                'fecha_fin': edan.fecha_fin,
                'prioridad': edan.prioridad,
                'mensaje': edan.mensaje,
                'imagen': edan.imagen,
                'urli': edan.urli}
        ediadform = EditAd(data)
        aidd = edan.id
        ediadform.fields['fecha_inicio'].label = "Fecha de inicio"
        ediadform.fields['fecha_fin'].label = "Fecha de fin"
        ediadform.fields['prioridad'].label = "Prioridad"
        if edan.imagen:
            ediadform.fields['imagen'].label = "Imagen (" + edan.imagen.name + ")"
        else:
            ediadform.fields['imagen'].label = "Imagen"
        ediadform.fields['mensaje'].label = "Mensaje"
        ediadform.fields['urli'].label = "URL"
        return render(request, 'admin/editan.html', {
            "titulo": "Modificación de Anuncio",
            "ediadform": ediadform,
            "aidd": aidd})


### Función para rechazar un anuncio
def rechan(request):
    if request.method == "POST":
        upid = request.POST['id']
        upan = Anunc.objects.get(id=upid)
        upan.estado = 'ne'
        usid = upan.creador.aidi
        upan.save()
        autor = Userio.objects.get(aidi=usid)
        send_mail(
            'Rechazo de Anuncio',
            'El anuncio que propuso ha sido rechazado para aparecer en el carrusel.',
            'from@example.com',
            [autor.correo],
            fail_silently=False,
        )
        return redirect(anuque)


### Función para mostrar los anuncios actuales registrados en la base de datos
def anuque(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 're':
            return redirect(logon)
    else:
        return redirect(logon)
    que_anuncios = Anunc.objects.all().order_by('fecha_crea')
    for anuncio in que_anuncios:
        if anuncio.fecha_fin.strftime("%Y-%m-%d") < fecha_del().strftime("%Y-%m-%d"):
            anuncio.delete()
    return render(request, 'vista/anuncios.html', {"titulo": "Anuncios Registrados",
                  "que_anuncios": que_anuncios})


### Función para obtener los anuncios que serán mostrados en el carrusel/banner
def bannque(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 're':
            return redirect(logon)
    else:
        return redirect(logon)
    criterio1 = Q(estado="ap")
    criterio2 = Q(fecha_inicio__lte=datetime.datetime.today().strftime("%Y-%m-%d"))
    criterio3 = Q(fecha_fin__gte=datetime.datetime.today().strftime("%Y-%m-%d"))
    que_anuncios = Anunc.objects.filter(criterio1 & criterio2 & criterio3).order_by('prioridad')
    return render(request, 'vista/banner.html', {"titulo": "Banner",
                  "que_anuncios": que_anuncios})


### Función para obtener los anuncios que serán mostrados en un carrusel/banner que simula la página del departamento de posgrado
def depque(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 're':
            return redirect(logon)
    else:
        return redirect(logon)
    criterio1 = Q(estado="ap")
    criterio2 = Q(fecha_inicio__lte=datetime.datetime.today().strftime("%Y-%m-%d"))
    criterio3 = Q(fecha_fin__gte=datetime.datetime.today().strftime("%Y-%m-%d"))
    que_anuncios = Anunc.objects.filter(criterio1 & criterio2 & criterio3).order_by('prioridad')
    return render(request, 'vista/depbanner.html', {"que_anuncios": que_anuncios})


### Formulario para usuarios regulares para crear anuncios
def creanunreg(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 'ad':
            return redirect(logon)
    else:
        return redirect(logon)
    data = {'fecha_inicio': datetime.datetime.today().strftime("%Y-%m-%d"),
            'fecha_fin': fin_default().strftime("%Y-%m-%d"),
            'prioridad': 'me'}
    fanun = AnuForm(data)
    fanun.fields['fecha_inicio'].label = "Fecha de inicio"
    fanun.fields['fecha_fin'].label = "Fecha de fin"
    fanun.fields['imagen'].label = "Imagen"
    fanun.fields['mensaje'].label = "Mensaje"
    fanun.fields['urli'].label = 'URL'
    return render(request, 'regular/forman.html',
                  {"titulo": "Registro de Anuncios",
                   "fanun": fanun})


### Formulario para usuarios administradores para crear anuncios
def creanunad(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 're':
            return redirect(logon)
    else:
        return redirect(logon)
    data = {'fecha_inicio': datetime.datetime.today().strftime("%Y-%m-%d"),
            'fecha_fin': fin_default().strftime("%Y-%m-%d"),
            'prioridad': 'me'}
    fanun = AnuFormAd(data)
    fanun.fields['fecha_inicio'].label = "Fecha de inicio"
    fanun.fields['fecha_fin'].label = "Fecha de fin"
    fanun.fields['prioridad'].label = "Prioridad"
    fanun.fields['imagen'].label = "Imagen"
    fanun.fields['mensaje'].label = "Mensaje"
    fanun.fields['urli'].label = 'URL'
    return render(request, 'admin/formanad.html',
                  {"titulo": "Registro de Anuncios",
                   "fanun": fanun})


### Función para realizar cambios a un anuncio
def postchan(request):
    if request.method == "POST":
        edid = request.POST['id']
        anu = EditAd(request.POST, request.FILES)
        edianu = anu.save(commit=False)
        edan = Anunc.objects.get(id=edid)
        edan.fecha_inicio = edianu.fecha_inicio
        edan.fecha_fin = edianu.fecha_fin
        edan.prioridad = edianu.prioridad
        edan.mensaje = edianu.mensaje
        if edianu.imagen:
            edan.imagen = edianu.imagen
        edan.urli = edianu.urli
        edan.save()
        return redirect(anuque)


### Función para descartar los cambios realizados a un anuncio
def postdescan(request):
    return redirect(anuque)


### Función para agregar un usuario a la base de datos
def postregistro(request):
    if request.method == 'POST':
        f = UserForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect(userque)
        else:
            return HttpResponse(str(f.errors))


### Función para cambiar la contraseña del usuario actual
def postcambiocon(request):
    if request.method == "POST" and UserChangePass(request.POST).is_valid():
        newpas = request.POST['passw']
        usse = Userio.objects.get(aidi=request.session['id'])
        usse.passw = newpas
        usse.save()
        if request.session['tipo'] == 're':
            return render(request, 'regular/main.html')
        if request.session['tipo'] == 'ad':
            return render(request, 'admin/main.html')
    else:
        return HttpResponse(str(UserChangePass(request.POST).errors))


### Función para usuarios regulares para crear un anuncio en la base de datos
def postanunreg(request):
    if request.method == "POST":
        anu = AnuForm(request.POST, request.FILES)
        new_anu = anu.save(commit=False)
        new_anu.fecha_crea = datetime.datetime.today().strftime("%Y-%m-%d")
        new_anu.fecha_aut = '1944-06-06'
        new_anu.estado = 'pe'
        new_anu.prioridad = 'me'
        new_anu.creador = Userio.objects.get(aidi=request.session['id'])
        new_anu.autorizador = None
        new_anu.save()
        correos = []
        criterio = Q(tipo="ad")
        que_adm = Userio.objects.filter(criterio)
        for admin in que_adm:
            correos = correos + [admin.correo]
        send_mail(
            'Propuesta de Anuncio',
            'Se ha propuesto un nuevo anuncio por: ' + request.session['id'] + '. Se podrá aprobar o rechazar en la página de gestión de anuncios.',
            'from@example.com',
            correos,
            fail_silently=False,
        )
        return redirect('logon')


### Función para usuarios regulares para crear un anuncio en la base de datos
def postanunad(request):
    if request.method == "POST":
        anu = AnuFormAd(request.POST, request.FILES)
        new_anu = anu.save(commit=False)
        new_anu.fecha_crea = datetime.datetime.today().strftime("%Y-%m-%d")
        new_anu.fecha_aut = datetime.datetime.today().strftime("%Y-%m-%d")
        new_anu.estado = 'ap'
        beto = Userio.objects.get(aidi=request.session['id'])
        new_anu.creador = beto
        new_anu.autorizador = beto
        new_anu.save()
        return redirect('logon')


### Función para realizar el inicio de sesión como un usuario registrado
def sesion(request):
    request.session['signed'] = request.session.get('signed', False)
    if request.session['signed']:
        if request.session['tipo'] == 'ad':
            return render(request, 'admin/main.html')
        if request.session['tipo'] == 're':
            return render(request, 'regular/main.html')
    if not request.session['signed'] and not request.POST.get('aidi', False):
        return redirect('logon')
    if request.method == 'POST':
        aidi = request.POST['aidi']
        passw = request.POST['passw']
        veri = False
        curr_users = Userio.objects.all()
        for uss in curr_users:
            if aidi == uss.aidi:
                if passw == uss.passw:
                    veri = True
                    tipp = uss.tipo
                    break
        if veri:
            request.session['id'] = uss.aidi
            request.session['tipo'] = tipp
            request.session['signed'] = True
            if tipp == 'ad':
                return render(request, 'admin/main.html')
            if tipp == 're':
                return render(request, 'regular/main.html')
        else:
            return HttpResponse("Credenciales de sesión incorrectas")
