#Datos de demostracion, para probar la pagina y cambiar el Front-end sin usar las APIs
from django.conf import settings
from django.templatetags.static import static

def _receta(i, con_imagen=True):
    return {
        "id": i,
        "titulo": f"Receta de ejemplo número {i}",
        "imagen": static("recetas/demo.jpg") if con_imagen else "",
        "minutos": 20 + i,
        "porciones": 2,
        "url": "https://example.com",
        "calorias": 350,
        "proteina": 25,
        "carbohidratos": 40,
        "azucar": 6,
    }
    
def plan_demo():
  plan = []
  for d in range(settings.DIAS_DEL_PLAN):
    
    comidas = []
    for c in range(settings.COMIDAS_POR_DIA):
      comidas.append(_receta(d * 3 + c + 1))
      
    # Build the dictionary for the day and add it to the plan
    dia_dict = {"dia": f"Día {d + 1}", "comidas": comidas}
    plan.append(dia_dict)

  return plan

def receta_demo(receta_id):
    return {
        "id": receta_id,
        "titulo": f"Receta de ejemplo número {receta_id}",
        "imagen": static("recetas/demo.jpg"),
        "minutos": 30,
        "porciones": 4,
        "url": "https://example.com",
        "ingredientes": ["1 taza de arroz", "2 tomates", "Sal a gusto"],
        "pasos": ["Lavar el arroz.", "Cocinar 15 minutos.", "Servir caliente."],
    }