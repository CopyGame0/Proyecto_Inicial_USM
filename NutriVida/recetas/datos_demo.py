#Datos de demostracion, para probar la pagina y cambiar el Front-end sin usar las APIs
from django.conf import settings
from django.templatetags.static import static
import urllib.parse

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

    def generar_links(ingrediente):
   
      ingrediente_seguro = urllib.parse.quote(ingrediente)
      links = {"Jumbo" : f"https://www.jumbo.cl/busqueda?ft={ingrediente_seguro}",
              "Google": f"https://www.google.com/search?q={ingrediente_seguro}&udm=28",
              "Unimarc": f"https://www.unimarc.cl/search?q={ingrediente_seguro}",
              "Santa_Isabel": f"https://www.santaisabel.cl/busqueda?ft={ingrediente_seguro}"}
      return links
  
    ingredientes_falsos = [
        ("1 taza de arroz", "arroz"),
        ("2 tomates", "tomate"),
        ("Sal a gusto", "sal"),
    ]
    
    ingredientes_procesados = []
    for frase, nombre in ingredientes_falsos:
        ingredientes_procesados.append({
            "nombre": frase,                      
            "url_compra": generar_links(nombre),  
        })
  
    return {
      
      
        "id": receta_id,
        "titulo": f"Receta de ejemplo número {receta_id}",
        "imagen": static("recetas/demo.jpg"),
        "minutos": 30,
        "porciones": 4,
        "url": "https://example.com",
        "ingredientes": ingredientes_procesados,
        "pasos": ["Lavar el arroz.", "Cocinar 15 minutos.", "Servir caliente."],
    }