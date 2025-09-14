from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from typing import List

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
    def add_attribute(self, element: ET.Element, attr_name: str, attr_value: str) -> None: pass

    @abstractmethod
    def delete_attribute(self, element: ET.Element, attr_name: str) -> bool: pass

    @abstractmethod
    def edit_attribute(self, element: ET.Element, attr_name: str, new_value: str) -> bool: pass

class IElementFinder(ABC):
    @abstractmethod
    def find_element_by_tag(self, root: ET.Element, tag: str) -> List[ET.Element]: pass

    @abstractmethod
    def find_element_by_xpath(self, root: ET.Element, xpath: str) -> List[ET.Element]: pass
