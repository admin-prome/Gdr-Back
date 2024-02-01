import datetime

class TextAreaField:
  """
  Representa un campo de tipo textarea.

  Args:
    key: La clave del campo.
    label: El label del campo.
    name: El nombre del campo.
    placeholder: El placeholder del campo.
    required: Indica si el campo es obligatorio.
    value: El valor del campo.
    validators: Los validadores del campo.
    return: El tipo de retorno del campo.
  """

  def __init__(
      self,
      key,
      label,
      name,
      placeholder,
      required,
      value,
      validators,
      return_type):
    self.key = key
    self.label = label
    self.name = name
    self.placeholder = placeholder
    self.required = required
    self.value = value
    self.validators = validators
    self.return_type = return_type

  def __repr__(self):
    return f"TextAreaField(key={self.key}, label={self.label}, name={self.name}, placeholder={self.placeholder}, required={self.required}, value={self.value}, validators={self.validators}, return_type={self.return_type})"

  def validate(self, value):
    for validator in self.validators:
      validator(value)

  def to_dict(self):
    return {
      "key": self.key,
      "label": self.label,
      "name": self.name,
      "placeholder": self.placeholder,
      "required": self.required,
      "value": self.value,
      "validators": self.validators,
      "return_type": self.return_type,
    }

class DatePickerField:
  """
  Representa un campo de tipo datepicker.

  Args:
    key: La clave del campo.
    label: El label del campo.
    name: El nombre del campo.
    placeholder: El placeholder del campo.
    required: Indica si el campo es obligatorio.
    value: El valor del campo.
    validators: Los validadores del campo.
    return: El tipo de retorno del campo.
  """

  def __init__(
      self,
      key,
      label,
      name,
      placeholder,
      required,
      value,
      validators,
      return_type):
    self.key = key
    self.label = label
    self.name = name
    self.placeholder = placeholder
    self.required = required
    self.value = value
    self.validators = validators
    self.return_type = return_type

  def __repr__(self):
    return f"DatePickerField(key={self.key}, label={self.label}, name={self.name}, placeholder={self.placeholder}, required={self.required}, value={self.value}, validators={self.validators}, return_type={self.return_type})"

  def validate(self, value):
    if not value:
      if self.required:
        raise ValueError(f"El campo {self.label} es obligatorio.")
    else:
      try:
        date = datetime.datetime.strptime(value, "%Y-%m-%d")
      except ValueError:
        raise ValueError(f"El valor del campo {self.label} no es una fecha válida.")

  def to_dict(self):
    return {
      "key": self.key,
      "label": self.label,
      "name": self.name,
      "placeholder": self.placeholder,
      "required": self.required,
      "value": self.value,
      "validators": self.validators,
      "return_type": self.return_type,
    }

