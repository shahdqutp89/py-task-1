# py-task-1
# ARXML Manager

A Python tool for manipulating AUTOSAR XML (ARXML) files with support for attribute operations and JSON conversion.

## Features

-  **Load and save ARXML files**
-  **Add, edit, and delete attributes** in XML elements
-  **Find elements** by tag, XPath, or attribute values
-  **Convert ARXML to JSON** format
-  **Singleton pattern** for consistent instance management
-  **Error handling** for file operations and XML parsing


## Quick Usage

### Basic Example
```python
from arxml_manager import ARXMLManagerFactory

# Create manager instance
manager = ARXMLManagerFactory.create_standard_manager()

# Load ARXML file
manager.load_arxml_file("input.arxml")

# Add attributes
count = manager.add_attribute_by_tag("ECUC-MODULE-CONFIGURATION-VALUES", "version", "1.0")
print(f"Added attribute to {count} elements")

# Save modified file
manager.save_arxml_file("output/updated.arxml")
```

### Command Line Usage
```bash
# Basic usage with arguments
python main.py --input input.arxml --output-arxml output.arxml --output-json output.json

# Add attribute while processing
python main.py --input input.arxml --add-attr "version:1.0:ECUC-MODULE"
```

### JSON Conversion
```python
# Convert ARXML to JSON (after loading)
json_data = manager.convert_to_json()

# Save JSON file
with open("output.json", "w") as f:
    json.dump(json_data, f, indent=2)
```

## Core Operations

### Attribute Management
```python
# Add attribute to all elements with specific tag
count = manager.add_attribute_by_tag("SHORT-NAME", "version", "2.0")

# Edit existing attributes
success = manager.edit_attribute_by_tag("SHORT-NAME", "version", "3.0") 

# Delete attributes
count = manager.delete_attribute_by_tag("SHORT-NAME", "version")
```


### Test Scenarios
See `test_scenarios.txt` for comprehensive test case documentation covering:
- File loading and saving
- Attribute operations (add, edit, delete)
- Element finding
- JSON conversion
- Error handling
- Integration workflows

## Error Handling

- **FileNotFoundError** - Missing input files
- **ValueError** - Invalid XML or XPath syntax
- **RuntimeError** - Operations without loaded file
- **IOError** - File permission or write errors
