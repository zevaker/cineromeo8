from django.shortcuts import render
from .models import Categoria,Pelicula #importar el modelo
# para lograr el ingreso de usuarios regsitrados al sistema, se debe
# incorporar el modelo de usuarios registrados de Django
from django.contrib.auth.models import User
# importar el sistema de autentificacion
from django.contrib.auth import authenticate,logout,login as auth_login
# importar los "decorators" que permiten evitar el ingreso a una pagina
# sin estar logeado
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here. crear los controladores
# para las paginas web

def vacio_carrito(request):
    request.session["carro"]=""
    lista=request.session.get("carro","")
    return render(request,"core/carrito.html",{'lista':lista})

@login_required(login_url='/login/')
def home(request):
    return render(request,'core/home.html')
    # retorna la pagina renderizada

def cerrar_sesion(request):
    logout(request)
    return HttpResponse("<script>alert('cerro sesion');window.location.href='/';</script>")

@login_required(login_url='/login/')
def agregar_carro(request, id):
    #recuperar el valor de la pelicula
    # clausula select "select * from Pelicula where name like (%id%)"
    pelicula=Pelicula.objects.filter(name__contains=id)
    valor=pelicula.precio
    #recuperar una sesion llamada 'carro', de no existir no deja nada ''
    sesion=request.session.get("carro","")
    # buscar la pelicula en el interior del listado
    arr=sesion.split(";")
    #almacea los registros limpios
    arr2=''
    sw=0
    cant=1
    for p in arr:
        pel=p.split(":")        
        if pel[0]==id:
            cant=int(pel[1])+1
            sw=1
            arr2=arr2+str(pel[0])+":"+str(cant)+":"+str(valor)+";"            
        elif not pel[0]=="":
            cant=pel[1]
            arr2=arr2+str(pel[0])+":"+str(cant)+":"+str(valor)+";"
        
    #pregunta si la pelicula existe o no
    if sw==0:
        arr2=arr2+str(id)+":"+str(1)+":"+str(valor)+";"

    #en la session 'carro' almaceno lo que trae la sesion mas el titulo de la pelicula
    request.session["carro"]=arr2
    #recuperar el listado de peliculas
    pelis=Pelicula.objects.all()
    #renderizar la pagina, pasandole el listado de peliculas
    msg='agrego pelicula'
    return render(request,'core/galeria.html',{'listapelis':pelis,'msg':msg})

@login_required(login_url='/login/')
def carrito(request):
    lista=request.session.get("carro","")
    arr=lista.split(";")
    return render(request,"core/carrito.html",{'lista':arr})

def login(request):
    return render(request,'core/login.html')

def login_iniciar(request):
    if request.POST:
        u=request.POST.get("txtUsuario")
        p=request.POST.get("txtPass")
        usu=authenticate(request,username=u,password=p)
        if usu is not None and usu.is_active:
            auth_login(request, usu)
            return render(request,'core/home.html')
    return render(request,'core/login.html')
    
@login_required(login_url='/login/')
def eliminar_pelicula(request,id):
    mensaje=''    
    peli=Pelicula.objects.get(name=id)
    try:
        peli.delete()
        mensaje='elimino pelicula'
    except:
        mensaje='no pudo elimiar pelicula'
    
    pelis=Pelicula.objects.all()
    return render(request,'core/galeria.html',{'listapelis':pelis,'msg':mensaje})

@login_required(login_url='/login/')
def galeria(request):
    pelis=Pelicula.objects.all()# select * from pelicula
    return render(request, 'core/galeria.html',{'listapelis':pelis})

@login_required(login_url='/login/')
def quienes_somos(request):
    return render(request,'core/quienes_somos.html')

@login_required(login_url='/login/')
def formulario2(request):
    cate=Categoria.objects.all()# select * from Categoria
    if request.POST:
        titulo=request.POST.get("txtTitulo")
        precio=request.POST.get("txtPrecio")
        duracion=request.POST.get("txtDuracion")
        descripcion=request.POST.get("txtDescripcion")
        categoria=request.POST.get("cboCategoria")
        #recupera el objeto con 'name' enviado desde el comboBox (cboCategoria)
        obj_categoria=Categoria.objects.get(name=categoria)
        #recuperar la imagen desde el formulario
        imagen=request.FILES.get("txtImagen")
        #crear una instancia de Pelicula (modelo)
        pelicula=Pelicula(
            name=titulo,
            duracion=duracion,
            precio=precio,
            descripcion=descripcion,
            categoria=obj_categoria,
            imagen=imagen
        )
        pelicula.save() #graba el objeto e bdd
        return render(request,'core/formulario2.html',{'lista':cate,'msg':'grabo','sw':True})
    return render(request,'core/formulario2.html',{'lista':cate})#pasan los datos a la web

@login_required(login_url='/login/')
def formulario(request):
    mensaje=''
    sw=False
    if request.POST:
        accion=request.POST.get("Accion")
        if accion=="Grabar":
            name=request.POST.get("txtCate")
            cali=request.POST.get("txtCalificacion")
            CATE=Categoria(
                name=name,
                calificacion=cali
            )
            CATE.save()
            mensaje='Grabo'    
            sw=True
        if accion=="Eliminar":
            name=request.POST.get("txtCate")
            cate=Categoria.objects.get(name=name)
            cate.delete()
            mensaje='Elimino'
            sw=True

    categorias=Categoria.objects.all()# select * from categoria
    return render(request,'core/formulario.html',{'lista':categorias,'msg':mensaje,'sw':True})