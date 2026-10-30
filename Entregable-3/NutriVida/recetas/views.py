from django.shortcuts import render

from .services import TOTAL_RECETAS, ErrorPlan, generar_plan, obtener_receta


def plan_semanal(request):
    """
    Recibe datos del formulario por la URL (GET), consulta a la API de Spoonacular con estos datos
    y muestra el plan. No se guarda nada en la base de datos de momento, pq aun no implementamos usuarios.

    - Si la URL trae parcial=1 (En caso de no econtrar suficientes recetas. Lo envía el JavaScript del formulario),
      se devuelve solo el pedazo con las tarjetas.
    - Si no, se devuelve la página completa: 1 receta por día en el plan
      y el resto de las recetas en "Otras recetas".
    """
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

    plantilla = "recetas/_plan.html" if es_parcial else "recetas/plan.html"
    return render(request, plantilla, contexto)


def detalle_receta(request, receta_id):
    """
    Devuelve el pedazo de HTML con una receta completa (ingredientes y pasos, ya en español).
    El JavaScript lo pega dentro de la ventana emergente de la página.
    """
    
    contexto = {"receta": None, "error": None}
    try:
        contexto["receta"] = obtener_receta(receta_id)
        #Esto da error en el VS code y tampoco se pq; supongo que es pq es de una funcion externa al archivo IDK. Funciona y eso es lo importante.
    except ErrorPlan as e:
        contexto["error"] = str(e)                     
    return render(request, "recetas/_detalle.html", contexto)