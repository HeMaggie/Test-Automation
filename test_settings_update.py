#!/usr/bin/env python3
"""Test script to verify database settings update"""

from database.get_mypos import GetMypos
from config import Config
import json
import time

def test_settings_update():
    """Test if support.taxb4discountnew setting is being updated correctly"""
    
    db = GetMypos(Config.SERVER_IP)
    
    print("=" * 60)
    print("Testing Database Settings Update")
    print("=" * 60)
    
    # Get initial state
    print("\n1. Getting initial mystore settings...")
    initial_results = db.get_mystore()
    if initial_results:
        support_field = initial_results[0].get('support')
        print(f"Initial support field type: {type(support_field)}")
        print(f"Initial support field raw value: {support_field}")
        
        if support_field:
            try:
                if isinstance(support_field, str):
                    support_json = json.loads(support_field)
                else:
                    support_json = support_field
                print(f"Initial support JSON: {support_json}")
                initial_value = support_json.get('taxb4discountnew')
                print(f"Initial taxb4discountnew value: {initial_value}")
            except Exception as e:
                print(f"Error parsing support field: {e}")
        else:
            print("Support field is empty or None")
    
    # Test updating the setting
    print("\n2. Updating support.taxb4discountnew to 0...")
    test_settings = {"support.taxb4discountnew": 0}
    db.update_mystore_settings(test_settings)
    
    # Wait a moment for update to complete
    time.sleep(1)
    
    # Check if update worked
    print("\n3. Verifying update...")
    updated_results = db.get_mystore()
    if updated_results:
        support_field = updated_results[0].get('support')
        print(f"Updated support field type: {type(support_field)}")
        print(f"Updated support field raw value: {support_field}")
        
        if support_field:
            try:
                if isinstance(support_field, str):
                    support_json = json.loads(support_field)
                else:
                    support_json = support_field
                print(f"Updated support JSON: {support_json}")
                updated_value = support_json.get('taxb4discountnew')
                print(f"Updated taxb4discountnew value: {updated_value}")
                
                if updated_value == 0:
                    print("✓ Setting updated successfully to 0")
                else:
                    print(f"✗ Setting update failed! Value is {updated_value}")
            except Exception as e:
                print(f"Error parsing support field: {e}")
    
    # Test updating to 1
    print("\n4. Updating support.taxb4discountnew to 1...")
    test_settings = {"support.taxb4discountnew": 1}
    db.update_mystore_settings(test_settings)
    
    time.sleep(1)
    
    print("\n5. Verifying update to 1...")
    final_results = db.get_mystore()
    if final_results:
        support_field = final_results[0].get('support')
        if support_field:
            try:
                if isinstance(support_field, str):
                    support_json = json.loads(support_field)
                else:
                    support_json = support_field
                final_value = support_json.get('taxb4discountnew')
                print(f"Final taxb4discountnew value: {final_value}")
                
                if final_value == 1:
                    print("✓ Setting updated successfully to 1")
                else:
                    print(f"✗ Setting update failed! Value is {final_value}")
            except Exception as e:
                print(f"Error parsing support field: {e}")
    
    # Test updating all three settings together
    print("\n6. Testing combined settings update...")
    combined_settings = {
        "store_tip": 1,
        "tipbefored": 0,
        "support.taxb4discountnew": 0
    }
    db.update_mystore_settings(combined_settings)
    
    time.sleep(1)
    
    print("\n7. Verifying combined update...")
    combined_results = db.get_mystore()
    if combined_results:
        store_tip = combined_results[0].get('store_tip')
        tipbefored = combined_results[0].get('tipbefored')
        support_field = combined_results[0].get('support')
        
        print(f"store_tip: {store_tip}")
        print(f"tipbefored: {tipbefored}")
        
        if support_field:
            try:
                if isinstance(support_field, str):
                    support_json = json.loads(support_field)
                else:
                    support_json = support_field
                taxb4disc = support_json.get('taxb4discountnew')
                print(f"support.taxb4discountnew: {taxb4disc}")
                
                if store_tip == 1 and tipbefored == 0 and taxb4disc == 0:
                    print("✓ All settings updated successfully")
                else:
                    print("✗ Some settings failed to update")
            except Exception as e:
                print(f"Error parsing support field: {e}")
    
    print("\n" + "=" * 60)
    print("Test complete")
    print("=" * 60)

if __name__ == "__main__":
    test_settings_update()