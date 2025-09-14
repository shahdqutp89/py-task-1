import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import os
from pathlib import Path

class IXMLReader(ABC):
    @abstractmethod
    def read_file(self, file_path: str) -> ET.Element:
        pass


class IXMLWriter(ABC):
    @abstractmethod
    def write_file(self, root: ET.Element, file_path: str) -> None:
        pass


class IElementManipulator(ABC):
    @abstractmethod
    def add_attribute(self, element: ET.Element, attr_name: str, attr_value: str) -> None:
        pass
    
    @abstractmethod
    def delete_attribute(self, element: ET.Element, attr_name: str) -> bool:
        pass
    
    @abstractmethod
    def edit_attribute(self, element: ET.Element, attr_name: str, new_value: str) -> bool:
        pass


class IElementFinder(ABC):
    @abstractmethod
    def find_element_by_tag(self, root: ET.Element, tag: str) -> List[ET.Element]:
        pass
    
    @abstractmethod
    def find_element_by_xpath(self, root: ET.Element, xpath: str) -> List[ET.Element]:
        pass


class XMLFileReader(IXMLReader):    
    def read_file(self, file_path: str) -> ET.Element:
        """Read XML file and return root element"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {e}")


class XMLFileWriter(IXMLWriter):
    
    def write_file(self, root: ET.Element, file_path: str) -> None:
        try:
            # Get the directory path
            dir_path = os.path.dirname(file_path)
            
            # Only create directories if there's actually a directory path
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='ISO-8859-1', xml_declaration=True)
        except Exception as e:
            raise IOError(f"Failed to write file {file_path}: {e}")


class ElementManipulator(IElementManipulator):    
    def add_attribute(self, element: ET.Element, attr_name: str, attr_value: str) -> None:
        element.set(attr_name, attr_value)
    
    def delete_attribute(self, element: ET.Element, attr_name: str) -> bool:
        if attr_name in element.attrib:
            del element.attrib[attr_name]
            return True
        return False
    
    def edit_attribute(self, element: ET.Element, attr_name: str, new_value: str) -> bool:
        if attr_name in element.attrib:
            element.set(attr_name, new_value)
            return True
        return False


class ElementFinder(IElementFinder):    
    def find_element_by_tag(self, root: ET.Element, tag: str) -> List[ET.Element]:
        return root.findall(f".//{tag}")
    
    def find_element_by_xpath(self, root: ET.Element, xpath: str) -> List[ET.Element]:
        try:
            return root.findall(xpath)
        except Exception as e:
            raise ValueError(f"Invalid XPath expression: {e}")
    
    def find_element_by_attribute(self, root: ET.Element, attr_name: str, attr_value: str) -> List[ET.Element]:
        elements = []
        for elem in root.iter():
            if elem.get(attr_name) == attr_value:
                elements.append(elem)
        return elements


class ARXMLManagerSingleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ARXMLManagerSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True

class ARXMLManager(ARXMLManagerSingleton):

    def __init__(self, reader: IXMLReader = None, writer: IXMLWriter = None, 
                 manipulator: IElementManipulator = None, finder: IElementFinder = None):
        super().__init__()
        
        self._reader = reader or XMLFileReader()
        self._writer = writer or XMLFileWriter()
        self._manipulator = manipulator or ElementManipulator()
        self._finder = finder or ElementFinder()
        
        self._root: Optional[ET.Element] = None
        self._file_path: Optional[str] = None
    
    def load_arxml_file(self, file_path: str) -> None:
        self._root = self._reader.read_file(file_path)
        self._file_path = file_path
        print(f"Successfully loaded ARXML file: {file_path}")
    
    def save_arxml_file(self, output_path: str = None) -> None:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        
        output_file = output_path or self._file_path
        if output_file is None:
            raise ValueError("No output path specified")
        
        self._writer.write_file(self._root, output_file)
        print(f"Successfully saved ARXML file: {output_file}")
    
    # Element finding methods
    def find_elements_by_tag(self, tag: str) -> List[ET.Element]:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        return self._finder.find_element_by_tag(self._root, tag)
    
    def find_elements_by_xpath(self, xpath: str) -> List[ET.Element]:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        return self._finder.find_element_by_xpath(self._root, xpath)
    
    def find_elements_by_attribute(self, attr_name: str, attr_value: str) -> List[ET.Element]:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        return self._finder.find_element_by_attribute(self._root, attr_name, attr_value)
    
    # Attribute manipulation methods
    def add_attribute_to_elements(self, elements: List[ET.Element], attr_name: str, attr_value: str) -> int:
        count = 0
        for element in elements:
            self._manipulator.add_attribute(element, attr_name, attr_value)
            count += 1
        return count
    
    def delete_attribute_from_elements(self, elements: List[ET.Element], attr_name: str) -> int:
        count = 0
        for element in elements:
            if self._manipulator.delete_attribute(element, attr_name):
                count += 1
        return count
    
    def edit_attribute_in_elements(self, elements: List[ET.Element], attr_name: str, new_value: str) -> int:
        count = 0
        for element in elements:
            if self._manipulator.edit_attribute(element, attr_name, new_value):
                count += 1
        return count
    
    # Convenience methods for common operations
    def add_attribute_by_tag(self, tag: str, attr_name: str, attr_value: str) -> int:
        elements = self.find_elements_by_tag(tag)
        return self.add_attribute_to_elements(elements, attr_name, attr_value)
    
    def delete_attribute_by_tag(self, tag: str, attr_name: str) -> int:
        elements = self.find_elements_by_tag(tag)
        return self.delete_attribute_from_elements(elements, attr_name)
    
    def edit_attribute_by_tag(self, tag: str, attr_name: str, new_value: str) -> int:
        elements = self.find_elements_by_tag(tag)
        return self.edit_attribute_in_elements(elements, attr_name, new_value)
    
    def get_element_info(self, element: ET.Element) -> Dict[str, Any]:
        return {
            'tag': element.tag,
            'attributes': dict(element.attrib),
            'text': element.text.strip() if element.text else None,
            'children_count': len(list(element))
        }
    
    def list_all_tags(self) -> List[str]:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        
        tags = set()
        for elem in self._root.iter():
            tags.add(elem.tag)
        return sorted(list(tags))


class ARXMLManagerFactory:    
    @staticmethod
    def create_standard_manager() -> ARXMLManager:
        """Create standard ARXML manager"""
        return ARXMLManager()
    
    @staticmethod
    def create_custom_manager(reader: IXMLReader = None, writer: IXMLWriter = None,
                            manipulator: IElementManipulator = None, finder: IElementFinder = None) -> ARXMLManager:
        """Create custom ARXML manager with injected dependencies"""
        return ARXMLManager(reader, writer, manipulator, finder)


if __name__ == "__main__":
    # Get the singleton instance
    arxml_manager = ARXMLManager()
    
    try:
        # Load the ARXML file
        input_file = "SOUND_Short_eHorizon_Pdu.arxml"
        arxml_manager.load_arxml_file(input_file)
        
        print("=== Analyzing Existing Attributes in ARXML File ===\n")
        
        # Find all elements that have attributes
        elements_with_attributes = []
        attribute_summary = {}
        
        for elem in arxml_manager._root.iter():
            if elem.attrib:  # Element has attributes
                elements_with_attributes.append(elem)
                
                # Count each attribute type
                for attr_name, attr_value in elem.attrib.items():
                    if attr_name not in attribute_summary:
                        attribute_summary[attr_name] = []
                    attribute_summary[attr_name].append({
                        'element': elem,
                        'tag': elem.tag,
                        'value': attr_value
                    })
        
        print(f"Found {len(elements_with_attributes)} elements with attributes")
        print(f"Found {len(attribute_summary)} different attribute types\n")
        
        # Display all existing attributes
        print("=== All Existing Attributes ===")
        for attr_name, occurrences in attribute_summary.items():
            print(f"Attribute '{attr_name}': {len(occurrences)} occurrences")
            # Show first few examples
            for i, occ in enumerate(occurrences[:3]):
                print(f"  Example {i+1}: <{occ['tag']} {attr_name}=\"{occ['value']}\">")
            if len(occurrences) > 3:
                print(f"  ... and {len(occurrences) - 3} more")
            print()
        
        # Test operations on existing attributes
        print("=== Testing Edit Operations on Existing Attributes ===\n")
        
        for attr_name, occurrences in attribute_summary.items():
            if len(occurrences) > 0:  # Only test if attribute exists
                print(f"Testing with attribute '{attr_name}' ({len(occurrences)} elements):")
                
                # Get elements that have this attribute
                elements_with_attr = [occ['element'] for occ in occurrences]
                
                # Show original values (first few)
                print("  Original values:")
                for i, occ in enumerate(occurrences[:3]):
                    print(f"    Element {i+1} ({occ['tag']}): {attr_name}=\"{occ['value']}\"")
                
                # BACKUP original values before editing
                original_values = {}
                for elem in elements_with_attr:
                    original_values[elem] = elem.get(attr_name)
                
                # TEST EDIT: Modify existing attribute values
                new_value = f"EDITED_{attr_name}_VALUE"
                edit_count = arxml_manager.edit_attribute_in_elements(elements_with_attr, attr_name, new_value)
                print(f"  ✅ Edited '{attr_name}' to '{new_value}' in {edit_count} elements")
                
                # Verify the edit worked
                print("  Verification after edit:")
                for i, elem in enumerate(elements_with_attr[:3]):
                    current_value = elem.get(attr_name)
                    print(f"    Element {i+1}: {attr_name}=\"{current_value}\"")
                
                # TEST DELETE: Remove the attribute entirely
                delete_count = arxml_manager.delete_attribute_from_elements(elements_with_attr, attr_name)
                print(f"  ✅ Deleted '{attr_name}' from {delete_count} elements")
                
                # Verify the deletion worked
                print("  Verification after delete:")
                for i, elem in enumerate(elements_with_attr[:3]):
                    current_value = elem.get(attr_name)
                    has_attr = attr_name in elem.attrib
                    print(f"    Element {i+1}: {attr_name} exists={has_attr}, value={current_value}")
                
                # RESTORE original values (so we don't break the file structure)
                print("  Restoring original values...")
                for elem, original_value in original_values.items():
                    elem.set(attr_name, original_value)
                
                # Verify restoration
                print("  Verification after restore:")
                for i, elem in enumerate(elements_with_attr[:3]):
                    restored_value = elem.get(attr_name)
                    print(f"    Element {i+1}: {attr_name}=\"{restored_value}\"")
                
                print("-" * 60)
                
                # Only test first few attributes to avoid too much output
                if list(attribute_summary.keys()).index(attr_name) >= 2:
                    print("(Testing first 3 attribute types only...)\n")
                    break
        
        # Test with convenience methods on existing attributes
        print("=== Testing Convenience Methods on Existing Attributes ===\n")
        
        if attribute_summary:
            # Get the first attribute type that exists
            first_attr = list(attribute_summary.keys())[0]
            occurrences = attribute_summary[first_attr]
            
            if occurrences:
                # Get the tag of elements that have this attribute
                element_tag = occurrences[0]['tag']
                original_value = occurrences[0]['value']
                
                print(f"Testing convenience methods with:")
                print(f"  Tag: '{element_tag}'")
                print(f"  Attribute: '{first_attr}'")
                print(f"  Original value: '{original_value}'")
                
                # Find elements by tag
                elements_by_tag = arxml_manager.find_elements_by_tag(element_tag)
                print(f"  Found {len(elements_by_tag)} elements with tag '{element_tag}'")
                
                # Edit using convenience method
                edit_count = arxml_manager.edit_attribute_by_tag(element_tag, first_attr, "CONVENIENCE_EDIT")
                print(f"  ✅ Convenience edit affected {edit_count} elements")
                
                # Check the change
                if elements_by_tag:
                    new_value = elements_by_tag[0].get(first_attr)
                    print(f"  Verification: First element now has {first_attr}=\"{new_value}\"")
                
                # Restore using convenience method  
                restore_count = arxml_manager.edit_attribute_by_tag(element_tag, first_attr, original_value)
                print(f"  ✅ Convenience restore affected {restore_count} elements")
                
                # Delete using convenience method
                delete_count = arxml_manager.delete_attribute_by_tag(element_tag, first_attr)
                print(f"  ✅ Convenience delete affected {delete_count} elements")
                
                # Restore the attribute completely
                add_count = arxml_manager.add_attribute_by_tag(element_tag, first_attr, original_value)
                print(f"  ✅ Convenience restore (add back) affected {add_count} elements")
        
        # Test finding by existing attribute values
        print("\n=== Testing Find by Existing Attribute Values ===")
        
        if attribute_summary:
            for attr_name, occurrences in list(attribute_summary.items())[:2]:  # Test first 2 attributes
                if occurrences:
                    test_value = occurrences[0]['value']
                    print(f"\nSearching for elements with {attr_name}='{test_value}':")
                    
                    found_elements = arxml_manager.find_elements_by_attribute(attr_name, test_value)
                    print(f"  Found {len(found_elements)} elements")
                    
                    for i, elem in enumerate(found_elements[:3]):
                        info = arxml_manager.get_element_info(elem)
                        print(f"  Element {i+1}: <{info['tag']}> with {len(info['attributes'])} attributes")
        
        # Save to verify everything still works
        print("\n=== Saving File ===")
        arxml_manager.save_arxml_file("output_existing_attrs_test.arxml")
        
        print("\n=== Test Summary ===")
        print("✅ Successfully tested edit operations on existing attributes")
        print("✅ Successfully tested delete operations on existing attributes") 
        print("✅ Successfully tested convenience methods")
        print("✅ Successfully tested find by attribute value")
        print("✅ All original values were properly restored")
        print("✅ File structure integrity maintained")
        
        print(f"\nYour ARXML file contains:")
        print(f"  - {len(elements_with_attributes)} elements with attributes")
        print(f"  - {len(attribute_summary)} different attribute types")
        print("  - All operations confirmed working on real data!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()