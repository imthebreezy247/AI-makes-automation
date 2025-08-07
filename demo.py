#!/usr/bin/env python3
"""
Demo script showing AI automation generation
"""

import json
import os
from automation_generator import AutomationGenerator
from validator import AutomationValidator, ValidationReporter
from templates import AutomationTemplates

def demo():
    """Demonstrate the automation generator"""
    
    print("🚀 AI Makes Automation - Demo")
    print("=" * 50)
    print("Generate complete Make.com automations from simple descriptions!")
    print()
    
    generator = AutomationGenerator()
    validator = AutomationValidator()
    
    # Demo 1: Simple email automation
    print("📧 Demo 1: Email Support Automation")
    print("-" * 40)
    description = "Monitor support@company.com emails and auto-reply to common questions"
    print(f"Input: {description}")
    
    automation = generator.generate_automation(description)
    is_valid, results = validator.validate_automation(automation)
    
    print(f"✅ Generated: {automation['name']}")
    print(f"📊 Modules: {len(automation['modules'])}")
    print(f"🔌 Connections: {len(automation['connections'])}")
    print(f"🔍 Valid: {'✅' if is_valid else '⚠️'}")
    
    # Save demo output
    os.makedirs("output", exist_ok=True)
    with open("output/demo_email_automation.json", "w") as f:
        json.dump({
            "automation": automation,
            "blueprint": json.loads(generator.export_to_make_blueprint(automation)),
            "validation": ValidationReporter.generate_report(results)
        }, f, indent=2)
    
    print("💾 Saved to: output/demo_email_automation.json")
    
    # Demo 2: Template usage
    print("\n📊 Demo 2: Pre-built Template")
    print("-" * 40)
    
    template = AutomationTemplates.gmail_customer_support()
    print(f"Template: {template['name']}")
    print(f"📋 {template['description']}")
    print(f"📊 Modules: {len(template['blueprint']['flow'])}")
    
    with open("output/demo_template.json", "w") as f:
        json.dump(template, f, indent=2)
    
    print("💾 Template saved to: output/demo_template.json")
    
    # Demo 3: Show what gets generated
    print("\n🔧 Demo 3: Generated Configuration Sample")
    print("-" * 40)
    
    sample_module = automation['modules'][0] if automation['modules'] else {}
    print("Sample Gmail Watch Module:")
    print(json.dumps(sample_module, indent=2)[:500] + "...")
    
    print("\n✨ Key Features:")
    print("• Natural language input → Complete automation")
    print("• Full Make.com JSON configuration")
    print("• Built-in validation and error checking")
    print("• Pre-built templates for common patterns")
    print("• Connection setup instructions")
    print("• Error handling and best practices")
    
    print("\n🎯 Usage:")
    print("1. Describe what you want to automate")
    print("2. Get complete Make.com configuration")
    print("3. Copy JSON to Make.com")
    print("4. Configure connections")
    print("5. Test and activate!")
    
    print(f"\n📁 Check the output/ directory for generated files")
    print("🚀 Ready to automate!")

if __name__ == "__main__":
    demo()