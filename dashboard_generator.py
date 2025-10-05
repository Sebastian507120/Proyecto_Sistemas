import matplotlib
# ¡ESTA ES LA LÍNEA MÁGICA! Debe ir ANTES de importar pyplot.
# Le dice a Matplotlib que use un motor gráfico que no necesita ventanas.
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os

def generar_dashboard_data(tickets):
    """
    Analiza la lista de tickets para calcular KPIs y generar gráficos.
    """
    # --- 1. Calcular KPIs ---
    total_tickets = len(tickets)
    tickets_abiertos = sum(1 for t in tickets if t['estado'] == 'Abierto')
    
    kpis = {
        "total_tickets": total_tickets,
        "tickets_abiertos": tickets_abiertos
    }

    # --- 2. Preparar Datos para el Gráfico ---
    # Contamos cuántos tickets hay de cada prioridad
    conteo_prioridades = {"Crítico": 0, "Alto": 0, "Medio": 0, "Bajo": 0}
    for ticket in tickets:
        if ticket['prioridad'] in conteo_prioridades:
            conteo_prioridades[ticket['prioridad']] += 1
            
    prioridades = list(conteo_prioridades.keys())
    valores = list(conteo_prioridades.values())

    # --- 3. Generar el Gráfico con Matplotlib ---
    fig, ax = plt.subplots() # Crea una figura y un eje para el gráfico
    
    colores = ['#dc3545', '#ffc107', '#17a2b8', '#28a745']
    ax.bar(prioridades, valores, color=colores)
    
    ax.set_ylabel('Número de Tickets')
    ax.set_title('Distribución de Tickets por Prioridad')
    
    # Asegurarnos de que la carpeta 'static' exista
    if not os.path.exists('static'):
        os.makedirs('static')
        
    # Guardamos el gráfico como una imagen PNG en la carpeta 'static'
    # Flask usa esta carpeta para servir archivos como imágenes, CSS, etc.
    plt.savefig('static/grafico_prioridades.png')
    plt.close(fig) # Cerramos la figura para liberar memoria

    return kpis

