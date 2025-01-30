import xml.etree.ElementTree as ET
import yaml

xml_file_path = "buildnum.xml"
yaml_file_path = "build.yml"


def xml_handler(xmlfilepath, updateby=0.001):
    # Load XML file
    xml_file = xmlfilepath  # Ensure the correct file path

    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()  # Root itself is <BuildNumber>

    # Debug: Print the XML structure
    print("Root tag:", root.tag)
    print("Current BuildNumber value:", root.text)

    # Update the build number by adding 0.001
    try:
        build_number = float(root.text)  # Convert text to float
        build_number += updateby  # Increment by 0.001
        root.text = f"{build_number:.3f}"  # Keep 3 decimal places

        # Save changes back to XML file
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        print("Updated BuildNumber:", root.text)
        print("Build number updated successfully.")
    except ValueError:
        print("Error: BuildNumber is not a valid number.")

def yaml_handler(yamlfilepath, updateby=1):
    # Load YAML file
    yaml_file = yamlfilepath  # Change this to your actual YAML file name

    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)  # Parse YAML file

    # Debug: Print the original YAML content
    print("Original YAML Data:", data)

    # Update the 'Minor' value
    if "variables" in data and "Minor" in data["variables"]:
        data["variables"]["Minor"] += updateby  # Increment by 1

        # Save changes back to the YAML file
        with open(yaml_file, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

        print("Updated Minor:", data["variables"]["Minor"])
        print("Minor version updated successfully.")
    else:
        print("Error: 'variables' or 'Minor' key not found in YAML.")


# Calling functions to implement the increments 
xml_handler(xml_file_path)
yaml_handler(yaml_file_path)