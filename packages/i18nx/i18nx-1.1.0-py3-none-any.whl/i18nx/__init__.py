"""Internationalization module for Python"""

from typing import List, Dict, Any

class I18n:
  """I18n class"""

  raw: Dict[str, Dict[str, Any]]
  def __init__(
    self,
    locale: str,
    fallback_locale: str,
    translations: Dict[str, Dict[str, Any]],
    show_warning = False
  ):
    """Initializer"""

    self._locale = locale
    self._fallback_locale = fallback_locale
    self._show_warning = show_warning
    self._raw = translations
    self._translations = {
      lang: self._flatten(messages) for lang, messages in translations.items()
    }

    for lang in [locale, fallback_locale]:
      if lang not in self._translations:
        self._translations[lang] = {}

  @property
  def locale(self):
    """Active locale"""
    return self._locale

  @locale.setter
  def locale(self, value: str):
    """Set active locale"""
    self._locale = value

  @property
  def fallback_locale(self):
    """Fallback locale"""
    return self._fallback_locale

  @fallback_locale.setter
  def fallback_locale(self, value: str):
    """Set active locale"""
    self._fallback_locale = value

  @property
  def available_locales(self):
    """Available locales"""
    return self._translations.keys()

  @property
  def raw(self) -> dict:
    """Raw translations object for the active locale"""
    return self._raw[self._locale]

  def _flatten(self, input_object: dict):
    result = {}

    for key in input_object:
      value = input_object[key]

      if isinstance(value, dict):
        self._flatten_deep(value, key, result)
      else:
        result[key] = value

        if isinstance(value, list):
          self._flatten_deep(dict(zip(list(range(len(value))), value)), key, result)

    return result

  def _flatten_deep(self, input_object: dict, base_key: str, result: dict):
    for key in input_object:
      prop = f'{base_key}.{key}' if base_key else key
      value = input_object[key]

      if isinstance(value, (dict, list)):
        self._flatten_deep(value, prop, result)
      else:
        result[prop] = value

    return result

  def _get_message_variant(self, message: str, **params):
    count = params.get('count', 0)
    message = message.split('|')

    if len(message) == 2:
      message = [message[0]] + message

    if count == 0:
      return message[0]

    return message[1] if count == 1 else message[2]

  def _translate(self, path: str, translations: dict, **params):
    if path in translations:
      message = translations[path]
      response = self._get_message_variant(message, **params).strip() if '|' in message else message

      for param, value in params.items():
        response = response.replace("{" + str(param) + "}", str(value))

      return response

    return None

  def tr(self, path: str, **params):
    """Get the translate text for the given dot path"""

    response = self._translate(path, self._translations[self._locale], **params)

    if response is None:
      response = self._translate(path, self._translations[self._fallback_locale], **params)
    else:
      return response

    if response is None:
      if self._show_warning:
        print(f"Translation missing for {path}")

      return path

    return response
