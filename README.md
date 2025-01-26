# GeoJSON to KML Damage Assessment Converter

This script converts CAL FIRE's Damage Inspection (DINS) data for the 2025 Palisades Fire from GeoJSON format to a color-coded KML file for visualization in Google Earth or Google Earth Pro. This script changes the visual style of the original data from CAL FIRE by grouping the structures by type and damage level, using different icons for different structure types, and color coding the icons to indicate the amount of damage.

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
  - Church
  - Commercial Building Multi Story
  - Commercial Building Single Story
  - Infrastructure
  - Mixed Commercial/Residential
  - Mobile Home Double Wide
  - Mobile Home Single Wide
  - Mobile Home Triple Wide
  - Motor Home
  - Multi Family Residence Multi Story
  - Multi Family Residence Single Story
  - School
  - Single Family Residence Multi Story
  - Single Family Residence Single Story
  - Utility Misc Structure

- Multi-family buildings are displayed slightly larger for better visibility
- Google Earth Pro is limited in its built-in icon options, so this script has to use rather basic icons for each structure type and there are duplicates for several structure types. Clicking on each icon will show text for the structure type and damage level.


## Using the KML file directly in Google Earth Pro

To access the KML file directly in Google Earth Pro without having to run this script or download anything, you can use a network link:

1. In Google Earth Pro, select "Add" → "Network Link"
2. Set the Link to: `https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/damage_assessments.kml`
3. Set "Refresh" settings as desired (e.g., periodically or when view changes). More frequently than every 4 hours won't be useful because the data is only updated every 4 hours.

The KML file is automatically updated at 6am, 10am, 2pm, and 6pm through GitHub Actions, pulling the latest data from CAL FIRE's public dataset.


## Using the script to generate a KML file

1. Install requirements:
```bash
python -m pip install -r requirements.txt
```

2. Run the script:
```bash
python process_geojson_to_kml.py
```

## License

This project uses data from CAL FIRE which is licensed under Creative Commons Attribution [Open Data](https://data.ca.gov/dataset/dins-2025-palisades-public-view).