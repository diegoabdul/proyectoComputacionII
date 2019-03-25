from Vista.VistaVentanaEntrenamientoSQL import *
import Controlador.ControladorVentanaEntrenamientoSQL as ventanaEntrenamientoSQL
import Controlador.ControladorVentanaEntrenamiento as ventanaEntrenamiento
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="vtc.hopto.org",
  user="diego",
  passwd="Galicia96.",
    database="vtc"
)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    flagDirectorio = False
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.btn_atras.clicked.connect(self.volverAtras)
        self.btn_obtener.clicked.connect(self.obtener)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT URL FROM paginaweb")
        myresult = mycursor.fetchall()
        for x in myresult:
            URL = x[0]
            self.comboBox.addItem(URL[0:50])
        mycursor.close()

    def volverAtras(self):
        self.Open = ventanaEntrenamiento.NewApp()
        self.Open.show()
        self.close()

    def obtener(self):

        mycursor = mydb.cursor()
        mycursor.execute("SELECT ID_PaginaWeb FROM paginaweb WHERE URL LIKE %s", ('%'+self.comboBox.currentText()+'%',))
        myresult = mycursor.fetchall()
        for x in myresult:
            ID = x[0]
        mycursor.close()

        path = os.getcwd() + '/Valoraciones'

        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

        path = os.getcwd() + '/Valoraciones/Buenas'

        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT Nombre FROM paginaweb WHERE ID_PaginaWeb=%s", (ID,))
        myresult = mycursor.fetchall()
        for x in myresult:
            NombreArchivo = x[0]
        mycursor.close()

        mycursor = mydb.cursor()
        mycursor.execute("SELECT Nota,Texto FROM opinion WHERE ID_PaginaWeb=%s and Label='Buenas'", (ID,))
        myresult = mycursor.fetchall()
        i = 0
        for x in myresult:
            i += 1
            Nota = x[0]
            Texto = x[1]
            NotaGuardar = str(Nota)
            f = open(path + "/" + NombreArchivo + "_" + str(i) + ".txt", "w+")
            f.write(NotaGuardar + ' ' + Texto)
            f.close()
        mycursor.close()

        path = os.getcwd() + '/Valoraciones/Malas'

        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT Nombre FROM paginaweb WHERE ID_PaginaWeb=%s", (ID,))
        myresult = mycursor.fetchall()
        for x in myresult:
            NombreArchivoMalas = x[0]
        mycursor.close()

        mycursor = mydb.cursor()
        mycursor.execute("SELECT Nota,Texto FROM opinion WHERE ID_PaginaWeb=%s and Label='Malas'", (ID,))
        myresult = mycursor.fetchall()
        for x in myresult:
            i += 1
            Nota2 = x[0]
            Texto2 = x[1]
            NotaGuardar2 = str(Nota2)
            f = open(path + "/" + NombreArchivoMalas + "_" + str(i) + ".txt", "w+")
            f.write(NotaGuardar2 + ' ' + Texto2)
            f.close()
        mycursor.close()
        self.flagborrar = False
        MainWindow.flagDirectorio = True
        QMessageBox.about(self, "Ok", "Se ha guardado correctamente")
        self.volverAtras()
