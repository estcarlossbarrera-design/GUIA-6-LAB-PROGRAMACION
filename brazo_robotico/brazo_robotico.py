import sys
import os
import tkinter as tk
from math import sin, cos, radians
import numpy as np
from stl import mesh
from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
ESCALA=0.01
carpeta=os.path.dirname(os.path.abspath(__file__))
piezas=[
    ("Base","Pieza1.stl", (0, 0, 0),None,None, None,False),
    ("Torre","Pieza2.stl", (0, 40, 0),(0, 1, 0), 0,"giro",False),
    ("Brazo","Pieza3.stl", (0, 115, 0),(0, 0, 1), 1,"giro",False),
    ("Antebrazo","Pieza4.stl", (0, 180, 0),(0, 0, 1),  2,"giro", False),
    ("Muneca","Pieza5.stl", (0, 150, 0),(0, 1, 0), 3,"giro",False),
    ("Palma","Pieza6.stl", (0, 40, 0),(0, 0, 1), 4,"giro", False),
    ("Mano","Pieza7.stl", (0, 45, 0),(0, 1, 0), 5,"giro",False),
    ("Dedo derecho","Pieza8.stl", (0, 58, 0),(1, 0, 0),  6,"desliza", True),
    ("Dedo izquierdo","Pieza9.stl", (0, 58, 0),(-1, 0, 0), 6,"desliza", True),
]
colores=[(0.5, 0.5, 0.55), (0.2, 0.4, 0.8), (0.9, 0.5, 0.1),
           (0.2, 0.7, 0.3), (0.8, 0.2, 0.2), (0.6, 0.3, 0.7),
           (0.1, 0.7, 0.8), (0.9, 0.9, 0.2), (0.9, 0.9, 0.2)]
listas=[]
nombres_art=["Base (giro)", "Hombro", "Codo",
               "Giro antebrazo", "Muneca", "Giro mano",
               "Pinza (mm)"]
minimos=[-180,-90,-120,-180,-90,-180, 0]
maximos=[180, 90, 120, 180, 90, 180, 20]
home_art=[0, 0, 0, 0, 0, 0, 10]
nombres_esc=["Mover X", "Mover Y", "Mover Z",
               "Rotar X", "Rotar Y", "Rotar Z"]
min_esc=[-5,-5,-5,-180,-180,-180]
max_esc=[5, 5, 5, 180, 180, 180]
cam_az=45.0
cam_el=35.0
DIST_HOME=14.0
ancho, alto=800, 600
arrastrando=False
mouse_x=0
mouse_y=0
root=tk.Tk()
root.title("Panel de control - Brazo robotico")
root.geometry("+20+20")
vars_art=[]
for i in range(7):
    vars_art.append(tk.DoubleVar(value=home_art[i]))
vars_esc=[]
for i in range(6):
    vars_esc.append(tk.DoubleVar(value=0))
var_zoom=tk.DoubleVar(value=DIST_HOME)
txt_art=[]
for i in range(7):
    txt_art.append(tk.StringVar())
txt_esc=[]
for i in range(6):
    txt_esc.append(tk.StringVar())
def home_articulaciones():
    for i in range(7):
        vars_art[i].set(home_art[i])
def poner_vista(az, el):
    global cam_az, cam_el
    cam_az=az
    cam_el=el
def home_camara():
    global cam_az, cam_el
    for i in range(6):
        vars_esc[i].set(0)
    var_zoom.set(DIST_HOME)
    cam_az=45.0
    cam_el=35.0
def salir():
    try:
        root.destroy()
    except tk.TclError:
        pass
    os._exit(0)
root.protocol("WM_DELETE_WINDOW", salir)
marco_art=tk.LabelFrame(root, text="Articulaciones", padx=5, pady=5)
marco_art.grid(row=0, column=0, padx=8, pady=5, sticky="n")
for i in range(7):
    tk.Label(marco_art, text=nombres_art[i], width=16, anchor="w").grid(row=i, column=0)
    tk.Scale(marco_art, from_=minimos[i], to=maximos[i], orient=tk.HORIZONTAL,
             length=170, resolution=1, showvalue=0,
             variable=vars_art[i]).grid(row=i, column=1)
    tk.Label(marco_art, textvariable=txt_art[i], width=8,
             relief="sunken").grid(row=i, column=2, padx=3)
tk.Button(marco_art, text="HOME", bg="lightgreen", width=12,
          command=home_articulaciones).grid(row=7, column=0, columnspan=3, pady=6)
