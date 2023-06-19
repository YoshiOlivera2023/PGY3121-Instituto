from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Alumno, Genero 

from .forms import GeneroForm

# Create your views here.

############################ CRUD USANDO FORMS #############################

def crud_generos(request):

    generos = Genero.objects.all()
    context = {"generos": generos}
    print("enviando datos generos_list")
    return render(request, "alumnos/generos_list.html", context)

def generosAdd(request):
    print("estoy en controlador generosAdd...")
    context={}

    if request.method == "POST":
        print("controlador es un post...")
        form = GeneroForm(request.POST)
        if form.is_valid():
            print("estoy en agregar, is_valid")
            form.save()

            #limpiar form 
            form = GeneroForm()

            context = {"mensaje" : "Ok, datos grabados...", "form": form}
            return render(request, "alumnos/generos_add.html", context)    
    else:
        form = GeneroForm()
        context = {"form": form}
        return render(request, "alumnos/generos_add.html", context)  
    
def generos_del(request, pk):
    mensajes = []
    errores = []
    generos = Genero.objects.all()
    try:
        genero = Genero.objects.get(id_genero = pk)
        context = {}
        if genero:
            genero.delete()
            mensajes.append("Bien, datos eliminados...")
            context = {"generos": generos, "mensajes": mensajes, "errores": errores}
            return render(request, "alumnos/generos_list.html", context)  
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje = "Error, id no existe"
        context = {"mensaje": mensaje, "generos": generos}
        return render(request, "alumnos/generos_list.html", context)  

def generos_edit(request, pk):
    try:
        genero = Genero.objects.get(id_genero=pk)
        context = {}
        if genero:
            print("Edit encontró el género...")
            if request.method == "POST":
                print("edit, es un POST")
                form = GeneroForm(request.POST, instance=genero)
                form.save()
                mensaje = "Bien, datos actualizados..."
                print(mensaje)
                context = {"genero": genero, "form": form, "mensaje": mensaje}
                return render(request, "alumnos/generos_edit.html", context)
            else:
                # no es un POST
                print("edit, NO ES UN POST")
                form = GeneroForm(instance=genero)
                mensaje = ""
                context = {"genero": genero, "form": form, "mensaje": mensaje, "generos": genero}
                return render(request, "alumnos/generos_edit.html", context)
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje = "Error, id no existe"
        context = {"mensaje": mensaje, "generos": generos}
        return render(request, "alumnos/generos_list.html", context)

############################################################################

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
        #generos = Genero.objects.all()
        #context = {"generos": generos}
        context = {'form': GeneroForm}
        #context['form'] = GeneroForm
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