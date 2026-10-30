from django.shortcuts import render

from .services import TOTAL_RECETAS, ErrorPlan, generar_plan, obtener_receta


def plan_semanal(request):
    """
    Recibe los datos del formulario por la URL (GET), consulta Spoonacular
    y muestra el plan. No se guarda nada en la base de datos.

    - Si la URL trae parcial=1 (lo envía el JavaScript del formulario),
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
    Devuelve SOLO el pedazo de HTML con una receta completa (ingredientes
    y pasos, ya en español). El JavaScript lo pega dentro de la ventana
    emergente de la página.
    """
    contexto = {"receta": None, "error": None}
    try:
        contexto["receta"] = obtener_receta(receta_id)
    except ErrorPlan as e:
        contexto["error"] = str(e)
    return render(request, "recetas/_detalle.html", contexto)