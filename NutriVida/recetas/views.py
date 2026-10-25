from django.shortcuts import render

from .services import TOTAL_RECETAS, ErrorPlan, generar_plan


def plan_semanal(request):
    """
    Recibe los datos del formulario por la URL (GET), consulta Spoonacular
    y muestra el plan. No se guarda nada en la base de datos.

    - Si la URL trae parcial=1 (lo envía el JavaScript del formulario),
      se devuelve solo el pedazo con las tarjetas.
    - Si no, se devuelve la página completa.
    """
    contexto = {"plan": [], "error": None, "total": 0, "maximo": TOTAL_RECETAS}
    try:
        contexto["plan"] = generar_plan(request.GET)
        contexto["total"] = sum(len(d["comidas"]) for d in contexto["plan"])
    except ErrorPlan as e:
        contexto["error"] = str(e)

    plantilla = "recetas/_plan.html" if request.GET.get("parcial") else "recetas/plan.html"
    return render(request, plantilla, contexto)
