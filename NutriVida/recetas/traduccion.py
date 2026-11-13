#Traduccion, usaremos DeepL, ya que deep translator no funciono :P
#from deep_translator import GoogleTranslator

"""Traducir todo con diccionario llevaria mill años, y no pude encontrar APIs en español, asi que usaremos una API de traduccion, 
    para hacer Outsourcing como dicen los jovenes."""

import logging
import re
import deepl
from django.conf import settings

#Mas Fancy que print(error)
logger = logging.getLogger(__name__)

def _separar_pasos(pasos):
    resultados = []
    
    for paso in pasos:

        # Usamos la libreria "Regular expression operations", para separar despues de un punto, exclamaciono o pregunta. 
        # Solo si viene depues uma mayuscula, exclamaciono o pregunta.
        separacion = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡])', paso.strip())

        for paso_individual in separacion:
            paso_individual = paso_individual.strip()
            if paso_individual:
                resultados.append(paso_individual)
    
    
    return resultados
    

def traducir_receta(titulo, descripciones, nombres, pasos):
    """Traduce una receta completa en UN solo viaje a DeepL.

    Recibe el título, la descripción y el nombre limpio de cada ingrediente,
    y los pasos (todo en inglés). Devuelve un diccionario con lo mismo en
    español, más "ok" (False si DeepL falló y se devolvió el inglés)."""
    originales = [titulo] + descripciones + nombres + pasos
    try:
        traducidos = _traducir(originales, "EN", "ES")
        ok = True
    except ErrorTraduccion:
        traducidos, ok = originales, False

    n = len(descripciones)
    return {
        "titulo": traducidos[0],
        "descripciones": traducidos[1:1 + n],
        "nombres": traducidos[1 + n:1 + 2 * n],
        "pasos": _separar_pasos(traducidos[1 + 2 * n:]),
        "ok": ok,
    }

class ErrorTraduccion(Exception):
    pass


def _traducir(textos, origen, destino): 
    """Funcion de traduccion, 
        DeepL (ademas de la Key) nesesita: Texto a traducir, idioma de origen, idioma de destino"""
        
    clave = getattr(settings, "DEEPL_API_KEY", "")
    if not clave:
        raise ErrorTraduccion("Falta DEEPL_API_KEY")
    try:
        resultados = deepl.Translator(clave).translate_text(
            textos, source_lang=origen, target_lang=destino
        )
    except Exception:
        logger.exception("Falló la traducción con DeepL")
        raise ErrorTraduccion("DeepL no respondió")
    
    lista_textos = []
    for r in resultados: #No se porque arroja error en el VS code, pero funciona, asi que "If it ain't broken don't fix it".
        lista_textos.append(r.text)
    return lista_textos 


def es_a_en_lista(textos):
    if not textos:
        return []
    
    resultados = []
    for t in _traducir(textos, "ES", "EN-US"):
        limpio = t.strip().lower()
        resultados.append(limpio)
    return resultados


def en_a_es_lista(textos):
    """Para los títulos: si falla, se muestran en inglés (no es grave)."""
    if not textos:
        return []
    try:
        return _traducir(textos, "EN", "ES")
    except ErrorTraduccion:
        return textos