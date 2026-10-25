#Traduccion, usaremos DeepL, ya que deep translator no funciono :P
#from deep_translator import GoogleTranslator

import logging

import deepl
from django.conf import settings

logger = logging.getLogger(__name__)


class ErrorTraduccion(Exception):
    pass


def _traducir(textos, origen, destino):
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
    return [r.text for r in resultados]


def es_a_en_lista(textos):
    if not textos:
        return []
    return [t.strip().lower() for t in _traducir(textos, "ES", "EN-US")]


def en_a_es_lista(textos):
    """Para los títulos: si falla, se muestran en inglés (no es grave)."""
    if not textos:
        return []
    try:
        return _traducir(textos, "EN", "ES")
    except ErrorTraduccion:
        return textos