marco_esc=tk.LabelFrame(root, text="Escena completa (mover / rotar)", padx=5, pady=5)
marco_esc.grid(row=0, column=1, padx=8, pady=5, sticky="n")
for i in range(6):
    tk.Label(marco_esc, text=nombres_esc[i], width=10, anchor="w").grid(row=i, column=0)
    if i<3:
        paso=0.1
    else:
        paso=1
    tk.Scale(marco_esc, from_=min_esc[i], to=max_esc[i], orient=tk.HORIZONTAL,
             length=170, resolution=paso, showvalue=0,
             variable=vars_esc[i]).grid(row=i, column=1)
    tk.Label(marco_esc, textvariable=txt_esc[i], width=9,
             relief="sunken").grid(row=i, column=2, padx=3)
tk.Label(marco_esc, text="Zoom (distancia)", width=10, anchor="w").grid(row=6, column=0)
tk.Scale(marco_esc, from_=5, to=30, orient=tk.HORIZONTAL, length=170,
         resolution=0.5, showvalue=0, variable=var_zoom).grid(row=6, column=1)
tk.Button(marco_esc, text="HOME CAMARA", bg="lightblue", width=14,
          command=home_camara).grid(row=7, column=0, columnspan=3, pady=6)
marco_vistas=tk.LabelFrame(root, text="Vistas", padx=5, pady=5)
marco_vistas.grid(row=1, column=0, padx=8, pady=5, sticky="we")
tk.Button(marco_vistas, text="Superior", width=9,
          command=lambda: poner_vista(0, 89.9)).grid(row=0, column=0, padx=3)
tk.Button(marco_vistas, text="Isometrica", width=9,
          command=lambda: poner_vista(45, 35.3)).grid(row=0, column=1, padx=3)
tk.Button(marco_vistas, text="Lateral", width=9,
          command=lambda: poner_vista(90, 0)).grid(row=0, column=2, padx=3)
tk.Button(marco_vistas, text="Frontal", width=9,
          command=lambda: poner_vista(0, 0)).grid(row=0, column=3, padx=3)
marco_piezas=tk.LabelFrame(root, text="Piezas importadas (STL)", padx=5, pady=5)
marco_piezas.grid(row=1, column=1, padx=8, pady=5, sticky="we")
lista_piezas=tk.Listbox(marco_piezas, height=5, width=42)
lista_piezas.pack()
ayuda=("Teclado (en la ventana 3D): q/a J1, w/s J2, e/d J3, r/f J4, "
         "t/g J5, y/h J6, u/j pinza, b = HOME, ESC = salir.\n"
         "Mouse: arrastrar con el boton izquierdo gira la camara, "
         "la rueda hace zoom.")
tk.Label(root, text=ayuda, justify="left", wraplength=640).grid(row=2, column=0,
                                                              columnspan=2, pady=4)
def actualizar_textos():
    for i in range(6):
        txt_art[i].set("%.0f deg"%vars_art[i].get())
    txt_art[6].set("%.0f mm"%vars_art[6].get())
    for i in range(3):
        txt_esc[i].set("%.1f"%vars_esc[i].get())
    for i in range(3, 6):
        txt_esc[i].set("%.0f deg"%vars_esc[i].get())
def cargar_piezas():
    for i in range(len(piezas)):
        nombre=piezas[i][0]
        archivo=piezas[i][1]
        ruta=os.path.join(carpeta, archivo)
        if not os.path.exists(ruta):
            print("ERROR: no se encontro", archivo, "en la carpeta", carpeta)
            salir()
        print("Importando", archivo, "...")
        modelo=mesh.Mesh.from_file(ruta)
        modelo.vectors*=ESCALA
        lista=glGenLists(1)
        glNewList(lista, GL_COMPILE)
        c=colores[i%len(colores)]
        glColor3f(c[0], c[1], c[2])
        glBegin(GL_TRIANGLES)
        for k in range(len(modelo.vectors)):
            glNormal3fv(modelo.normals[k])
            for vertice in modelo.vectors[k]:
                glVertex3fv(vertice)
        glEnd()
        glEndList()
        listas.append(lista)
        lista_piezas.insert(tk.END, "%s  -  %s  (%d triangulos)"%
                            (archivo, nombre, len(modelo.vectors)))
    print("Todas las piezas fueron importadas")
def dibujar_piso():
    glDisable(GL_LIGHTING)
    glLineWidth(1)
    glColor3f(0.35, 0.35, 0.4)
    glBegin(GL_LINES)
    for i in range(-10, 11):
        glVertex3f(i, 0,-10)
        glVertex3f(i, 0, 10)
        glVertex3f(-10, 0, i)
        glVertex3f(10, 0, i)
    glEnd()
