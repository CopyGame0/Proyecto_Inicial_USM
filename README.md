# Proyecto NutriVida
Proyecto inicial equipo 7 informática 2026

------------


Una aplicación web para ayudar a conseguir recetas en base a una pauta nutricional.

------------

## Funcionalidades planeadas
-  Búsqueda de recetas saludables adaptadas a las pautas nutricionales de cada usuario. (hecho)
- ~~Apartado especial para la entrega de recetas equilibradas aptas para niños, como postres o recetas entretenidas para fomentar el consumo de alimentos saludables.~~ (Descartado)
- Una lista de recetas para un máximo de 5 días. (Hecho)

------------


## Instrucciones de uso
#### Instalación
- (Recomendado) Crear un ambiente virtual `python -m venv .venv`
	- Entra al ambiente virtual `source .venv/bin/activate` o `.venv/bin/activate` (Windows PowerShell y Linux)
- Instalar las dependencias de requirements.txt: `pip install -r requirements.txt`
- Si no esta en la carpeta de origen, copiar el .env con las Keys de las API
- Iniciar la página web `py .\NutriVida\manage.py runserver`

#### Uso
1. Entrar en la página y hacer clic en el botón de empezar
2. Rellenar el formulario con las preferencias nutritivas; todos los campos son obligatorios, a menos que se diga lo contrario (se recomiendan rangos amplios).
3. Ver las recetas presionando los botones correspondientes (y disfrutar de la vida saludable :D)


------------



#### Instrucciones extra para el desarrollo
- En settings.py: MODO_DEMO = False:
  Cambiar a True para probar la interfaz sin utilizar las API (usa datos inventados)
  
- Errores de traducción:
	No se pudieron resolver errores de traducción específicos (E.g. Honey = Cariño), estos no se resolverán por el fin del desarrollo.


