import random
import time

# --- CONFIGURACIÓN DE LA SIMULACIÓN ---
TOTAL_COMPONENTES = 10
PROBABILIDAD_FALLO_COMPONENTE = 0.25

def simular_despliegue_componente():
    """Simula el despliegue de un componente. Devuelve True si tiene éxito."""
    time.sleep(0.1) # Hacemos la simulación un poco más rápida para la web
    return random.random() >= PROBABILIDAD_FALLO_COMPONENTE

# --- ESTRATEGIAS DE DESPLIEGUE ---

def simulador_big_bang():
    """Despliega todos los componentes. Si uno falla, todo falla."""
    inicio = time.time()
    fallos = sum(1 for _ in range(TOTAL_COMPONENTES) if not simular_despliegue_componente())
    
    tiempo_total = time.time() - inicio
    
    resultado = {
        "estrategia": "Big Bang",
        "tiempo": f"{tiempo_total:.2f}s",
        "riesgo": "Alto" if fallos > 0 else "Bajo",
        "descripcion": f"Despliegue fallido con {fallos} errores. Requiere rollback total." if fallos > 0 else "Despliegue completado con éxito."
    }
    return resultado

def simulador_faseado():
    """Despliega en fases. Si una fase falla, solo se revierte esa."""
    inicio = time.time()
    fallos_totales = 0
    fases = 2
    componentes_por_fase = TOTAL_COMPONENTES // fases
    
    for _ in range(fases):
        fallos_en_fase = sum(1 for _ in range(componentes_por_fase) if not simular_despliegue_componente())
        fallos_totales += fallos_en_fase

    tiempo_total = time.time() - inicio
    
    resultado = {
        "estrategia": "Faseado",
        "tiempo": f"{tiempo_total:.2f}s",
        "riesgo": "Medio" if fallos_totales > 0 else "Bajo",
        "descripcion": f"Despliegue parcialmente completado con {fallos_totales} errores." if fallos_totales > 0 else "Despliegue completado con éxito."
    }
    return resultado

def simulador_blue_green():
    """Despliega en un entorno nuevo y solo cambia si todo funciona."""
    inicio = time.time()
    # Simula tiempo extra para preparar el entorno "Green"
    time.sleep(0.5)
    fallos = sum(1 for _ in range(TOTAL_COMPONENTES) if not simular_despliegue_componente())

    tiempo_total = time.time() - inicio
    
    resultado = {
        "estrategia": "Blue-Green",
        "tiempo": f"{tiempo_total:.2f}s",
        "riesgo": "Muy Bajo",
        "descripcion": "Despliegue cancelado de forma segura. Cero impacto en el usuario." if fallos > 0 else "Despliegue completado con éxito."
    }
    return resultado

def ejecutar_todas_simulaciones():
    """Ejecuta todas las simulaciones y devuelve una lista de resultados."""
    resultados = [
        simulador_big_bang(),
        simulador_faseado(),
        simulador_blue_green()
    ]
    return resultados
