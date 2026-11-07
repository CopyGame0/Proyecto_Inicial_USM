import urllib.parse
from django.shortcuts import render
from .services import TOTAL_RECETAS, ErrorPlan, generar_plan, obtener_receta

def plan_semanal(request):
    contexto = {"plan": [], "otras_recetas": [], "error": None, "total": 0, "maximo": TOTAL_RECETAS}
    try:
        contexto["plan"] = generar_plan(request.GET)
        contexto["total"] = sum(len(d["comidas"]) for d in contexto["plan"])
    except ErrorPlan as e:
        contexto["error"] = str(e)

    es_parcial = request.GET.get("parcial")

    if not es_parcial:
        plan_corto = []
        otras = []
        for dia in contexto["plan"]:
            plan_corto.append(dict(dia, comidas=dia["comidas"][:1]))
            otras.extend(dia["comidas"][1:])
        contexto["plan"] = plan_corto
        contexto["otras_recetas"] = otras

    for receta in contexto["otras_recetas"]:
        if "ingredientes" in receta and isinstance(receta["ingredientes"], list):
            receta["compra_ingredientes"] = [
                {
                    "nombre": ing,
                    "url_supermercado": f"https://www.google.com/search?q={urllib.parse.quote(ing + ' comprar supermercado')}"
                }
                for ing in receta["ingredientes"]
            ]
    
    for dia in contexto["plan"]:
        for receta in dia.get("comidas", []):
            if "ingredientes" in receta and isinstance(receta["ingredientes"], list):
               
                lista_compra = []
                
                for ing in receta["ingredientes"]:
        
                    item_ingrediente = {
                        "nombre": ing,
                        "url_supermercado": f"https://www.google.com/search?q={urllib.parse.quote(ing + ' comprar supermercado')}"
                    }
                  
                    lista_compra.append(item_ingrediente)
                
               
                receta["compra_ingredientes"] = lista_compra

        plantilla = "recetas/_plan.html" if es_parcial else "recetas/plan.html"
        return render(request, plantilla, contexto)


def detalle_receta(request, receta_id):
    contexto = {"receta": None, "error": None}
    try:
        receta = obtener_receta(receta_id)
        if receta and "ingredientes" in receta and isinstance(receta["ingredientes"], list):
            receta["compra_ingredientes"] = [
                {
                    "nombre": ing,
                    "url_supermercado": f"https://www.google.com/search?q={urllib.parse.quote(ing + ' comprar supermercado')}"
                }
                for ing in receta["ingredientes"]
            ]
        contexto["receta"] = receta
    except ErrorPlan as e:
        contexto["error"] = str(e)

    return render(request, "recetas/_detalle.html", contexto)