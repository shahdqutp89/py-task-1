from arxml_manager import ARXMLManager

if __name__ == "__main__":
    arxml_manager = ARXMLManager()
    
    try:
        input_file = "SOUND_Short_eHorizon_Pdu.arxml"
        arxml_manager.load_arxml_file(input_file)
        
        print("ARXML Manager Test Suite")
        print("=" * 50)
        
        all_elements = list(arxml_manager._root.iter())
        elements_with_attrs = [elem for elem in all_elements if elem.attrib]
        
        existing_attrs = {}
        for elem in elements_with_attrs:
            for attr_name in elem.attrib.keys():
                if attr_name not in existing_attrs:
                    existing_attrs[attr_name] = 0
                existing_attrs[attr_name] += 1
        
        # TEST 1: Add new attributes
        print("TEST 1: Add New Attributes")
        
        # Add attribute to SHORT-NAME elements
        count = arxml_manager.add_attribute_by_tag('SHORT-NAME', 'test-version', '1.0')
        print(f"Added 'test-version' attribute to {count} SHORT-NAME elements")
        
        # Verify addition
        short_name_elements = arxml_manager.find_elements_by_tag('SHORT-NAME')
        verified = sum(1 for elem in short_name_elements if elem.get('test-version') == '1.0')
        print(f"Verified: {verified} elements now have the new attribute")
        
        # TEST 2: Edit existing attributes 
        print("TEST 2: Edit Existing Attributes")
        
        if existing_attrs:
            # Find an element with UUID attribute 
            uuid_elements = [elem for elem in elements_with_attrs if 'UUID' in elem.attrib]
            if uuid_elements:
                elem = uuid_elements[0]
                original_uuid = elem.get('UUID')
                
                # Edit the UUID
                success = arxml_manager._manipulator.edit_attribute(elem, 'UUID', 'EDITED-UUID-VALUE')
                print(f"Edited UUID attribute: {success}")
                
                # Verify edit
                new_uuid = elem.get('UUID')
                print(f"UUID changed from '{original_uuid[:20]}...' to '{new_uuid}'")
                
                # Restore original
                elem.set('UUID', original_uuid)
                print("Restored original UUID value")
            else:
                print("No UUID attributes found to test editing", False)
        
        # TEST 3: Edit newly added attributes
        print("TEST 3: Edit Added Attributes")
        
        # Find elements with my test attribute and edit them
        elements_to_edit = [elem for elem in short_name_elements if 'test-version' in elem.attrib]
        edit_count = 0
        for elem in elements_to_edit:
            if arxml_manager._manipulator.edit_attribute(elem, 'test-version', '2.0'):
                edit_count += 1
        
        print(f"Edited 'test-version' to '2.0' in {edit_count} elements")
        
        # Verify edit
        updated_count = sum(1 for elem in short_name_elements if elem.get('test-version') == '2.0')
        print(f"Verified: {updated_count} elements have version '2.0'")
        
        # TEST 4: Delete existing attributes (temporary)
        print("TEST 4: Delete Existing Attributes")
        
        if existing_attrs:
            # Test deleting DEST attribute if it exists
            dest_elements = [elem for elem in elements_with_attrs if 'DEST' in elem.attrib]
            if dest_elements:
                test_elem = dest_elements[0]
                original_dest = test_elem.get('DEST')
                
                # Delete the attribute
                success = arxml_manager._manipulator.delete_attribute(test_elem, 'DEST')
                print(f"Deleted DEST attribute: {success}")
                
                # Verify deletion
                has_dest = 'DEST' in test_elem.attrib
                print(f"Attribute removed: {not has_dest}")
                
                # Restore it
                test_elem.set('DEST', original_dest)
                print("Restored DEST attribute")
            else:
                print("No DEST attributes found to test deletion", False)
        
        # TEST 5: Delete added attributes
        print("TEST 5: Delete Added Attributes")
        
        # Delete my test attributes
        delete_count = 0
        for elem in short_name_elements:
            if arxml_manager._manipulator.delete_attribute(elem, 'test-version'):
                delete_count += 1
        
        print(f"Deleted 'test-version' from {delete_count} elements")
        
        # Verify deletion
        remaining = sum(1 for elem in short_name_elements if 'test-version' in elem.attrib)
        print(f"Verified: {remaining} elements still have 'test-version' (should be 0)")
        
        # TEST 6: Element finding
        print("TEST 6: Element Finding")
        
        # Find by tag
        length_elements = arxml_manager.find_elements_by_tag('LENGTH')
        print(f"Found {len(length_elements)} LENGTH elements")
        
        # Find by attribute (if UUID exists)
        if existing_attrs and 'UUID' in existing_attrs:
            uuid_elem = next(elem for elem in elements_with_attrs if 'UUID' in elem.attrib)
            uuid_value = uuid_elem.get('UUID')
            found_by_attr = arxml_manager._finder.find_element_by_attribute(arxml_manager._root, 'UUID', uuid_value)
            print(f"Found {len(found_by_attr)} elements by UUID attribute")
        
        # TEST 7: Save file
        print("TEST 7: Save File")
        
        output_file = "output_test_result.arxml"
        arxml_manager.save_arxml_file(output_file)
        print(f"Saved file as '{output_file}'")

        print(f"\nOutput saved to: {output_file}")
        
    except FileNotFoundError:
        print("Error: Could not find '{input_file}'")
        print("Make sure the file exists in the current directory")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
