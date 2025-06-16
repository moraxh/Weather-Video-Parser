# Weather Video Parser

Automated system for processing Spanish weather forecast videos and extracting structured climate data.

## Description

Weather Video Parser transforms weekly weather broadcast videos into structured JSON data. It processes a set of 9 MP4 video files representing the full weekly forecast (from introduction to conclusion), and extracts key weather information such as temperature ranges, weather conditions, and precipitation probabilities for multiple cities.

## Features

* **Automatic transcription**: Uses OpenAI Whisper to transcribe Spanish audio
* **Segment detection**: Identifies each day’s segment using fuzzy matching
* **Weather data extraction**: Extracts weather data for multiple cities per day
* **Regional presets**: Supports configurable city and keyword sets for different regions
* **Structured output**: Produces clean JSON files and copies/renames videos for easier reference

## Input Requirements

The system expects folders containing exactly **9 MP4 video files**, corresponding to the full weekly broadcast:

* One introduction
* Seven daily forecasts (Monday to Sunday)
* One conclusion

The filenames can be arbitrary, but the presence of 9 video files is required. During processing, the system will copy and rename these files to a standardized format in the output.

## Output Structure

### `forecast.json`

A JSON file containing the extracted forecast and transcription data, organized by day and city.

Example:

```json
{
  "forecast_data": [...],
  "transcriptions": [...],
  "preset": "EL_SALMANTINO"
}
```

### `days/` Folder

A folder where the 9 original videos are copied and renamed using the following format:

* `00_entrada.mp4` (Introduction)
* `01_lunes.mp4` to `07_domingo.mp4` (Monday to Sunday)
* `08_salida.mp4` (Conclusion)

## Regional Configuration

The system supports region-specific processing using presets that define cities and keyword patterns.

### Preset: `EL_SALMANTINO`

* **Cities**: Salamanca
* **Keywords**: "Salmantino"

### Preset: `EL_PAKAL`

* **Cities**: Tuxtla, San Cristóbal de las Casas, Tapachula
* **Keywords**: "Pakal", "Chiapas", "Tuxtla", "Gutiérrez"

## Weather Conditions Supported

The system can detect 10 distinct weather condition types, such as sunny, cloudy, rainy, etc.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place a folder with 9 MP4 files in the `./data` directory
2. Run the main processor:

```bash
python main.py
```

## How It Works

The `WeatherFolderExtractor` class performs the following:

1. **Text normalization**: Cleans and prepares the transcription text
2. **Stage detection**: Matches segments to days of the week using fuzzy logic
3. **Forecast extraction**: Uses regular expressions to identify temperatures, conditions, and rain probabilities
4. **City separation**: Detects city-level data using keywords and contextual cues

## Requirements

* Python 3.7 or higher (tested with Python 3.10)
* CUDA-enabled GPU (optional, for Whisper acceleration)
* OpenAI Whisper
* All Python dependencies listed in `requirements.txt`

## Notes

This tool is optimized for structured, Spanish-language weekly weather broadcasts. Its accuracy depends on audio clarity and consistency in the broadcast format. It uses fuzzy matching to mitigate transcription variations and typical audio imperfections in regional news videos.