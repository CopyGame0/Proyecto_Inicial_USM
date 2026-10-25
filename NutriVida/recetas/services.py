"""
Toda la lógica que habla con la API de Spoonacular vive aquí.

La idea es que views.py no sepa NADA de la API: solo pide "dame un plan"
y recibe datos listos para mostrar. Así, si mañana cambian de API,
solo se toca este archivo.
"""
import unicodedata
from .traduccion import ErrorTraduccion, es_a_en_lista, en_a_es_lista
import requests
from django.conf import settings
from django.core.cache import cache

#funcion para traducir, usaremos esto mas tarde
def _traducir_ingredientes(lista):
    try:
        return es_a_en_lista(lista)
    except ErrorTraduccion:
        raise ErrorPlan("El traductor no está disponible ahora. Intente de nuevo "
                        "en un momento o escriba los ingredientes en inglés.")

URL_BUSQUEDA = "https://api.spoonacular.com/recipes/complexSearch"

DIAS_DEL_PLAN = 5          # el README dice "máximo 5 días"
COMIDAS_POR_DIA = 3
TOTAL_RECETAS = DIAS_DEL_PLAN * COMIDAS_POR_DIA

# ---------------------------------------------------------------------------
# Traducciones español -> valores que entiende Spoonacular (solo acepta inglés)
# ---------------------------------------------------------------------------
DIETAS = {
    "vegetariana": "vegetarian",
    "vegana": "vegan",
    "omnivora": "",          # "" = sin restricción de dieta
    "vegetarian": "vegetarian",
    "vegan": "vegan",
}

INTOLERANCIAS = {
    "lacteos": "dairy",
    "lactosa": "dairy",
    "gluten": "gluten",
    "huevo": "egg",
    "mani": "peanut",
    "cacahuate": "peanut",
    "nueces": "tree nut",
    "frutos secos": "tree nut",
    "soya": "soy",
    "soja": "soy",
    "mariscos": "shellfish",
    "pescado": "seafood",
    "sesamo": "sesame",
    "sulfitos": "sulfite",
    "trigo": "wheat",
}

# (nombre del campo en el formulario, nombre del parámetro en Spoonacular)
CAMPOS_NUMERICOS = [
    ("min_cal", "minCalories"),
    ("max_cal", "maxCalories"),
    ("min_protein", "minProtein"),
    ("max_protein", "maxProtein"),
    ("min_carbs", "minCarbs"),
    ("max_carbs", "maxCarbs"),
    ("min_sugar", "minSugar"),
    ("max_sugar", "maxSugar"),
]


class ErrorPlan(Exception):
    """Error que SÍ es seguro mostrarle al usuario (el mensaje es legible)."""


def _normalizar(texto):
    """'Omnívora ' -> 'omnivora' (minúsculas, sin tildes, sin espacios)."""
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def _lista_separada_por_comas(texto):
    return [p.strip() for p in texto.split(",") if p.strip()]


def construir_parametros(datos):
    """
    Convierte lo que llegó del formulario (request.GET) en los parámetros
    de Spoonacular. Lanza ErrorPlan si algo viene mal escrito.
    """
    params = {}

    # --- dieta ---------------------------------------------------------
    dieta = _normalizar(datos.get("diet", ""))
    if dieta and dieta not in DIETAS:
        raise ErrorPlan("Tipo de dieta no reconocido. Use: Vegetariana, Vegana u Omnívora.")
    if DIETAS.get(dieta):
        params["diet"] = DIETAS[dieta]

    # --- intolerancias (se traducen una por una) ------------------------
    traducidas = []
    for item in _lista_separada_por_comas(datos.get("intolerances", "")):
        clave = _normalizar(item)
        traducidas.append(INTOLERANCIAS.get(clave, clave))
    if traducidas:
        params["intolerances"] = ",".join(traducidas)

    # --- ingredientes (Spoonacular los entiende en inglés) -------------- 
    incluir = _traducir_ingredientes(_lista_separada_por_comas(datos.get("include_ingredients", "")))
    excluir = _traducir_ingredientes(_lista_separada_por_comas(datos.get("exclude_ingredients", "")))
    
    if incluir:
        params["includeIngredients"] = ",".join(incluir)
    if excluir:
        params["excludeIngredients"] = ",".join(excluir)

    # --- números --------------------------------------------------------
    valores = {}
    for campo, parametro in CAMPOS_NUMERICOS:
        bruto = datos.get(campo, "").strip()
        if not bruto:
            continue
        try:
            numero = float(bruto)
        except ValueError:
            raise ErrorPlan(f"El valor de «{campo}» debe ser un número.")
        if numero < 0:
            raise ErrorPlan(f"El valor de «{campo}» no puede ser negativo.")
        valores[campo] = numero
        params[parametro] = int(numero)

    # que el mínimo no sea mayor que el máximo
    for nombre in ("cal", "protein", "carbs", "sugar"):
        minimo, maximo = valores.get(f"min_{nombre}"), valores.get(f"max_{nombre}")
        if minimo is not None and maximo is not None and minimo > maximo:
            raise ErrorPlan(f"El mínimo de «{nombre}» no puede ser mayor que el máximo.")

    return params


