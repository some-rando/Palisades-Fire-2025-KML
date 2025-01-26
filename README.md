# GeoJSON to KML Damage Assessment Converter

This script converts CAL FIRE's Damage Inspection (DINS) data for the 2025 Palisades Fire from GeoJSON format to a color-coded KML file for visualization in Google Earth.

## Data Source

The source GeoJSON data comes from [CAL FIRE's public dataset](https://data.ca.gov/dataset/dins-2025-palisades-public-view) which provides damage inspection information for structures affected by the Palisades Fire.

## Features

- Converts structure damage data to color-coded placemarks:
  - No Damage: Green
  - Affected (1-9%): Yellow
  - Minor (10-25%): Yellow-Orange
  - Major (26-50%): Orange
  - Destroyed (>50%): Red

- Organizes structures by type and damage level in nested folders
- Uses different icons for structure types:
  - Residential buildings (houses)
  - Commercial buildings
  - Churches
  - Schools
  - Infrastructure
  - Utility structures
  - Motor homes

- Multi-story buildings are displayed slightly larger for better visibility

## Usage

1. Install requirements:
```bash
python -m pip install -r requirements.txt
```

2. Run the script:
```bash
python process_geojson_to_kml.py
```

## Network Link Access

To access the KML file directly in Google Earth Pro using a network link:

1. In Google Earth Pro, select "Add" → "Network Link"
2. Set the Link to: `https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/damage_assessments.kml`
3. Set "Refresh" settings as desired (e.g., periodically or when view changes)

The KML file is automatically updated at 6am, 10am, 2pm, and 6pm through GitHub Actions, pulling the latest data from CAL FIRE's public dataset.

## License

This project uses data from CAL FIRE which is licensed under Creative Commons Attribution [Open Data](https://data.ca.gov/dataset/dins-2025-palisades-public-view).