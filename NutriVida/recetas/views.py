from django.shortcuts import render

from .services import ErrorPlan, generar_plan


def plan_semanal(request):
    """
    Recibe los datos del formulario por la URL (GET), consulta Spoonacular
    y muestra el plan. No se guarda nada en la base de datos.
    """
    contexto = {"plan": [], "error": None}
    try:
        contexto["plan"] = generar_plan(request.GET)
    except ErrorPlan as e:
        contexto["error"] = str(e)
    return render(request, "recetas/plan.html", contexto)
