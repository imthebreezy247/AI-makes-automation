#!/usr/bin/env python3
"""
Test script to demonstrate the AI automation generator
"""

import json
from automation_generator import AutomationGenerator
from validator import AutomationValidator, ValidationReporter

def test_generation():
    """Test automation generation with various descriptions"""
    
    generator = AutomationGenerator()
    validator = AutomationValidator()
    
    test_cases = [
        "Monitor support@company.com emails, classify them with AI, and auto-reply to simple questions",
        "Sync Excel sales data to MySQL database every hour with validation",
        "Watch for webhook data, process with AI, and create Slack alerts",
        "Monitor Gmail for invoices and save attachments to Google Drive"
    ]
    
    print("🤖 AI Make.com Automation Generator - Test Results")
    print("=" * 60)
    
    for i, description in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {description[:50]}...")
        print("-" * 60)
        
        try:
            # Generate automation
            automation = generator.generate_automation(description)
            
            # Validate
            is_valid, results = validator.validate_automation(automation)
            
            # Results
            print(f"✅ Generated: {automation['name']}")
            print(f"📊 Modules: {len(automation['modules'])}")
            print(f"🔌 Connections: {len(automation['connections'])}")
            print(f"🔍 Valid: {'✅ Yes' if is_valid else '❌ No'}")
            
            if results:
                errors = sum(1 for r in results if r.level.value == "error")
                warnings = sum(1 for r in results if r.level.value == "warning")
                print(f"⚠️  Issues: {errors} errors, {warnings} warnings")
            
            # Show connections
            if automation['connections']:
                print("🔌 Required connections:")
                for conn in automation['connections']:
                    print(f"   • {conn['name']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_generation()