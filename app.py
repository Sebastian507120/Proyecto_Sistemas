# Importamos las librerías necesarias
from flask import Flask, render_template, request, redirect, url_for
import datetime # Para obtener la fecha y hora actual
import spacy # ¡Importamos spaCy!

### NUEVO ### - Importamos las funciones de nuestros otros archivos
from simulador import ejecutar_todas_simulaciones
from dashboard_generator import generar_dashboard_data # <-- ESTA LÍNEA FALTABA

# Creamos la aplicación web.
app = Flask(__name__)

# --- Cargar Modelo de IA ---
# Cargamos el modelo de español de spaCy una sola vez al iniciar la app.
nlp = spacy.load("es_core_news_sm")


# --- Base de Datos Temporal ---
# Usamos una lista en memoria para guardar los tickets.
tickets_db = []
ticket_id_counter = 1 # Un contador para generar IDs únicos


# --- Lógica del Chatbot (CON SPACY) ---
def chatbot_analiza_prioridad(descripcion):
    """
    Analiza la descripción de un problema usando spaCy para asignar una prioridad
    basada en la similitud semántica con frases de ejemplo.
    """
    # Procesamos la descripción del usuario con el modelo de spaCy
    doc_usuario = nlp(descripcion.lower())

    # Definimos nuestras plantillas de problemas para cada prioridad
    plantillas_prioridad = {
        "Crítico": [
            "El sistema está completamente caído.",
            "No puedo acceder a la aplicación.",
            "El servidor no responde.",
            "Hay una brecha de seguridad grave."
        ],
        "Alto": [
            "La aplicación funciona muy lenta.",
            "Recibo un mensaje de error al intentar guardar.",
            "Una función principal no está operando correctamente.",
            "La página tarda demasiado en cargar.",
            "No se puede iniciar sesión, el sistema está lento.",
            "El reporte se queda congelado."
        ],
        "Medio": [
            "Tengo una duda sobre cómo exportar un reporte.",
            "Necesito ayuda para configurar mi cuenta.",
            "No entiendo cómo funciona una característica.",
            "Quisiera saber dónde encontrar el manual de usuario."
        ],
        "Bajo": [
            "Hay un error de tipeo en la página de contacto.",
            "Me gustaría sugerir una nueva funcionalidad.",
            "El color de un botón podría mejorar.",
            "El logo se ve un poco mal."
        ]
    }

    mejor_prioridad = "Bajo"  # Prioridad por defecto
    max_similitud = 0.0

    # Iteramos sobre cada prioridad y sus plantillas
    for prioridad, plantillas in plantillas_prioridad.items():
        for plantilla in plantillas:
            # Procesamos cada plantilla con spaCy
            doc_plantilla = nlp(plantilla.lower())
            
            # Calculamos la similitud entre la descripción del usuario y la plantilla
            similitud = doc_usuario.similarity(doc_plantilla)
            
            # Si encontramos una similitud más alta, la guardamos
            if similitud > max_similitud:
                max_similitud = similitud
                mejor_prioridad = prioridad
    
    # Si la similitud máxima es muy baja, la dejamos como "Bajo".
    # Esto evita falsos positivos. Un 0.4 es un umbral razonable para empezar.
    if max_similitud < 0.4:
        return "Bajo"
        
    return mejor_prioridad


# --- Rutas de la Aplicación Web ---

# Ruta para la página principal ('/')
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el formulario cuando un usuario envía un ticket
@app.route('/crear_ticket', methods=['POST'])
def crear_ticket():
    global ticket_id_counter # Usamos el contador global
    
    # Obtenemos los datos del formulario que el usuario llenó
    usuario = request.form['usuario']
    descripcion = request.form['descripcion']

    # 1. El chatbot con spaCy analiza la descripción para asignar una prioridad
    prioridad = chatbot_analiza_prioridad(descripcion)

    # 2. Creamos un nuevo ticket
    nuevo_ticket = {
        "id": ticket_id_counter,
        "usuario": usuario,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "Abierto",
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 3. Guardamos el ticket en nuestra "base de datos"
    tickets_db.append(nuevo_ticket)
    ticket_id_counter += 1 # Incrementamos el contador para el próximo ticket

    # 4. Redirigimos al usuario a la página que muestra todos los tickets
    return redirect(url_for('ver_tickets'))

# Ruta para mostrar todos los tickets creados
@app.route('/tickets')
def ver_tickets():
    return render_template('tickets.html', tickets=tickets_db)


# Las rutas para el simulador
@app.route('/simulador')
def pagina_simulador():
    return render_template('simulador.html')

@app.route('/ejecutar_simulacion', methods=['POST'])
def ejecutar_simulacion():
    resultados_simulacion = ejecutar_todas_simulaciones()
    return render_template('simulador.html', resultados=resultados_simulacion)


### NUEVO ### - La ruta para el Dashboard que faltaba
@app.route('/dashboard')
def dashboard():
    # 1. Llama a la función para generar los datos y el gráfico
    kpis = generar_dashboard_data(tickets_db)
    # 2. Muestra la página HTML y le pasa los KPIs
    return render_template('dashboard.html', kpis=kpis)


# --- Iniciar la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)

