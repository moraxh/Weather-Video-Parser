import os
import torch
import whisper
from enum import Enum

# It only allows subfolders with video or audio files
DATA_FOLDER = "./data" 
DATA_SUBFOLDERS = os.listdir(DATA_FOLDER)

PREFERRED_LANGUAGE = "es"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("small", device=DEVICE)

class Stage(Enum):
  START     = ["buenos", "dias", "amigos", "presento", "nuevamente"]
  MONDAY    = ["Lunes"]
  TUESDAY   = ["Martes"]
  WEDNESDAY = ["Miércoles"]
  THURSDAY  = ["Jueves"]
  FRIDAY    = ["Viernes"]
  SATURDAY  = ["Sabado"]
  SUNDAY    = ["Domingo"]
  END       = ["despido", "ustedes", "redes", "sociales"]

class StageFilesNames(Enum):
  START     = "00_entrada"
  MONDAY    = "01_lunes"
  TUESDAY   = "02_martes"
  WEDNESDAY = "03_miercoles"
  THURSDAY  = "04_jueves"
  FRIDAY    = "05_viernes"
  SATURDAY  = "06_sabado"
  SUNDAY    = "07_domingo"
  END       = "08_salida"

class Presets(Enum):
  EL_SALMANTINO = ["Salmantino"],
  EL_PAKAL = ["Pakal", "Chiapas", "Tuxtla", "Gutiérrez", "San", "Cristóbal", "Casas", "Tapachula"],

class Cities(Enum):
  SALAMANCA = "Salamanca"
  TUXTLA = "Tuxtla"
  SAN_CRISTOBAL = "San Cristóbal de las Casas"
  TAPACHULA = "Tapachula"

class PresetCities(Enum):
  EL_SALMANTINO = [Cities.SALAMANCA]
  EL_PAKAL = [Cities.TUXTLA, Cities.SAN_CRISTOBAL, Cities.TAPACHULA]

class Forecast(Enum):
  DOWNPOUR = ["chubasco", "aguacero", "chaparrón", "torrencial"]
  ELECTRICAL_STORM = ["tormenta", "eléctrica", "tormenta", "relámpagos", "trueno"]
  RAINY = ["lluvia", "lluvioso", "llovizna", "precipitación", "aguacero", "leve"]
  CLOUDY = ["nublado", "cubierto", "gris", "encapotado"]
  PARTIAL_CLOUDINESS = ["parcialmente nublado", "algo nublado", "nubes dispersas"]
  SUNNY = ["soleado", "sol", "despejado", "cielo despejado", "día claro"]
  PARTIAL_SUNNY = ["parcialmente soleado", "parcialmente soleado", "sol con nubes", "intermitentemente soleado"]
  HIGH_SUNNY = ["muy soleado", "muy soleado", "intenso sol", "sol fuerte", "día muy claro"]
  STORMY = ["tormenta", "tormentas", "tormentoso", "tormentosos", "tempestad", "tormenta fuerte"]
  WINDY = ["viento", "ventoso", "vientos", "viento fuerte", "ráfagas", "brisa fuerte"]