class SelectField:
  """
  Representa un campo de tipo select.

  Args:
    key: La clave del campo.
    label: El label del campo.
    name: El nombre del campo.
    placeholder: El placeholder del campo.
    options: Las opciones del campo.
    required: Indica si el campo es obligatorio.
    value: El valor del campo.
    validators: Los validadores del campo.
    condition: La condición que determina si el campo está habilitado o no.
    dependentOn: El campo del que depende este campo.
    dependencies: Las dependencias de este campo.
    dependents: Los campos que dependen de este campo.
    return: El tipo de retorno del campo.
  """

  def __init__(
      self,
      key,
      label,
      name,
      placeholder,
      options,
      required=False,
      value="",
      validators=None,
      condition="true",
      dependentOn=None,
      dependencies=None,
      dependents=None,
      return_type="string"
  ):
    self.key = key
    self.label = label
    self.name = name
    self.placeholder = placeholder
    self.options = options
    self.required = required
    self.value = value
    self.validators = validators or []
    self.condition = condition
    self.dependentOn = dependentOn
    self.dependencies = dependencies or []
    self.dependents = dependents or []
    self.return_type = return_type

  def __repr__(self):
    return f"SelectField(key={self.key}, label={self.label}, name={self.name}, placeholder={self.placeholder}, options={self.options}, required={self.required}, value={self.value}, validators={self.validators}, condition={self.condition}, dependentOn={self.dependentOn}, dependencies={self.dependencies}, dependents={self.dependents}, return_type={self.return_type})"

  def validate(self, value):
    for validator in self.validators:
      validator(value)

  def to_dict(self):
    return {
      "key": self.key,
      "label": self.label,
      "name": self.name,
      "placeholder": self.placeholder,
      "options": self.options,
      "required": self.required,
      "value": self.value,
      "validators": self.validators,
      "condition": self.condition,
      "dependentOn": self.dependentOn,
      "dependencies": self.dependencies,
      "dependents": self.dependents,
      "return_type": self.return_type,
    }

  def get_option_value(self, option):
    if isinstance(option, dict):
      return option["value"]
    elif isinstance(option, str):
      return option
    else:
      raise ValueError(f"La opción {option} no es válida.")

  def get_selected_option(self):
    if self.value is None:
      return None
    else:
      return self.get_option_value(self.value)

  def get_selected_option_label(self):
    option = self.get_selected_option()
    if option is not None:
      return self.options[option]["label"]
    else:
      return None

  def is_enabled(self, form_data):
    if self.condition != "true":
      condition_value = self.evaluate_condition(form_data)
      return condition_value
    else:
      return True

  def evaluate_condition(self, form_data):
    if self.dependentOn is None:
        return True
    else:
        dependent_value = form_data.get(self.dependentOn)
        if dependent_value is None:
            return False
        else:
            dependent_options = self.options
            if isinstance(dependent_value, str):
                dependent_value = dependent_options.get(dependent_value)
            if dependent_value is None:
                return False
            else:
                return dependent_value  # Corregido para devolver el valor de dependencia


class InputField:
  """
  Representa un campo de tipo input.

  Args:
    key: La clave del campo.
    label: El label del campo.
    name: El nombre del campo.
    placeholder: El placeholder del campo.
    required: Indica si el campo es obligatorio.
    value: El valor del campo.
    validators: Los validadores del campo.
    return_type: El tipo de retorno del campo.
  """

  def __init__(
      self,
      key,
      label,
      name,
      placeholder,
      required=False,
      value="",
      validators=None,
      return_type="string"
  ):
    self.key = key
    self.label = label
    self.name = name
    self.placeholder = placeholder
    self.required = required
    self.value = value
    self.validators = validators or []
    self.return_type = return_type

  def __repr__(self):
    return f"InputField(key={self.key}, label={self.label}, name={self.name}, placeholder={self.placeholder}, required={self.required}, value={self.value}, validators={self.validators}, return_type={self.return_type})"

  def validate(self, value):
    for validator in self.validators:
      validator(value)

  def to_dict(self):
    return {
      "key": self.key,
      "label": self.label,
      "name": self.name,
      "placeholder": self.placeholder,
      "required": self.required,
      "value": self.value,
      "validators": self.validators,
      "return_type": self.return_type,
    }

  def is_enabled(self, form_data):
    return True

class RadioButtonField:
    """
    Representa un campo de tipo radio.

    Args:
        key: La clave del campo.
        label: El label del campo.
        name: El nombre del campo.
        options: Las opciones del campo.
        value: El valor seleccionado.
        validators: Los validadores del campo.
        return_type: El tipo de retorno del campo.
    """

    def __init__(
        self,
        key,
        label,
        name,
        options,
        value="",
        validators=None,
        return_type="string"
    ):
        self.type = "radio"
        self.key = key
        self.label = label
        self.name = name
        self.options = options
        self.value = value
        self.validators = validators or []
        self.return_type = return_type

    def __repr__(self):
        return f"RadioButtonField(type={self.type}, key={self.key}, label={self.label}, name={self.name}, options={self.options}, value={self.value}, validators={self.validators}, return_type={self.return_type})"

    def validate(self):
        for validator in self.validators:
            validator(self.value)

    def to_dict(self):
        return {
            "type": self.type,
            "key": self.key,
            "label": self.label,
            "name": self.name,
            "options": self.options,
            "value": self.value,
            "validators": self.validators,
            "return_type": self.return_type,
        }

    def is_enabled(self, form_data):
        return True  # Puedes implementar la lógica de habilitación según tus necesidades

