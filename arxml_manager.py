import xml.etree.ElementTree as ET
from typing import Optional, List, Dict, Any

from implementations import XMLFileReader, XMLFileWriter, ElementManipulator, ElementFinder

class ARXMLManagerSingleton:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True

class ARXMLManager(ARXMLManagerSingleton):
    def __init__(self, reader=None, writer=None, manipulator=None, finder=None):
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

    def find_elements_by_tag(self, tag: str) -> List[ET.Element]:
        if self._root is None:
            raise RuntimeError("No ARXML file loaded")
        return self._finder.find_element_by_tag(self._root, tag)

    def add_attribute_by_tag(self, tag: str, attr_name: str, attr_value: str) -> int:
        elements = self.find_elements_by_tag(tag)
        for e in elements:
            self._manipulator.add_attribute(e, attr_name, attr_value)
        return len(elements)

class ARXMLManagerFactory:
    @staticmethod
    def create_standard_manager() -> ARXMLManager:
        return ARXMLManager()

    @staticmethod
    def create_custom_manager(reader=None, writer=None, manipulator=None, finder=None) -> ARXMLManager:
        return ARXMLManager(reader, writer, manipulator, finder)
