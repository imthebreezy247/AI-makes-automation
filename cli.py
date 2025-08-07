#!/usr/bin/env python3
"""
Make.com Automation Generator CLI
Interactive command-line interface for generating automations
"""

import argparse
import json
import sys
import os
from typing import Dict, List, Any, Optional
import re

# Import our modules
from automation_generator import AutomationGenerator
from templates import AutomationTemplates
from validator import AutomationValidator, ValidationReporter

class AutomationCLI:
    def __init__(self):
        self.generator = AutomationGenerator()
        self.templates = AutomationTemplates()
        self.validator = AutomationValidator()
    
    def interactive_mode(self):
        """Run interactive mode for automation creation"""
        print("🤖 AI Make.com Automation Generator")
        print("="*50)
        print("Describe what you want to automate and I'll generate the complete Make.com configuration!")
        print("Type 'help' for examples, 'templates' to see pre-built options, or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("📝 Describe your automation: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'templates':
                    self.show_templates()
                    continue
                
                if user_input.lower().startswith('template:'):
                    template_name = user_input[9:].strip()
                    self.use_template(template_name)
                    continue
                
                # Generate automation
                print("\n🔄 Generating automation...")
                self.generate_and_display(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for examples.")
    
    def generate_and_display(self, description: str):
        """Generate automation and display results"""
        try:
            # Generate automation
            automation = self.generator.generate_automation(description)
            blueprint = self.generator.export_to_make_blueprint(automation)
            
            # Validate automation
            print("\n🔍 Validating automation...")
            is_valid, validation_results = self.validator.validate_automation(automation)
            
            # Display validation results
            validation_report = ValidationReporter.generate_report(validation_results)
            print(validation_report)
            
            if not is_valid:
                print("\n⚠️  Automation has errors but will still be saved. Please review and fix issues.")
            
            # Display results
            print(f"\n✅ Generated: {automation['name']}")
            print(f"📊 Modules: {len(automation['modules'])}")
            print(f"🔌 Connections: {len(automation['connections'])}")
            
            # Save to file
            filename = self.save_automation(automation, blueprint, validation_results)
            print(f"💾 Saved to: {filename}")
            
            # Show connections needed
            if automation['connections']:
                print(f"\n🔌 Connections to configure in Make.com:")
                for conn in automation['connections']:
                    print(f"   • {conn['name']}: {conn['description']}")
            
            # Ask if user wants to see the full blueprint
            show_blueprint = input(f"\n📄 Show full Make.com blueprint? (y/n): ").strip().lower()
            if show_blueprint in ['y', 'yes']:
                print(f"\n📋 Make.com Blueprint (copy this to Make.com):")
                print("="*60)
                print(blueprint)
            
            print(f"\n✨ Copy the blueprint from {filename} to Make.com and configure the connections!")
            
        except Exception as e:
            print(f"❌ Error generating automation: {e}")
    
    def show_help(self):
        """Show help information"""
        print("""
🆘 Help - How to use the AI Automation Generator

📝 Example Descriptions:
   • "Monitor support emails and auto-reply to common questions"
   • "Sync Excel data to MySQL database every hour with AI validation"
   • "Watch Gmail for invoices and save to Google Drive"
   • "Create tickets from customer emails in our MySQL system"
   • "Process API data and generate Excel reports"

🎯 Keywords the AI understands:
   • Triggers: email, gmail, schedule, webhook, excel
   • Processing: AI, analyze, categorize, validate, process
   • Actions: reply, save, create, update, sync, alert
   • Storage: database, mysql, excel, drive, slack

📋 Commands:
   • help - Show this help
   • templates - Show pre-built templates
   • template:name - Use a specific template
   • quit - Exit the program

💡 Tips:
   • Be specific about triggers (what starts the automation)
   • Mention data sources and destinations
   • Include any special requirements or conditions
   • The more detail, the better the result!
        """)
    
    def show_templates(self):
        """Show available templates"""
        templates = AutomationTemplates.get_all_templates()
        
        print("\n🎯 Available Pre-built Templates:")
        print("="*50)
        
        for i, (name, template) in enumerate(templates.items(), 1):
            print(f"{i}. {name.replace('_', ' ').title()}")
            print(f"   📋 {template['description']}")
            print(f"   📊 {len(template['blueprint']['flow'])} modules")
            print()
        
        print("💡 Usage: Type 'template:gmail_customer_support' to use a template")
        
        # Ask user if they want to use a template
        choice = input("📝 Enter template name or press Enter to continue: ").strip()
        if choice:
            self.use_template(choice)
    
    def use_template(self, template_name: str):
        """Use a specific template"""
        templates = AutomationTemplates.get_all_templates()
        
        # Clean template name
        template_name = template_name.lower().replace(' ', '_').replace('-', '_')
        
        if template_name in templates:
            template = templates[template_name]
            
            print(f"\n🎯 Using template: {template_name.replace('_', ' ').title()}")
            print(f"📋 {template['description']}")
            
            # Save template
            blueprint = json.dumps(template['blueprint'], indent=2)
            filename = self.save_template(template_name, template, blueprint)
            
            print(f"💾 Template saved to: {filename}")
            
            # Show AI agent config if available
            if 'ai_agent_config' in template:
                print(f"\n🤖 AI Agent Configuration:")
                print(f"   Name: {template['ai_agent_config']['name']}")
                print(f"   Tokens: {template['ai_agent_config']['max_tokens']}")
                
            # Show connections
            if 'connections' in template:
                print(f"\n🔌 Required connections:")
                for conn in template['connections']:
                    print(f"   • {conn['name']}: {conn['type']}")
            
            show_blueprint = input(f"\n📄 Show full blueprint? (y/n): ").strip().lower()
            if show_blueprint in ['y', 'yes']:
                print(f"\n📋 Make.com Blueprint:")
                print("="*60)
                print(blueprint)
        else:
            available = list(templates.keys())
            print(f"❌ Template '{template_name}' not found.")
            print(f"Available templates: {', '.join(available)}")
    
    def save_automation(self, automation: Dict[str, Any], blueprint: str, validation_results: List = None) -> str:
        """Save automation to file"""
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', automation['name'])
        filename = f"output/{safe_name}.json"
        
        # Prepare save data
        save_data = {
            'automation': automation,
            'blueprint': json.loads(blueprint),
            'readme': {
                'description': automation['description'],
                'modules': len(automation['modules']),
                'connections': [conn['name'] for conn in automation['connections']],
                'instructions': [
                    '1. Copy the blueprint JSON to Make.com',
                    '2. Configure the required connections', 
                    '3. Test each module individually',
                    '4. Run end-to-end test',
                    '5. Activate the scenario'
                ]
            }
        }
        
        # Add validation results if available
        if validation_results:
            save_data['validation'] = {
                'report': ValidationReporter.generate_report(validation_results),
                'json_report': json.loads(ValidationReporter.generate_json_report(validation_results))
            }
        
        # Save full automation data
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return filename
    
    def save_template(self, name: str, template: Dict[str, Any], blueprint: str) -> str:
        """Save template to file"""
        os.makedirs("output", exist_ok=True)
        filename = f"output/template_{name}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'template': template,
                'blueprint': json.loads(blueprint)
            }, f, indent=2)
        
        return filename
    
    def batch_mode(self, input_file: str, output_dir: str = "output"):
        """Process multiple descriptions from file"""
        if not os.path.exists(input_file):
            print(f"❌ Input file not found: {input_file}")
            return
        
        print(f"📂 Processing batch file: {input_file}")
        os.makedirs(output_dir, exist_ok=True)
        
        with open(input_file, 'r') as f:
            descriptions = [line.strip() for line in f if line.strip()]
        
        for i, description in enumerate(descriptions, 1):
            print(f"\n🔄 Processing {i}/{len(descriptions)}: {description[:50]}...")
            
            try:
                automation = self.generator.generate_automation(description)
                blueprint = self.generator.export_to_make_blueprint(automation)
                
                # Save with index
                safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', automation['name'])
                filename = f"{output_dir}/batch_{i:03d}_{safe_name}.json"
                
                with open(filename, 'w') as f:
                    json.dump({
                        'automation': automation,
                        'blueprint': json.loads(blueprint)
                    }, f, indent=2)
                
                print(f"✅ Saved: {filename}")
                
            except Exception as e:
                print(f"❌ Error processing item {i}: {e}")
        
        print(f"\n🎉 Batch processing complete! Check {output_dir}/ for results.")

def main():
    parser = argparse.ArgumentParser(
        description="AI-powered Make.com automation generator",
        epilog="Examples:\n"
               "  %(prog)s --interactive\n"
               "  %(prog)s --description 'Monitor emails and auto-reply'\n"
               "  %(prog)s --template gmail_customer_support\n"
               "  %(prog)s --batch descriptions.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '-d', '--description',
        type=str,
        help='Generate automation from description'
    )
    
    parser.add_argument(
        '-t', '--template',
        type=str,
        help='Use a pre-built template'
    )
    
    parser.add_argument(
        '-b', '--batch',
        type=str,
        help='Process multiple descriptions from file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--list-templates',
        action='store_true',
        help='List available templates'
    )
    
    args = parser.parse_args()
    
    cli = AutomationCLI()
    
    if args.list_templates:
        cli.show_templates()
        return
    
    if args.interactive:
        cli.interactive_mode()
        return
    
    if args.batch:
        cli.batch_mode(args.batch, args.output)
        return
    
    if args.template:
        cli.use_template(args.template)
        return
    
    if args.description:
        cli.generate_and_display(args.description)
        return
    
    # Default to interactive mode
    cli.interactive_mode()

if __name__ == "__main__":
    main()