def dibujar_brazo():
    a=[]
    for i in range(7):
        a.append(vars_art[i].get())
    for i in range(len(piezas)):
        desplaz=piezas[i][2]
        eje=piezas[i][3]
        art=piezas[i][4]
        tipo=piezas[i][5]
        rama=piezas[i][6]
        if rama:
            glPushMatrix()
        glTranslatef(desplaz[0]*ESCALA, desplaz[1]*ESCALA, desplaz[2]*ESCALA)
        if art is not None:
            if tipo=="giro":
                glRotatef(a[art], eje[0], eje[1], eje[2])
            else:
                glTranslatef(a[art]*eje[0]*ESCALA,
                             a[art]*eje[1]*ESCALA,
                             a[art]*eje[2]*ESCALA)
        glCallList(listas[i])
        if rama:
            glPopMatrix()
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    dist=var_zoom.get()
    ex=dist*cos(radians(cam_el))*sin(radians(cam_az))
    ey=dist*sin(radians(cam_el))
    ez=dist*cos(radians(cam_el))*cos(radians(cam_az))
    gluLookAt(ex, ey+3, ez, 0, 3, 0, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 1.0, 0.8, 0.0])
    dibujar_piso()
    glPushMatrix()
    glTranslatef(vars_esc[0].get(), vars_esc[1].get(), vars_esc[2].get())
    glRotatef(vars_esc[3].get(), 1, 0, 0)
    glRotatef(vars_esc[4].get(), 0, 1, 0)
    glRotatef(vars_esc[5].get(), 0, 0, 1)
    dibujar_brazo()
    glPopMatrix()
    glutSwapBuffers()
def reshape(w, h):
    global ancho, alto
    if h==0:
        h=1
    ancho, alto=w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.12, 0.12, 0.18, 1.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.35, 0.35, 0.35, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, ancho/alto, 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)
teclas_art={b'q': (0, 5), b'a': (0,-5),
              b'w': (1, 5), b's': (1,-5),
              b'e': (2, 5), b'd': (2,-5),
              b'r': (3, 5), b'f': (3,-5),
              b't': (4, 5), b'g': (4,-5),
              b'y': (5, 5), b'h': (5,-5),
              b'u': (6, 1), b'j': (6,-1)}
def teclado(tecla, x, y):
    if tecla==b'\x1b':
        salir()
    elif tecla in teclas_art:
        i=teclas_art[tecla][0]
        paso=teclas_art[tecla][1]
        nuevo=vars_art[i].get()+paso
        if nuevo<minimos[i]:
            nuevo=minimos[i]
        if nuevo>maximos[i]:
            nuevo=maximos[i]
        vars_art[i].set(nuevo)
    elif tecla==b'b':
        home_articulaciones()
def mouse(boton, estado, x, y):
    global arrastrando, mouse_x, mouse_y
    if boton==GLUT_LEFT_BUTTON:
        if estado==GLUT_DOWN:
            arrastrando=True
        else:
            arrastrando=False
        mouse_x=x
        mouse_y=y
    elif boton==3 and estado==GLUT_DOWN:
        nuevo=var_zoom.get()-1
        if nuevo<5:
            nuevo=5
        var_zoom.set(nuevo)
    elif boton==4 and estado==GLUT_DOWN:
        nuevo=var_zoom.get()+1
        if nuevo>30:
            nuevo=30
        var_zoom.set(nuevo)
def movimiento_mouse(x, y):
    global cam_az, cam_el, mouse_x, mouse_y
    if arrastrando:
        cam_az-=(x-mouse_x)*0.5
        cam_el+=(y-mouse_y)*0.5
        if cam_el>89.9:
            cam_el=89.9
        if cam_el<89.9:
            cam_el=89.9
        mouse_x=x
        mouse_y=y
def actualizar(valor):
    root.update()
    actualizar_textos()
    glutPostRedisplay()
    glutTimerFunc(16, actualizar, 0)
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(ancho, alto)
    glutInitWindowPosition(600, 40)
    glutCreateWindow(b"Brazo robotico 3D")
    init()
    cargar_piezas()
    actualizar_textos()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)
    glutMouseFunc(mouse)
    glutMotionFunc(movimiento_mouse)
    glutTimerFunc(0, actualizar, 0)
    glutMainLoop()
if __name__=="__main__":
    main()
