import xml.etree.ElementTree as ET
import json


def arxml_to_dict(elem):
    """Recursively convert an ElementTree element into a dictionary."""
    d = {}

    # Include element attributes if any
    if elem.attrib:
        # Use attribute keys as-is, you may want to process namespaces if needed
        d.update({f"@{k}": v for k, v in elem.attrib.items()})

    # Process child elements
    children = list(elem)
    if children:
        # Group children by tag
        child_dict = {}
        for child in children:
            child_tag = child.tag.split("}")[-1]  # Remove namespace
            child_data = arxml_to_dict(child)
            # If tag already exists, convert to list
            if child_tag in child_dict:
                if not isinstance(child_dict[child_tag], list):
                    child_dict[child_tag] = [child_dict[child_tag]]
                child_dict[child_tag].append(child_data)
            else:
                child_dict[child_tag] = child_data
        d.update(child_dict)
    else:
        # Leaf node, get text
        text = elem.text.strip() if elem.text else ""
        if text:
            d = text if not d else {**d, "#text": text}
        else:
            if not d:
                d = None  # Empty element

    return d


def main():
    # Load ARXML file
    input_file = "SOUND_Short_eHorizon_Pdu.arxml"
    output_file = "output.json"

    tree = ET.parse(input_file)
    root = tree.getroot()

    # Convert root element (strip namespace for root tag)
    root_tag = root.tag.split("}")[-1]
    arxml_dict = {root_tag: arxml_to_dict(root)}

    # Save JSON output
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(arxml_dict, f, indent=2)

    print(f"Converted {input_file} to {output_file}")


if __name__ == "__main__":
    main()
