import re
import unicodedata
from Levenshtein import distance as lev
from utils.constants import Stage, Presets, PresetCities, Forecast

class WeatherFolderExtractor:
  def __init__(self):
    self.available_stages = [stage.name for stage in Stage]

    self.normalized_stage_phrases = {
      stage: [self.normalize_text(p) for p in Stage[stage].value]
      for stage in self.available_stages
    }

  @staticmethod
  def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = ''.join(c for c in text if c.isalnum() or c.isspace() or c == "%")
    return text.strip()

  @staticmethod
  def split_keep_look(text, sep):
    return re.split(rf'(?<={re.escape(sep)})', text)

  def get_preset(self, text):
    words = self.normalize_text(text).split()[:10]
    best_match = {'preset': None, 'score': float('inf')}

    for preset in Presets:
      for phrase in preset.value[0]:
        phrase = self.normalize_text(phrase)
        scores = [lev(phrase, word) for word in words]
        best_score = min(scores)
        if best_score < best_match['score']:
          best_match = {'preset': preset, 'score': best_score}

    preset = best_match['preset']

    return preset.name

  def get_stage(self, text):
    words = self.normalize_text(text).split()[:10]
    best_match = {'stage': None, 'score': float('inf')}

    for stage, phrases in self.normalized_stage_phrases.items():
      for phrase in phrases:
        scores = [lev(phrase, word) for word in words]
        best_score = min(scores)
        if best_score < best_match['score']:
          best_match = {'stage': stage, 'score': best_score}

    stage = best_match['stage']

    if stage in self.available_stages:
      self.available_stages.remove(stage)
      del self.normalized_stage_phrases[stage]

    return stage
  
  def get_city_index(self, text, city):
    words = self.normalize_text(text).split()

    scores = [lev(self.normalize_text(city), word) for word in words]
    print(scores)

  def separate_text_by_city(self, text, preset):
    if len(PresetCities[preset].value) == 0:
      return text

    # Check if the word "probabilidad de lluvia" appears n times in the text
    word_target_count = len(PresetCities[preset].value)

    if word_target_count == text.count("probabilidad de lluvia"):
      splitted_text = self.split_keep_look(text, "probabilidad de lluvia")
      return [s.strip() for s in splitted_text if s.strip()]

    # Separate by "%"
    if "%" in text:
      splitted_text = self.split_keep_look(text, "%")
      return [s.strip() for s in splitted_text if s.strip()]
  
  def extract_weather(self, text):
    # Remove "probabilidad de lluvia" from the text
    text = text.replace("probabilidad de lluvia", "").strip()

    best_match = {'forecast': None, 'score': float('inf')}
    words = self.normalize_text(text).split()

    for forecast, phrases in Forecast.__members__.items():
      for phrase in phrases.value:
        p_len = len(phrase.split())
        for i in range(len(words) - p_len + 1):
          segment = " ".join(words[i : i + p_len])
          score = lev(phrase, segment)
          if score < best_match['score']:
            best_match = {'forecast': forecast, 'score': score}

    forecast = best_match['forecast']
    return forecast.lower()

  def extract_forecasts(self, text):
    # Forecast order per city
    # - Max
    # - Weather
    # - Min
    # - Probability

    forecast = {
      "max": 0,
      "weather": "",
      "min": 0,
      "probability": 0,
    }

    # Check if the word "grados" appears 2 times in the text
    if text.count("grados") == 2:
      matches = re.findall(r"(\d+(?:\.\d+)?)(?:\s*(?:°|grados?))", text)

      if len(matches) < 2:
        print(f"Not enough temperature values found in text: {text}")
        return forecast

      forecast["max"] = int(matches[0])
      forecast["min"] = int(matches[1])
    else:
      nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)

      if len(nums) < 2:
        print(f"Not enough numbers found in text: {text}")
        return forecast
      
      forecast["max"] = int(nums[0])
      forecast["min"] = int(nums[-1])

    # Extract probability of rain
    # Extract using "<n>%"
    if "%" in text:
      matches = re.findall(r"(\d+(?:\.\d+)?)(?:\s*%)", text)
      if len(matches) > 0:
        forecast["probability"] = int(matches[0])
    elif "por ciento" in text:
      matches = re.findall(r"(\d+(?:\.\d+)?)(?:\s*por ciento)", text)
      if len(matches) > 0:
        forecast["probability"] = int(matches[0])
    else: 
      # Get the middle number in the text
      nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)

      if len(nums) < 3:
        print(f"Not enough numbers found in text: {text}")
        return forecast

      forecast["probability"] = int(nums[1])

    weather = self.extract_weather(text)
    forecast["weather"] = weather
    return forecast

  def process_transcriptions(self, transcriptions):
    # Get stages
    for transcription in transcriptions:
      transcription["stage"] = self.get_stage(transcription["text"])
    
    start_transcription = [t for t in transcriptions if t["stage"] == Stage.START.name][0]
    preset = self.get_preset(start_transcription["text"])

    forecast_data = []

    for transcription in transcriptions:
      if transcription["stage"] == Stage.END.name or transcription["stage"] == Stage.START.name:
        continue

      separated_text = self.separate_text_by_city(transcription["text"], preset)

      if len(separated_text) != len(PresetCities[preset].value):
        print(f"Warning: Expected {len(PresetCities[preset].value)} cities, but got {len(separated_text)} in text: {transcription['text']}")
        continue

      forecast = {
        "stage": transcription["stage"].lower(),
        "cities_forecasts": []
      }

      for i, text in enumerate(separated_text):
        forecast["cities_forecasts"].append({
          "city": PresetCities[preset].value[i].name.lower(),
          "forecast": self.extract_forecasts(text)
        })

      forecast_data.append(forecast)

    return {
      "forecast_data": forecast_data,
      "transcriptions": transcriptions,
      "preset": preset
    }