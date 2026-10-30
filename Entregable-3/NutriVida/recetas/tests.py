#No se como funcionan los Test, asi que no voy a tocar eso XD, seria bastante util para no gastar la API TBH.
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from .services import ErrorPlan, construir_parametros, generar_plan

RESPUESTA_FALSA = {
    "results": [
        {
            "title": f"Receta {i}",
            "image": "https://img.spoonacular.com/x.jpg",
            "readyInMinutes": 20,
            "servings": 2,
            "sourceUrl": "https://example.com/receta",
            "nutrition": {"nutrients": [
                {"name": "Calories", "amount": 350.4},
                {"name": "Protein", "amount": 25.2},
                {"name": "Carbohydrates", "amount": 40.0},
                {"name": "Sugar", "amount": 6.0},
            ]},
        }
        for i in range(15)
    ]
}

FORMULARIO = {
    "diet": "Vegetariana", "intolerances": "Lácteos, Gluten",
    "include_ingredients": "tomato, rice", "exclude_ingredients": "beef",
    "min_protein": "10", "max_protein": "40", "min_carbs": "20", "max_carbs": "80",
    "min_cal": "200", "max_cal": "600", "min_sugar": "0", "max_sugar": "15",
}


def respuesta(status=200, datos=None):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = datos if datos is not None else RESPUESTA_FALSA
    return r


class ConstruirParametrosTests(SimpleTestCase):
    def test_traduce_y_mapea_todos_los_campos(self):
        p = construir_parametros(FORMULARIO)
        self.assertEqual(p["diet"], "vegetarian")
        self.assertEqual(p["intolerances"], "dairy,gluten")
        self.assertEqual(p["includeIngredients"], "tomato,rice")
        self.assertEqual(p["excludeIngredients"], "beef")
        self.assertEqual(p["minCalories"], 200)
        self.assertEqual(p["maxCalories"], 600)
        self.assertEqual(p["minProtein"], 10)
        self.assertEqual(p["maxProtein"], 40)
        self.assertEqual(p["minCarbs"], 20)
        self.assertEqual(p["maxCarbs"], 80)
        self.assertEqual(p["minSugar"], 0)
        self.assertEqual(p["maxSugar"], 15)

    def test_omnivora_no_envia_dieta(self):
        self.assertNotIn("diet", construir_parametros({"diet": "Omnívora"}))

    def test_dieta_desconocida(self):
        with self.assertRaises(ErrorPlan):
            construir_parametros({"diet": "carnivora"})

    def test_minimo_mayor_que_maximo(self):
        with self.assertRaises(ErrorPlan):
            construir_parametros({"min_cal": "900", "max_cal": "100"})

    def test_numero_invalido(self):
        with self.assertRaises(ErrorPlan):
            construir_parametros({"min_cal": "abc"})


@override_settings(SPOONACULAR_API_KEY="clave-falsa")
class PlanTests(SimpleTestCase):
    @patch("recetas.services.requests.get")
    def test_arma_5_dias_de_3_comidas(self, get):
        get.return_value = respuesta()
        plan = generar_plan(FORMULARIO)
        self.assertEqual(len(plan), 5)
        self.assertTrue(all(len(d["comidas"]) == 3 for d in plan))
        self.assertEqual(plan[0]["comidas"][0]["calorias"], 350)
        # la clave y los filtros viajaron a la API
        enviados = get.call_args.kwargs["params"]
        self.assertEqual(enviados["apiKey"], "clave-falsa")
        self.assertEqual(enviados["diet"], "vegetarian")

    @patch("recetas.services.requests.get")
    def test_pocas_recetas_menos_dias(self, get):
        get.return_value = respuesta(datos={"results": RESPUESTA_FALSA["results"][:4]})
        plan = generar_plan({})
        self.assertEqual([len(d["comidas"]) for d in plan], [3, 1])

    @patch("recetas.services.requests.get")
    def test_limite_diario(self, get):
        get.return_value = respuesta(status=402)
        with self.assertRaises(ErrorPlan):
            generar_plan({})

    @override_settings(SPOONACULAR_API_KEY="")
    def test_sin_clave(self):
        with self.assertRaises(ErrorPlan):
            generar_plan({})


@override_settings(SPOONACULAR_API_KEY="clave-falsa", ROOT_URLCONF="recetas.test_urls")
class VistaTests(SimpleTestCase):
    @patch("recetas.services.requests.get")
    def test_vista_muestra_plan(self, get):
        get.return_value = respuesta()
        r = self.client.get("/plan/", FORMULARIO)
        self.assertContains(r, "Día 5")
        self.assertContains(r, "Receta 0")

    def test_vista_muestra_error(self):
        r = self.client.get("/plan/", {"diet": "carnivora"})
        self.assertContains(r, "Tipo de dieta no reconocido")
