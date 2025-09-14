import os
import xml.etree.ElementTree as ET
from typing import List
from interfaces import IXMLReader, IXMLWriter, IElementManipulator, IElementFinder

class XMLFileReader(IXMLReader):
    def read_file(self, file_path: str) -> ET.Element:
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
            dir_path = os.path.dirname(file_path)
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
        return [elem for elem in root.iter() if elem.get(attr_name) == attr_value]
