from arxml_manager import ARXMLManagerFactory

def main():
    manager = ARXMLManagerFactory.create_standard_manager()
    manager.load_arxml_file("SOUND_Short_eHorizon_Pdu.arxml")
    manager.add_attribute_by_tag("ECUC-MODULE-CONFIGURATION-VALUES", "version", "1.0")
    manager.save_arxml_file("output/output.arxml")

if __name__ == "__main__":
    main()
