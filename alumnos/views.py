from django.shortcuts import render
from .models import Alumno, Genero 

# Create your views here.

def index(request):
    alumnos = Alumno.objects.all()
    context = {"alumnos": alumnos}
    return render(request, "alumnos/index.html", context)

def listadoSQL(request):
    alumnos = Alumno.objects.raw("SELECT * FROM alumnos_alumno")
    context = {"alumnos": alumnos}
    return render(request, "alumnos/listadoSQL.html", context)

def crud(request):
    alumnos = Alumno.objects.all()
    context = {"alumnos": alumnos}
    return render(request, "alumnos/alumnos_list.html", context)

def alumnosAdd(request):
    if request.method != "POST":
        #no es un POST, por lo tanto se muestra el formulario para agregar
        generos = Genero.objects.all()
        context = {"generos": generos}
        return render(request, "alumnos/alumnos_add.html", context)
    
    else:
        #Es un POST, por lo tanto se recuperan los datos del formulario
        #y se graban en la tabla.
        
        rut =       request.POST["rut"]
        nombre =    request.POST["nombre"]
        apPaterno = request.POST["paterno"]
        apMaterno = request.POST["materno"]
        fechaNac =  request.POST["fechaNac"]
        genero =    request.POST["genero"]
        telefono =  request.POST["telefono"]
        email =     request.POST["email"]
        direccion = request.POST["direccion"]
        activo = "1"
        
        print(rut + " " + nombre + " " + apPaterno + " " + apMaterno + " " + fechaNac)

        objGenero = Genero.objects.get(id_genero = genero)
        obj = Alumno.objects.create( rut = rut,
                                     nombre = nombre,
                                     apellido_paterno = apPaterno,
                                     apellido_materno = apMaterno,
                                     fecha_nacimiento = fechaNac,
                                     id_genero = objGenero,
                                     telefono = telefono,
                                     email = email,
                                     direccion = direccion,
                                     activo = 1)
        
        obj.save()
        context = {"mensaje":"Ok, datos grabados..."}
        return render(request, "alumnos/alumnos_add.html", context)

def alumnos_del(request, pk):
    context={}
    try:
        alumno = Alumno.objects.get(rut = pk)
        
        alumno.delete()
        mensaje = "Bien, datos eliminados..."
        alumnos = Alumno.objects.all()
        context = {"alumnos": alumnos, "mensaje": mensaje}
        return render(request, "alumnos/alumnos_list.html", context)
    
    except:
        mensaje = "Error, rut no existe..."
        alumnos = Alumno.objects.all()
        context = {"alumnos": alumnos, "mensaje": mensaje}
        return render(request, "alumnos/alumnos_list.html", context)
    
def alumnos_findEdit(request, pk):

    if pk != "":
        alumno = Alumno.objects.get(rut = pk)
        generos = Genero.objects.all()

        context = {"alumno": alumno, "generos": generos}
        if alumno:
            return render(request, "alumnos/alumnos_edit.html", context)
        else:
            context = {"mensaje":"Error, rut no existe..."}
            return render(request, "alumnos/alumnos_list.html", context)

def alumnosUpdate(request):

    if request.method == "POST":
        #Es un POST, por lo tanto se recuperan los datos del formulario
        #y se graban en la tabla
    
        rut =       request.POST["rut"]
        nombre =    request.POST["nombre"]
        apPaterno = request.POST["paterno"]
        apMaterno = request.POST["materno"]
        fechaNac =  request.POST["fechaNac"]
        genero =    request.POST["genero"]
        telefono =  request.POST["telefono"]
        email =     request.POST["email"]
        direccion = request.POST["direccion"]
        activo = "1"
        
        objGenero = Genero.objects.get(id_genero = genero)

        alumno = Alumno()
        alumno.rut = rut
        alumno.nombre = nombre
        alumno.apellido_paterno = apPaterno
        alumno.apellido_materno = apMaterno
        alumno.fecha_nacimiento = fechaNac
        alumno.id_genero = objGenero
        alumno.telefono = telefono
        alumno.email = email
        alumno.direccion = direccion
        alumno.activo = 1
        alumno.save()
        
        generos = Genero.objects.all()
        context = {"mensaje": "Ok, los datos actualizados...", "generos": generos, "alumno": alumno }
        return render(request, "alumnos/alumnos_edit.html", context)
    else:
        #no es un POST, por lo tanto se muestra el formulario para agregar.
        alumnos = Alumno.objects.all()
        context = {"alumnos": alumnos}
        return render(request, "alumnos/alumnos_list.html", context)