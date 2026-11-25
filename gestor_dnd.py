"""Gestor de Personajes y Dados de Calabozos y Dragones (PyQt5) - Versión 3."""
import sys, json, random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QListWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QFormLayout)

ARCHIVO = "personajes.json"
ATRIBUTOS_BASE = {
    "Fuerza": 10,
    "Destreza": 10,
    "Constitución": 10,
    "Sabiduría": 10
}

def modificador(valor):  # Función matemática que calcula el bonificador oficial de D&D a partir del atributo
    return (valor - 10) // 2  # Resta 10 y aplica división entera (//) entre 2, redondeando siempre hacia abajo

class BotonAtributo(QPushButton):
    def __init__(self, nombre, al_cambiar):
        super().__init__()
        self.nombre = nombre
        self.al_cambiar = al_cambiar

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.al_cambiar(self.nombre, +1)
        elif e.button() == Qt.RightButton:
            self.al_cambiar(self.nombre, -1)
        super().mousePressEvent(e)

class GestorPersonajes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de personajes D&D")
        self.personajes = self.leer_archivo()
        self.atributos = dict(ATRIBUTOS_BASE)
        self.botones_atributos = dict()
        
        self.crear_interfaz()
        self.refrescar_lista_HUD()

    def agregar_boton(self, layout, texto, funcion):
        boton = QPushButton(texto)
        boton.clicked.connect(funcion)
        layout.addWidget(boton)

    def crear_interfaz(self):
        principal = QHBoxLayout()

        #Panel izquierdo: lista de personajes y sus botones
        izquierda = QVBoxLayout()
        izquierda.addWidget(QLabel("Personajes:"))
        self.lista = QListWidget()
        self.lista.setFixedWidth(180)
        self.lista.itemClicked.connect(self.mostrar_personaje)
        izquierda.addWidget(self.lista)

        botones = [("Nuevo", self.nuevo), ("Guardar", self.guardar), ("Eliminar", self.eliminar)]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(funcion)
            izquierda.addWidget(btn)

        principal.addLayout(izquierda)

        #Panel derecho: datos, HP, atributos, dados e historial
        derecha = QVBoxLayout()
        formulario = QFormLayout()
        self.entrada_nombre = QLineEdit()
        self.entrada_clase = QLineEdit()
        formulario.addRow("Nombre: ", self.entrada_nombre)
        formulario.addRow("Clase/Raza: ", self.entrada_clase)
        derecha.addLayout(formulario)

            #Fila HP y daño/curación rápida
        self.entrada_hp_actual = QLineEdit()
        self.entrada_hp_max = QLineEdit()
        fila_hp = QHBoxLayout()
        fila_hp.addWidget(QLabel("HP:"))
        fila_hp.addWidget(self.entrada_hp_actual)
        fila_hp.addWidget(QLabel("/"))
        fila_hp.addWidget(self.entrada_hp_max)

        # Agrega esto a fila_hp antes de meterla a derecha:
        self.entrada_cantidad = QLineEdit(placeholderText="Cantidad")  # Campo de texto con texto fantasma para indicar cuánto daño o cura aplicar[cite: 15]
        fila_hp.addWidget(self.entrada_cantidad)  # Añade el campo a la fila de HP[cite: 15]

        boton_dano = QPushButton("Daño")  # Crea el botón para infligir daño[cite: 15]
        boton_dano.clicked.connect(lambda: self.cambiar_hp(-1))  # Conecta el botón llamando a cambiar_hp con signo negativo[cite: 15]
        fila_hp.addWidget(boton_dano)  # Añade el botón de daño a la fila[cite: 15]

        boton_curar = QPushButton("Curar")  # Crea el botón para recuperar salud[cite: 15]
        boton_curar.clicked.connect(lambda: self.cambiar_hp(+1))  # Conecta el botón llamando a cambiar_hp con signo positivo[cite: 15]
        fila_hp.addWidget(boton_curar)  # Añade el botón de curar a la fila[cite: 15]

        derecha.addLayout(fila_hp)

        derecha.addWidget(QLabel("Atributos (clic izquierdo: +1, clic derecho: -1)"))

        derecha.addWidget(QLabel("Dados:"))
        fila_dados = QHBoxLayout()

        boton_d6 = QPushButton("Tirar D6")
        boton_d6.clicked.connect(self.tirar_d6)
        fila_dados.addWidget(boton_d6)

        boton_d20 = QPushButton("Tirar D20")
        boton_d20.clicked.connect(self.tirar_d20)
        fila_dados.addWidget(boton_d20)

        derecha.addLayout(fila_dados)

        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        derecha.addWidget(self.historial)        
        
        principal.addLayout(derecha)

        fila_attr = QHBoxLayout()  # Layout horizontal para acomodar los 4 botones de atributos uno al lado del otro
        for nombre in self.atributos:  # Recorre las claves del diccionario: "Fuerza", "Destreza", "Constitución", "Sabiduría"
            boton = BotonAtributo(nombre, self.cambiar_atributo)  # Crea nuestro botón especial pasándole el nombre y la función a ejecutar
            self.botones_atributos[nombre] = boton  # Guarda la referencia del botón en el diccionario para poder actualizar su texto después
            self.actualizar_boton(nombre)  # Llama al método para asignarle su texto inicial formateado
            fila_attr.addWidget(boton)  # Añade el botón al contenedor horizontal
        derecha.addLayout(fila_attr)  # Inserta la fila de atributos en la columna derecha de la ventana

        self.setLayout(principal)

    def tirar_d6(self):
        self.historial.append(f"Tiraste un D6: {random.randint(1,6)}")

    def tirar_d20(self):
        base = random.randint(1, 20)  # Genera el tiro crudo del dado d20 (entre 1 y 20)[cite: 15]
        mod = modificador(self.atributos["Fuerza"])  # Calcula el modificador numérico correspondiente a la Fuerza actual[cite: 15]
        self.historial.append(f"Tiraste D20: {base} + Mod. Fuerza ({mod:+d}) = Total: {base + mod}")  # Muestra el desglose detallado en el registro[cite: 15]

    def leer_archivo(self):
        try:
            with open(ARCHIVO, "r", encoding = "utf-8") as a:
                return json.load(a)
        except (FileNotFoundError, json.JSONDecodeError): #Si no encuentra el archivo o si está dañado
            return {} #Diccionario vacío

    def escribir_archivo(self):
        with open(ARCHIVO, "w", encoding = "utf-8") as a:
            json.dump(self.personajes, a, indent= 4, ensure_ascii= False)

    def refrescar_lista_HUD(self, seleccion = ""):
        self.lista.clear()
        self.lista.addItems(sorted(self.personajes))
        for item in self.lista.findItems(seleccion, Qt.MatchExactly): #falta explicación
            self.lista.setCurrentItem(item)

    def guardar(self):
        nombre = self.entrada_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El personaje necesita un nombre.")
            return
        try:
            ficha = {
                "clase": self.entrada_clase.text().strip(),
                "hp_actual": int(self.entrada_hp_actual.text()),
                "hp_max": int(self.entrada_hp_max.text()),
                "atributos": dict(self.atributos)
            }
        except ValueError:
            QMessageBox.warning(self, "Error", "Los HP deben ser números enteros.")
            return

        self.personajes[nombre] = ficha
        self.escribir_archivo()
        self.refrescar_lista_HUD(nombre)

    def mostrar_personaje(self, item):
        ficha = self.personajes[item.text()]
        self.entrada_nombre.setText(item.text())
        self.entrada_clase.setText(ficha.get("clase", ""))
        self.entrada_hp_actual.setText(str(ficha.get("hp_actual","")))
        self.entrada_hp_max.setText(str(ficha.get("hp_max","")))
        self.poner_atributos(ficha.get("atributos", {}))  # Rellena los botones de atributos con los datos del personaje seleccionado

    def nuevo(self):
        self.entrada_nombre.clear()
        self.entrada_clase.clear()
        self.entrada_hp_actual.clear()
        self.entrada_hp_max.clear()
        self.poner_atributos(ATRIBUTOS_BASE)
        self.lista.setCurrentRow(-1)

    def eliminar(self):
        item = self.lista.currentItem()
        if not item:
            return
        if QMessageBox.question(self, "Eliminar", f"¿Eliminar a {item.text()}?") == QMessageBox.Yes:
            del self.personajes[item.text()]
            self.escribir_archivo()
            self.refrescar_lista_HUD()
            self.nuevo()

    def actualizar_boton(self, nombre):  # Método que refresca el texto del botón cuando el atributo cambia
        valor = self.atributos[nombre]  # Obtiene el valor numérico actual del atributo (ej: 16)
        self.botones_atributos[nombre].setText(f"{nombre}: {valor} ({modificador(valor):+d})")  # Cambia el texto mostrando el modificador con signo (+d)

    def cambiar_atributo(self, nombre, cambio):  # Método que se activa tanto con clic izquierdo (+1) como con clic derecho (-1)
        self.atributos[nombre] = max(1, min(20, self.atributos[nombre] + cambio))  # Limita el valor para que nunca baje de 1 ni suba de 20
        self.actualizar_boton(nombre)  # Refresca el texto visible del botón modificado

    def poner_atributos(self, valores):  # Carga un conjunto de atributos desde una ficha guardada y actualiza los botones
        for nombre in ATRIBUTOS_BASE:  # Recorre los cuatro atributos estándar
            self.atributos[nombre] = valores.get(nombre, 10)  # Extrae el valor guardado o asigna 10 por defecto si no existía
            self.actualizar_boton(nombre)  # Actualiza el botón correspondiente en la interfaz[cite: 15]
    def cambiar_hp(self, signo):  # Recibe -1 para daño o +1 para curación[cite: 15]
        try:  # Bloque de seguridad para validar entradas numéricas[cite: 15]
            actual = int(self.entrada_hp_actual.text())  # Convierte el HP actual de la pantalla a número entero[cite: 15]
            maximo = int(self.entrada_hp_max.text())  # Convierte el HP máximo a número entero[cite: 15]
            cantidad = abs(int(self.entrada_cantidad.text()))  # Convierte la cantidad a entero positivo usando abs()[cite: 15]
        except ValueError:  # Se dispara si los campos están vacíos o contienen letras[cite: 15]
            QMessageBox.warning(self, "Error", "Completa HP actual, HP máximo y cantidad.")  # Advierte al usuario sobre el dato inválido[cite: 15]
            return  # Cancela la operación sin alterar los datos[cite: 15]

        nuevo = max(0, actual - cantidad) if signo < 0 else min(maximo, actual + cantidad)  # Resta sin bajar de 0 o suma sin superar el máximo[cite: 15]
        self.entrada_hp_actual.setText(str(nuevo))  # Muestra el nuevo valor numérico en el campo de texto de HP actual[cite: 15]
        self.historial.append(f"HP: {actual} -> {nuevo}")  # Escribe en el historial el cambio de vida registrado[cite: 15]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestorPersonajes()
    ventana.show()
    sys.exit(app.exec_())