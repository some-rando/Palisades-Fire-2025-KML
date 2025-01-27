# Before running the script, create a virtual environment via the terminal:
    # python3 -m venv .
    # source ./bin/activate

import json
import xml.etree.ElementTree as ET
from datetime import datetime

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
    "mobile_home": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/mobile-home.png",
        "types": [
            "Mobile Home Double Wide",
            "Mobile Home Single Wide",
            "Mobile Home Triple Wide"
        ],
        "scale": 0.6
    },
    "single_family_single": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/single-family-single.png",
        "types": ["Single Family Residence Single Story"],
        "scale": 0.6
    },
    "single_family_multi": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/single-family-multi.png",
        "types": ["Single Family Residence Multi Story"],
        "scale": 0.6
    },
    "multi_family_single": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/multi-family-single.png",
        "types": ["Multi Family Residence Single Story"],
        "scale": 0.6
    },
    "multi_family_multi": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/multi-family-multi.png",
        "types": ["Multi Family Residence Multi Story"],
        "scale": 0.6
    },
    "commercial_single": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/commercial-building.png",
        "types": ["Commercial Building Single Story"],
        "scale": 0.6
    },
    "commercial_multi": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/commercial-building-multi.png",
        "types": ["Commercial Building Multi Story"],
        "scale": 0.6
    },
    "mixed": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/mixed-use.png",
        "types": ["Mixed Commercial/Residential"],
        "scale": 0.6
    },
    "church": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/church.png",
        "types": ["Church"],
        "scale": 0.6
    },
    "school": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/school.png",
        "types": ["School"],
        "scale": 0.6
    },
    "infrastructure": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/infrastructure.png",
        "types": ["Infrastructure"],
        "scale": 0.6
    },
    "utility": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/utility.png",
        "types": ["Utility Misc Structure"],
        "scale": 0.6
    },
    "motor_home": {
        "icon": "https://raw.githubusercontent.com/some-rando/Palisades-Fire-2025-KML/main/icons/motor-home.png",
        "types": ["Motor Home"],
        "scale": 0.6
    }
}

def create_kml_from_geojson(input_file, output_file):
    # Create KML root element
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, 'Document')
    doc.append(ET.Comment(f'Generated on {datetime.now().isoformat()}'))
    
    # Create mapping of structure types to their icon group
    structure_to_group = {}
    for group_name, group_info in ICON_GROUPS.items():
        for structure_type in group_info["types"]:
            structure_to_group[structure_type] = group_name
    
    # Define styles for each damage type and structure combination
    for group_name, group_info in ICON_GROUPS.items():
        for damage_type, damage_color in DAMAGE_COLORS.items():
            style = ET.SubElement(doc, 'Style', 
                                id=f"{group_name}_{damage_type.replace(' ', '_').replace('(', '').replace(')', '').replace('%', '').replace('-', '')}")
            icon_style = ET.SubElement(style, 'IconStyle')
            ET.SubElement(icon_style, 'color').text = damage_color
            ET.SubElement(icon_style, 'scale').text = str(group_info["scale"])
            icon = ET.SubElement(icon_style, 'Icon')
            ET.SubElement(icon, 'href').text = group_info["icon"]
    
    # Create structure type folders
    folders = {}
    for struct_type in structure_to_group.keys():
        folder = ET.SubElement(doc, 'Folder')
        ET.SubElement(folder, 'name').text = struct_type
        damage_folders = {}
        for damage_type in DAMAGE_COLORS.keys():
            damage_folder = ET.SubElement(folder, 'Folder')
            ET.SubElement(damage_folder, 'name').text = damage_type
            damage_folders[damage_type] = damage_folder
        folders[struct_type] = damage_folders
    
    # Read and process GeoJSON
    with open(input_file, 'r') as f:
        geojson_data = json.load(f)
    
    # Process features
    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        
        structure_type = properties['STRUCTURETYPE']
        damage = properties['DAMAGE']
        coordinates = geometry['coordinates']
        
        if structure_type in folders:
            # Create placemark
            placemark = ET.SubElement(folders[structure_type][damage], 'Placemark')
            
            # Style reference
            group_name = structure_to_group[structure_type]
            style_id = f"{group_name}_{damage.replace(' ', '_').replace('(', '').replace(')', '').replace('%', '').replace('-', '')}"
            ET.SubElement(placemark, 'styleUrl').text = f"#{style_id}"
            
            # Description
            ET.SubElement(placemark, 'description').text = f"{structure_type}\n{damage}"
            
            # Point coordinates
            point = ET.SubElement(placemark, 'Point')
            ET.SubElement(point, 'coordinates').text = f"{coordinates[0]},{coordinates[1]}"
    
    # Write KML file
    tree = ET.ElementTree(kml)
    ET.indent(tree, space="  ")
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

if __name__ == "__main__":
    input_file = "DINS_2025_Palisades_Public_View.geojson"
    output_file = "damage_assessments.kml"
    create_kml_from_geojson(input_file, output_file) 