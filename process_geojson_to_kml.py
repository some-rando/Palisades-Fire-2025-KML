# Create a virtual environment
    # python3 -m venv .
    # source ./bin/activate
    # python3 -m pip install xyz

import simplekml
import json

# Define color mapping (KML uses aabbggrr format)
DAMAGE_COLORS = {
    "No Damage": "ff00ff00",             # Green
    "Affected (1-9%)": "ff00ffff",       # Yellow
    "Minor (10-25%)": "ff00b5ff",        # Yellow-Orange
    "Major (26-50%)": "ff0051ff",        # Orange
    "Destroyed (>50%)": "ff0000ff",      # Red
}

# Group structures by their icon type and scale
ICON_GROUPS = {
    "residential": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png",
        "types": [
            "Mobile Home Double Wide",
            "Mobile Home Single Wide",
            "Mobile Home Triple Wide",
            "Single Family Residence Multi Story",
            "Single Family Residence Single Story"
        ],
        "scale": 0.6
    },
    "residential_multi": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png",
        "types": [
            "Multi Family Residence Multi Story",
            "Multi Family Residence Single Story"
        ],
        "scale": 0.7
    },
    "commercial": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/buildings.png",
        "types": [
            "Commercial Building Single Story",
            "Mixed Commercial/Residential"
        ],
        "scale": 0.6
    },
    "commercial_multi": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/buildings.png",
        "types": [
            "Commercial Building Multi Story"
        ],
        "scale": 0.7
    },
    "church": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/church.png",
        "types": ["Church"],
        "scale": 0.6
    },
    "school": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/schools.png",
        "types": ["School"],
        "scale": 0.6
    },
    "infrastructure": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/triangle.png",
        "types": ["Infrastructure"],
        "scale": 0.6
    },
    "utility": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/square.png",
        "types": ["Utility Misc Structure"],
        "scale": 0.6
    },
    "vehicle": {
        "icon": "http://maps.google.com/mapfiles/kml/shapes/truck.png",
        "types": ["Motor Home"],
        "scale": 0.6
    }
}

def create_kml_from_geojson(input_file, output_file):
    # Create KML object
    kml = simplekml.Kml()
    doc = kml.newdocument(name="Damage Assessments")
    
    # Create mapping of structure types to their icon group
    structure_to_group = {}
    for group_name, group_info in ICON_GROUPS.items():
        for structure_type in group_info["types"]:
            structure_to_group[structure_type] = group_name
    
    # Create folders for each structure type and damage level
    folders = {}
    for struct_type in structure_to_group.keys():
        type_folder = doc.newfolder(name=struct_type)
        folders[struct_type] = {}
        for damage_type in DAMAGE_COLORS.keys():
            damage_folder = type_folder.newfolder(name=damage_type)
            folders[struct_type][damage_type] = damage_folder
    
    # Create shared styles for each icon group and damage combination
    shared_styles = {}
    for group_name, group_info in ICON_GROUPS.items():
        for damage_type, damage_color in DAMAGE_COLORS.items():
            style = simplekml.Style()
            style.iconstyle.icon.href = group_info["icon"]
            style.iconstyle.color = damage_color
            style.iconstyle.scale = group_info["scale"]
            doc.styles.append(style)
            shared_styles[(group_name, damage_type)] = style
    
    # Read GeoJSON file
    with open(input_file, 'r') as f:
        geojson_data = json.load(f)
    
    # Process each feature
    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        
        structure_type = properties['STRUCTURETYPE']
        damage = properties['DAMAGE']
        coordinates = geometry['coordinates']
        
        # Create placemark in appropriate subfolder
        if structure_type in folders:
            pnt = folders[structure_type][damage].newpoint(
                coords=[(coordinates[0], coordinates[1])]
            )
            
            # Remove name to avoid labels
            pnt.name = ""
            
            # Use shared style based on icon group
            group_name = structure_to_group[structure_type]
            pnt.style = shared_styles[(group_name, damage)]
            
            # Simplified description
            pnt.description = f"""{structure_type}
{damage}"""
    
    # Save the KML file
    kml.save(output_file)

if __name__ == "__main__":
    input_file = "DINS_2025_Palisades_Public_View.geojson"
    output_file = "damage_assessments.kml"
    create_kml_from_geojson(input_file, output_file) 