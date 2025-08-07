#!/usr/bin/env python3
"""
Generate Chris's specific Gmail deal processing automation
"""

from automation_generator import AutomationGenerator
from validator import AutomationValidator, ValidationReporter
import json
import os

def generate_chris_automation():
    """Generate the specific automation for Chris's deal processing"""
    
    print("🎯 Generating Chris's Deal Processing Automation")
    print("=" * 60)
    
    # Detailed description based on README requirements
    description = """
    Create Gmail automation for chris@cjsinsurancesolutions.com that:
    - Monitors Gmail label 'Sold deal' 
    - Runs weekly (every 7 days)
    - Processes 5 emails at a time
    - Extracts client names from email subject lines (first and last name)
    - Extracts agent names from email senders (first name + first initial of last name)
    - NEVER extracts Christopher Shannahan or Chris Shannahan as agent names
    - Formats output as: '25x5 Referral fee for 1. ClientName \\ Agt: AgentName - 2. ClientName \\ Agt: AgentName...'
    - Keeps output under 200 characters
    - Marks processed emails with label to avoid reprocessing
    - Continues until all emails in label are processed
    """
    
    generator = AutomationGenerator()
    validator = AutomationValidator()
    
    # Generate the automation
    automation = generator.generate_automation(description)
    
    # Customize for Chris's specific needs
    automation = customize_for_chris(automation)
    
    # Validate
    is_valid, results = validator.validate_automation(automation)
    
    # Generate blueprint
    blueprint = generator.export_to_make_blueprint(automation)
    
    # Show results
    print(f"✅ Generated: {automation['name']}")
    print(f"📊 Modules: {len(automation['modules'])}")
    print(f"🔌 Connections: {len(automation['connections'])}")
    print(f"🔍 Valid: {'✅ Yes' if is_valid else '⚠️ Has issues'}")
    
    if results:
        validation_report = ValidationReporter.generate_report(results)
        print("\n" + validation_report)
    
    # Save the automation
    os.makedirs("output", exist_ok=True)
    filename = "output/chris_deal_processor.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "automation": automation,
            "blueprint": json.loads(blueprint),
            "validation": {
                "report": ValidationReporter.generate_report(results),
                "is_valid": is_valid
            },
            "setup_instructions": {
                "gmail_account": "chris@cjsinsurancesolutions.com",
                "label_to_monitor": "Sold deal",
                "frequency": "Weekly (every 7 days)",
                "batch_size": "5 emails per execution",
                "output_format": "25x5 Referral fee for 1. ClientName \\ Agt: AgentName - ...",
                "character_limit": 200,
                "exclusions": ["Christopher Shannahan", "Chris Shannahan"]
            }
        }, f, indent=2)
    
    print(f"\n💾 Saved complete automation to: {filename}")
    
    # Show the blueprint preview
    print(f"\n📋 Make.com Blueprint Preview:")
    print("="*50)
    blueprint_data = json.loads(blueprint)
    print(f"Scenario Name: {blueprint_data['name']}")
    print(f"Modules: {len(blueprint_data['flow'])}")
    
    for i, module in enumerate(blueprint_data['flow'][:3], 1):  # Show first 3 modules
        print(f"  {i}. {module['module']} (ID: {module['id']})")
    
    if len(blueprint_data['flow']) > 3:
        print(f"  ... and {len(blueprint_data['flow']) - 3} more modules")
    
    print(f"\n🔌 Required Connections:")
    for conn in automation['connections']:
        print(f"  • {conn['name']}: {conn['description']}")
    
    print(f"\n📄 Next Steps:")
    print("1. Copy the blueprint JSON from the saved file")
    print("2. Go to Make.com and create a new scenario")
    print("3. Import the blueprint")
    print("4. Configure the Gmail connection for chris@cjsinsurancesolutions.com")
    print("5. Set up the AI agent with the generated system prompt")
    print("6. Test with a few emails first")
    print("7. Activate for weekly processing")
    
    print(f"\n🎉 Your automation is ready!")
    return filename

def customize_for_chris(automation):
    """Customize the automation for Chris's specific requirements"""
    
    # Update name and description
    automation['name'] = 'Chris_Deal_Processor_Automation'
    automation['description'] = 'Weekly Gmail deal processing for chris@cjsinsurancesolutions.com'
    
    # Find and customize Gmail module
    for module in automation['modules']:
        if module.get('module') == 'gmail':
            # Customize Gmail parameters for Chris's requirements
            module['parameters'].update({
                'folder': 'INBOX',  # Will use label filter instead
                'filter': 'label:"Sold deal" is:unread',
                'maxResults': 5,  # Process 5 at a time
                'markAsRead': False  # Don't mark as read, will add label instead
            })
    
    # Find and customize AI Agent module
    for module in automation['modules']:
        if module.get('module') == 'make-ai-agents':
            # Add custom system prompt for Chris's deal processing
            module['mapper'] = {
                'messages': [
                    {
                        'role': 'system',
                        'content': '''You are a deal processing specialist for Chris's insurance business. 

Extract information from sold deal emails:

1. CLIENT NAME: Extract first and last name from the email subject line
2. AGENT NAME: Extract sender's first name + first initial of last name
3. NEVER extract "Christopher Shannahan" or "Chris Shannahan" as agent names

Format exactly as: "25x5 Referral fee for 1. [ClientName] \\ Agt: [AgentName] - 2. [ClientName] \\ Agt: [AgentName] - 3. [ClientName] \\ Agt: [AgentName] - 4. [ClientName] \\ Agt: [AgentName] - 5. [ClientName] \\ Agt: [AgentName]"

Keep under 200 characters total. Process exactly 5 deals per batch.'''
                    },
                    {
                        'role': 'user', 
                        'content': 'Process these emails and extract deal information:\n\nEmail 1 Subject: {{1.subject}}\nFrom: {{1.from}}\n\nEmail 2 Subject: {{2.subject}}\nFrom: {{2.from}}\n\nEmail 3 Subject: {{3.subject}}\nFrom: {{3.from}}\n\nEmail 4 Subject: {{4.subject}}\nFrom: {{4.from}}\n\nEmail 5 Subject: {{5.subject}}\nFrom: {{5.from}}'
                    }
                ]
            }
    
    # Add schedule module for weekly processing
    schedule_module = {
        'id': len(automation['modules']) + 1,
        'module': 'builtin:schedule',
        'version': 1,
        'parameters': {
            'schedule': '0 0 * * 1'  # Every Monday at midnight
        },
        'metadata': {
            'designer': {'x': -300, 'y': 0}
        }
    }
    
    # Insert schedule at the beginning
    automation['modules'].insert(0, schedule_module)
    
    # Add Gmail label module to mark processed emails
    label_module = {
        'id': len(automation['modules']) + 1,
        'module': 'gmail',
        'version': 1,
        'parameters': {
            'modifyLabels': True,
            'connection': '{{gmail_connection}}',
            'messageId': '{{1.id}}',  # Will need iterator for multiple emails
            'addLabelIds': ['processed_deals'],
            'removeLabelIds': ['Sold deal']
        },
        'metadata': {
            'designer': {'x': 1500, 'y': 0}
        }
    }
    
    automation['modules'].append(label_module)
    
    return automation

if __name__ == "__main__":
    generate_chris_automation()