class FileField:
    """
    Representa un campo de tipo archivo.

    Args:
        key: La clave del campo.
        label: El label del campo.
        name: El nombre del campo.
        placeholder: El placeholder del campo.
        required: Indica si el campo es obligatorio.
        value: El valor del campo.
        validators: Los validadores del campo.
        accept: Los tipos de archivo permitidos.
        max_file_size: El tamaño máximo del archivo en MB.
    """

    def __init__(
        self,
        key,
        label,
        name,
        placeholder,
        required=False,
        value="",
        validators=None,
        accept="",
        max_file_size=None
    ):
        self.type = "file"
        self.key = key
        self.label = label
        self.name = name
        self.placeholder = placeholder
        self.required = required
        self.value = value
        self.validators = validators or {}
        self.accept = accept
        self.max_file_size = max_file_size

    def __repr__(self):
        return f"FileField(type={self.type}, key={self.key}, label={self.label}, name={self.name}, placeholder={self.placeholder}, required={self.required}, value={self.value}, validators={self.validators}, accept={self.accept}, max_file_size={self.max_file_size})"

    def validate(self, file):
        if self.required:
            if not file:
                raise ValueError("El archivo es obligatorio.")
        if self.max_file_size is not None:
            file_size_in_mb = len(file) / (1024 * 1024)
            if file_size_in_mb > self.max_file_size:
                raise ValueError("El tamaño del archivo excede el límite permitido.")

    def to_dict(self):
        return {
            "type": self.type,
            "key": self.key,
            "label": self.label,
            "name": self.name,
            "placeholder": self.placeholder,
            "required": self.required,
            "value": self.value,
            "validators": self.validators,
            "accept": self.accept,
            "maxFileSize": self.max_file_size,
        }
        
class Formulario:
    def __init__(self, form_data):
        self.fields = {}
        for key, field_data in form_data.items():
            field_type = field_data["type"]
            if field_type == "file":
                self.fields[key] = FileField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    placeholder=field_data["placeholder"],
                    required=field_data.get("required") == "true",
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    accept=field_data.get("accept", ""),
                    max_file_size=field_data.get("maxFileSize")
                )
            elif field_type == "input":
                self.fields[key] = InputField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    placeholder=field_data["placeholder"],
                    required=field_data.get("required") == "true",
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    return_type=field_data.get("return", "string")
                )
            elif field_type == "radio":
                self.fields[key] = RadioButtonField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    options=field_data["options"],
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    return_type=field_data.get("return", "string")
                )
            elif field_type == "select":
                self.fields[key] = SelectField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    placeholder=field_data["placeholder"],
                    options=field_data["options"],
                    required=field_data.get("required") == "true",
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    condition=field_data.get("condition", "true"),
                    dependentOn=field_data.get("dependentOn", "false"),
                    dependencies=field_data.get("dependencies", {}),
                    dependents=field_data.get("dependents", []),
                    return_type=field_data.get("return", "string")
                )
            elif field_type == "datepicker":
                self.fields[key] = DatePickerField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    placeholder=field_data["placeholder"],
                    required=field_data.get("required") == "true",
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    return_type=field_data.get("return", "string")
                )
            elif field_type == "textarea":
                self.fields[key] = TextAreaField(
                    key=field_data["key"],
                    label=field_data["label"],
                    name=field_data["name"],
                    placeholder=field_data["placeholder"],
                    required=field_data.get("required") == "true",
                    value=field_data["value"],
                    validators=field_data.get("validators", {}),
                    return_type=field_data.get("return", "string")
                )
            else:
                raise ValueError(f"Tipo de campo desconocido: {field_type}")

    def to_dict(self):
        # Devuelve un diccionario que representa el formulario completo
        form_data = {}
        for key, field in self.fields.items():
            form_data[key] = field.to_dict()
        return form_data

    def __str__(self):
        return f"Formulario(fields={self.fields})"

    def __repr__(self):
        return self.__str__()

        
        