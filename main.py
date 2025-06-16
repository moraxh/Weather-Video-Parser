import os
import json
import shutil
from tqdm import tqdm
from utils.weather import WeatherFolderExtractor
from utils.constants import model, DATA_SUBFOLDERS, DATA_FOLDER, PREFERRED_LANGUAGE, StageFilesNames

def process_weather_data():
  for subfolder in tqdm(DATA_SUBFOLDERS, desc="Processing subfolders", unit="folder"):
    subfolder_path = os.path.join(DATA_FOLDER, subfolder)

    if not os.path.isdir(subfolder_path):
        continue

    files = os.listdir(subfolder_path)

    if not files:
      continue

    extractor = WeatherFolderExtractor()

    folder_transcription = []

    i = 0

    for file in tqdm(files, desc=f"Processing files in {subfolder}", unit="file"):
      i += 1
      file_path = os.path.join(subfolder_path, file)
      if not os.path.isfile(file_path):
        continue
      
      if not file.lower().endswith(('.mp4')):
        print(f"Skipping unsupported file: {file_path}")
        continue

      print(f"Processing file: {file_path}")
      result = model.transcribe(file_path, language=PREFERRED_LANGUAGE)

      if 'text' not in result:
        print(f"No transcription text found in file: {file_path}")
        continue

      text = WeatherFolderExtractor.normalize_text(result['text'])

      data = {
        "file": file,
        "text": text,
      }

      folder_transcription.append(data)

    if len(folder_transcription) != 9:
      raise ValueError(f"Expected 9 mp4 files in {subfolder}, found {len(folder_transcription)}")

    data = extractor.process_transcriptions(folder_transcription)

    if not data:
      print(f"No valid data processed for {subfolder}")
      continue

    output_file = os.path.join(subfolder_path, "forecast.json")
    with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=2)

    # Create another dir with the names changed to the day
    days_folder = os.path.join(subfolder_path, "days")
    os.makedirs(days_folder, exist_ok=True)

    for transcription in data["transcriptions"]:
      stage_file_name = StageFilesNames[transcription["stage"]].value

      input_file = os.path.join(subfolder_path, transcription["file"])
      output_file = os.path.join(days_folder, f"{stage_file_name}.{transcription['file'].split('.')[-1]}")

      # Copy the file with the new name
      shutil.copy(input_file, output_file)

if __name__ == "__main__":
  process_weather_data()