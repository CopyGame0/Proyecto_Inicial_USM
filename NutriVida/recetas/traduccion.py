#Traduccion, usaremos DeepL como traductor principal, Azure IA Translator como alternativa.

"""Traducir todo con diccionario llevaria mill años, y no pude encontrar APIs en español, asi que usaremos una API de traduccion, 
    para hacer Outsourcing como dicen los jovenes."""

import logging
import re
import requests
import deepl
from django.conf import settings

#Mas Fancy que print(error)
logger = logging.getLogger(__name__)

# Azure acepta hasta 1000 textos por peticion. Nosotros Usaremos lotes mas pequeños por seguridad
AZURE_TEXTOS_POR_LOTE = 100
AZURE_TIMEOUT = 10  # segundos


class ErrorTraduccion(Exception):
    pass


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
    """Traduce una receta completa en UN solo viaje al traductor.

    Recibe el título, la descripción y el nombre limpio de cada ingrediente,
    y los pasos (todo en inglés). Devuelve un diccionario con lo mismo en
    español, más "ok" (False si ningun traductor respondio y se devolvió el inglés)."""
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


def _traducir_deepl(textos, origen, destino):
    #Traduccion con DeepL (ademas de la Key) pide: Texto a traducir, idioma original, idioma deseado

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


def _traducir_azure(textos, origen, destino):
    #Traduccion con Azure AI Translator (REST). Necesita AZURE_TRANSLATOR_KEY (API key) y AZURE_TRANSLATOR_REGION (region).
    
    #POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=es

    clave = getattr(settings, "AZURE_TRANSLATOR_KEY", "")
    if not clave:
        raise ErrorTraduccion("Falta AZURE_TRANSLATOR_KEY")

    endpoint = getattr(settings, "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    region = getattr(settings, "AZURE_TRANSLATOR_REGION", "")

    headers = {
        "Ocp-Apim-Subscription-Key": clave,
        "Content-Type": "application/json",
    }
    if region:
        headers["Ocp-Apim-Subscription-Region"] = region

    params = {
        "api-version": "3.0",
        "from": origen.split("-")[0].lower(),
        "to": destino.split("-")[0].lower(),
    }

    lista_textos = []
    for i in range(0, len(textos), AZURE_TEXTOS_POR_LOTE):
        lote = textos[i:i + AZURE_TEXTOS_POR_LOTE]
        cuerpo = [{"Text": t} for t in lote]
        try:
            respuesta = requests.post(
                f"{endpoint.rstrip('/')}/translate",
                params=params, headers=headers, json=cuerpo, timeout=AZURE_TIMEOUT,
            )
            respuesta.raise_for_status()
            datos = respuesta.json()
            traducidos = [item["translations"][0]["text"] for item in datos]
        except Exception:
            logger.exception("Falló la traducción con Azure Translator")
            raise ErrorTraduccion("Azure Translator no respondió")

        if len(traducidos) != len(lote):
            logger.error("Azure devolvió %d textos y se enviaron %d", len(traducidos), len(lote))
            raise ErrorTraduccion("Azure Translator devolvió una respuesta incompleta")
        lista_textos.extend(traducidos)

    return lista_textos


def _traducir(textos, origen, destino):
    """Intenta DeepL primero; si falla, usa Azure como respaldo.
    Si ambos fallan, lanza ErrorTraduccion."""
    try:
        return _traducir_deepl(textos, origen, destino)
    except ErrorTraduccion as error_deepl:
        logger.warning("DeepL no disponible (%s). Probando con Azure Translator.", error_deepl)

    try:
        return _traducir_azure(textos, origen, destino)
    except ErrorTraduccion as error_azure:
        logger.error("Tampoco funcionó Azure Translator (%s). Es nuestro fin.", error_azure)
        raise ErrorTraduccion("Ningún traductor está disponible")


def es_a_en_lista(textos):
    if not textos:
        return []
    
    resultados = []
    for t in _traducir(textos, "ES", "EN-US"):
        limpio = t.strip().lower()
        resultados.append(limpio)
    return resultados


def en_a_es_lista(textos):
    #Para los títulos: si falla, se muestran en inglés (no es grave).
    if not textos:
        return []
    try:
        return _traducir(textos, "EN", "ES")
    except ErrorTraduccion:
        return textos