def buscar_recetas(params):
    """Llama a Spoonacular y devuelve la lista cruda de recetas."""
    clave = getattr(settings, "SPOONACULAR_API_KEY", "")
    if not clave:
        raise ErrorPlan("Falta configurar la clave de Spoonacular (SPOONACULAR_API_KEY).")

    consulta = dict(params)
    consulta.update({
        "apiKey": clave,
        "number": TOTAL_RECETAS,
        "sort": "random",              # así cada consulta da un plan distinto
        "addRecipeInformation": "true",
        "addRecipeNutrition": "true",  # trae calorías, proteínas, etc.
    })

    try:
        respuesta = requests.get(URL_BUSQUEDA, params=consulta, timeout=15)
    except requests.RequestException:
        raise ErrorPlan("No se pudo conectar con Spoonacular. Intente de nuevo en un momento.")

    if respuesta.status_code in (401, 403):
        raise ErrorPlan("La clave de Spoonacular no es válida.")
    if respuesta.status_code == 402:
        raise ErrorPlan("Se agotó el límite diario de consultas de Spoonacular.")
    if respuesta.status_code != 200:
        raise ErrorPlan(f"Spoonacular respondió con un error ({respuesta.status_code}).")

    return respuesta.json().get("results", [])


def _nutriente(receta, nombre):
    """Busca un nutriente (Calories, Protein...) dentro de la receta."""
    for n in receta.get("nutrition", {}).get("nutrients", []):
        if n.get("name") == nombre:
            return round(n.get("amount", 0))
    return None


def simplificar(receta):
    """Deja solo los datos que la plantilla necesita."""
    return {
        "id": receta.get("id"),
        "titulo": receta.get("title", "Sin título"),
        "imagen": receta.get("image", ""),
        "minutos": receta.get("readyInMinutes"),
        "porciones": receta.get("servings"),
        "url": receta.get("sourceUrl", ""),
        "calorias": _nutriente(receta, "Calories"),
        "proteina": _nutriente(receta, "Protein"),
        "carbohidratos": _nutriente(receta, "Carbohydrates"),
        "azucar": _nutriente(receta, "Sugar"),
    }


def armar_plan(recetas):
    """
    Reparte las recetas en días: [{"dia": "Día 1", "comidas": [...]}, ...]
    Si Spoonacular devuelve menos de 15, se arman menos días.
    """
    recetas = [simplificar(r) for r in recetas]
  
    titulos = en_a_es_lista([r["titulo"] for r in recetas])
    for receta, titulo in zip(recetas, titulos):
        receta["titulo"] = titulo
    
    plan = []
    for i in range(DIAS_DEL_PLAN):
        comidas = recetas[i * COMIDAS_POR_DIA:(i + 1) * COMIDAS_POR_DIA]
        if comidas:
            plan.append({"dia": f"Día {i + 1}", "comidas": comidas})
    return plan


def generar_plan(datos):
    """Función principal: formulario -> plan semanal listo para mostrar."""
    params = construir_parametros(datos)
    recetas = buscar_recetas(params)
    return armar_plan(recetas)


URL_DETALLE = "https://api.spoonacular.com/recipes/{id}/information"


def obtener_receta(receta_id):
    """
    Trae UNA receta completa (ingredientes y pasos) y la traduce al español.
    Se guarda en caché 24 h: si otro usuario abre la misma receta, no se
    gasta ni la API de Spoonacular ni el traductor.
    """
    clave_cache = f"receta_{receta_id}"
    guardada = cache.get(clave_cache)
    if guardada:
        return guardada

    clave = getattr(settings, "SPOONACULAR_API_KEY", "")
    if not clave:
        raise ErrorPlan("Falta configurar la clave de Spoonacular (SPOONACULAR_API_KEY).")

    try:
        respuesta = requests.get(
            URL_DETALLE.format(id=receta_id),
            params={"apiKey": clave, "includeNutrition": "false"},
            timeout=15,
        )
    except requests.RequestException:
        raise ErrorPlan("No se pudo conectar con Spoonacular. Intente de nuevo en un momento.")

    if respuesta.status_code == 404:
        raise ErrorPlan("No encontramos esa receta.")
    if respuesta.status_code in (401, 403):
        raise ErrorPlan("La clave de Spoonacular no es válida.")
    if respuesta.status_code == 402:
        raise ErrorPlan("Se agotó el límite diario de consultas de Spoonacular.")
    if respuesta.status_code != 200:
        raise ErrorPlan(f"Spoonacular respondió con un error ({respuesta.status_code}).")

    datos = respuesta.json()
    titulo = datos.get("title", "Sin título")
    ingredientes = [i["original"] for i in datos.get("extendedIngredients", []) if i.get("original")]
    pasos = []
    for bloque in datos.get("analyzedInstructions", []):
        pasos += [p["step"] for p in bloque.get("steps", []) if p.get("step")]

    # Un solo viaje al traductor: título + ingredientes + pasos
    originales = [titulo] + ingredientes + pasos
    traducidos = en_a_es_lista(originales)
    n = len(ingredientes)

    receta = {
        "id": receta_id,
        "titulo": traducidos[0],
        "imagen": datos.get("image", ""),
        "minutos": datos.get("readyInMinutes"),
        "porciones": datos.get("servings"),
        "url": datos.get("sourceUrl", ""),
        "ingredientes": traducidos[1:1 + n],
        "pasos": traducidos[1 + n:],
    }

    # Si el traductor falló, en_a_es_lista devuelve la MISMA lista de entrada:
    # en ese caso no se guarda en caché, para reintentar la próxima vez.
    if traducidos is not originales:
        cache.set(clave_cache, receta, 60 * 60 * 24)
    return receta