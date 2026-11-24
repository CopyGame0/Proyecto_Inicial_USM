# NutriVida

Aplicación web que genera un plan de comidas de hasta 5 días a partir de una pauta nutricional (calorías, proteínas, carbohidratos y azúcar), con recetas en español y enlaces para comprar los ingredientes en supermercados chilenos.

Proyecto inicial, Equipo 7 "Los cinco furiosos", Informática 2026.

> **Estado: finalizado y archivado.** Ver [Limitaciones conocidas](#limitaciones-conocidas).

---

## Funcionalidades
- Búsqueda de recetas según dieta (vegetariana, vegana, omnívora, sin gluten, keto), intolerancias, ingredientes a incluir/excluir y rangos nutricionales.
- Plan semanal de 5 días, con las demás recetas en "Otras recetas".
- Detalle de cada receta (ingredientes y pasos) traducido al español.
- Lista de compras con enlaces a Jumbo, Unimarc y Santa Isabel.
- Modo demo para probar la interfaz sin consumir APIs.

## Tecnologías
- Python y Django 6.1
- API de [Spoonacular](https://spoonacular.com/food-api) (recetas)
- DeepL (traducción principal) y Azure AI Translator (respaldo)

## Instalación
1. Clona el repositorio y entra a la carpeta.
2. Crea y activa un entorno virtual:
   - Windows: `python -m venv .venv` y luego `.venv\Scripts\activate`
   - Linux/Mac: `python -m venv .venv` y luego `source .venv/bin/activate`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Copia `.env.example` como `.env` y completa tus claves:
   - `SPOONACULAR_API_KEY`
   - `DEEPL_API_KEY`
   - `AZURE_TRANSLATOR_KEY` y `AZURE_TRANSLATOR_REGION` (opcionales, solo respaldo)
5. Inicia el servidor: `python NutriVida/manage.py runserver`
6. Abre http://127.0.0.1:8000/

## Uso
1. Haz clic en **Comenzar mi búsqueda**.
2. Completa el formulario (todos los campos son obligatorios salvo los marcados como opcionales; se recomiendan rangos amplios).
3. Revisa tu plan y presiona **Ver receta** para ver el detalle o la lista de compras.

## Modo demo
En `NutriVida/mysite/settings.py` cambia `MODO_DEMO = True` para usar datos de ejemplo sin gastar cuota de las APIs.

## Limitaciones conocidas
- La cuenta gratuita de Spoonacular tiene límite diario de consultas.
- Errores de traducción puntuales (por ejemplo "honey" como "cariño") no se corrigieron.
- No hay usuarios ni base de datos: la app `login` no está implementada y el plan no se guarda.
- Algunos tests quedaron desactualizados respecto a la configuración actual (`COMIDAS_POR_DIA = 2`).

## Licencia
MIT. Ver el archivo [LICENSE](LICENSE).
