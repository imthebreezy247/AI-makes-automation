#!/usr/bin/env python3
"""
Make.com Automation Generator
Generates complete Make.com automation configurations from natural language descriptions
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re

class ModuleType(Enum):
    GMAIL_WATCH = "gmail_watch_emails"
    GMAIL_SEND = "gmail_send_email"
    GMAIL_CREATE_DRAFT = "gmail_create_draft"
    AI_AGENT = "make_ai_agent"
    ROUTER = "builtin_router"
    WEBHOOK = "webhook_custom_webhook"
    MYSQL_SELECT = "mysql_select_rows"
    MYSQL_INSERT = "mysql_insert_row"
    MYSQL_TRANSACTION = "mysql_execute_query"
    EXCEL_WATCH = "microsoft365_excel_watch_workbooks"
    EXCEL_UPDATE = "microsoft365_excel_update_row"
    HTTP_AGENT = "http_agent_make_request"
    ERROR_HANDLER = "builtin_ignore"
    DATA_STORE = "builtin_data_store"
    SCHEDULER = "builtin_schedule"

@dataclass
class ModuleConfig:
    type: ModuleType
    name: str
    parameters: Dict[str, Any]
    position: tuple
    connections: List[str] = None
    error_handlers: List[Dict] = None

class AutomationGenerator:
    def __init__(self):
        self.templates = self._load_templates()
        self.module_counter = 0
    
    def _get_next_id(self) -> int:
        """Get next module ID"""
        self.module_counter += 1
        return self.module_counter
    
    def _load_templates(self) -> Dict:
        """Load module templates for different automation types"""
        return {
            "gmail_monitoring": {
                "trigger": {
                    "type": ModuleType.GMAIL_WATCH,
                    "config": {
                        "connection": "gmail_connection",
                        "folder": "INBOX",
                        "filter": "is:unread",
                        "max_results": 10,
                        "mark_as_read": False
                    }
                },
                "ai_processing": {
                    "type": ModuleType.AI_AGENT,
                    "config": {
                        "agent_name": "Email_Processor_Agent",
                        "system_prompt": "You are an email processing agent that categorizes emails and determines appropriate actions.",
                        "max_tokens": 500,
                        "temperature": 0.3
                    }
                }
            },
            "database_sync": {
                "trigger": {
                    "type": ModuleType.SCHEDULER,
                    "config": {
                        "schedule_type": "interval",
                        "interval": 3600,
                        "timezone": "UTC"
                    }
                },
                "database": {
                    "type": ModuleType.MYSQL_SELECT,
                    "config": {
                        "connection": "mysql_connection",
                        "table": "data_table",
                        "limit": 1000
                    }
                }
            },
            "excel_processing": {
                "trigger": {
                    "type": ModuleType.EXCEL_WATCH,
                    "config": {
                        "connection": "excel_connection",
                        "filter_modified": "last_24_hours",
                        "limit": 10
                    }
                }
            }
        }
    
    def generate_automation(self, description: str) -> Dict[str, Any]:
        """Generate complete Make.com automation from description"""
        # Parse the description to understand requirements
        requirements = self._parse_description(description)
        
        # Generate scenario structure
        scenario = {
            "name": self._generate_scenario_name(requirements),
            "description": description,
            "modules": [],
            "connections": [],
            "error_handling": "comprehensive",
            "testing": True
        }
        
        # Build module chain based on requirements
        modules = self._build_module_chain(requirements)
        scenario["modules"] = modules
        scenario["connections"] = self._generate_connections(requirements)
        
        # Add error handling
        self._add_error_handling(scenario)
        
        return scenario
    
    def _parse_description(self, description: str) -> Dict[str, Any]:
        """Parse natural language description into structured requirements"""
        requirements = {
            "triggers": [],
            "data_sources": [],
            "processing": [],
            "outputs": [],
            "ai_needed": False,
            "database_ops": [],
            "error_handling": "basic"
        }
        
        # Detect triggers
        if "email" in description.lower() or "gmail" in description.lower():
            requirements["triggers"].append("gmail")
        if "schedule" in description.lower() or "every" in description.lower():
            requirements["triggers"].append("schedule")
        if "webhook" in description.lower() or "api" in description.lower():
            requirements["triggers"].append("webhook")
        if "excel" in description.lower() or "spreadsheet" in description.lower():
            requirements["triggers"].append("excel")
        
        # Detect AI processing needs
        ai_keywords = ["analyze", "categorize", "generate", "classify", "process", "understand"]
        if any(keyword in description.lower() for keyword in ai_keywords):
            requirements["ai_needed"] = True
        
        # Detect database operations
        db_keywords = ["database", "mysql", "store", "save", "update", "insert"]
        if any(keyword in description.lower() for keyword in db_keywords):
            requirements["database_ops"].append("mysql")
        
        # Detect outputs
        if "reply" in description.lower() or "respond" in description.lower():
            requirements["outputs"].append("email_reply")
        if "slack" in description.lower():
            requirements["outputs"].append("slack")
        if "ticket" in description.lower():
            requirements["outputs"].append("ticket_system")
        if "report" in description.lower():
            requirements["outputs"].append("report")
        
        return requirements
    
    def _build_module_chain(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build the chain of modules based on requirements"""
        modules = []
        
        # Add trigger modules
        if "gmail" in requirements["triggers"]:
            modules.append(self._create_gmail_watch_module())
        elif "schedule" in requirements["triggers"]:
            modules.append(self._create_scheduler_module())
        elif "webhook" in requirements["triggers"]:
            modules.append(self._create_webhook_module())
        elif "excel" in requirements["triggers"]:
            modules.append(self._create_excel_watch_module())
        
        # Add AI processing if needed
        if requirements["ai_needed"]:
            modules.append(self._create_ai_agent_module(requirements))
        
        # Add router for conditional logic
        if len(requirements["outputs"]) > 1:
            modules.append(self._create_router_module(requirements))
        
        # Add database operations
        if "mysql" in requirements["database_ops"]:
            modules.append(self._create_mysql_module())
        
        # Add output modules
        for output in requirements["outputs"]:
            if output == "email_reply":
                modules.append(self._create_gmail_send_module())
            elif output == "slack":
                modules.append(self._create_slack_module())
            elif output == "report":
                modules.append(self._create_excel_update_module())
        
        # Add logging
        modules.append(self._create_data_store_module())
        
        return modules
    
    def _create_gmail_watch_module(self) -> Dict[str, Any]:
        """Create Gmail watch emails module"""
        return {
            "id": self._get_next_id(),
            "module": "gmail",
            "version": 1,
            "parameters": {
                "watch": "emails",
                "connection": "{{gmail_connection}}",
                "folder": "INBOX",
                "filter": "is:unread -label:processed",
                "maxResults": 10,
                "markAsRead": False
            },
            "mapper": {},
            "metadata": {
                "designer": {
                    "x": 0,
                    "y": 0
                },
                "restore": {
                    "parameters": {
                        "folder": {"label": "INBOX"},
                        "watch": {"label": "Emails"}
                    }
                },
                "expect": [
                    {
                        "name": "id",
                        "type": "text",
                        "label": "Message ID"
                    },
                    {
                        "name": "threadId",
                        "type": "text",
                        "label": "Thread ID"
                    },
                    {
                        "name": "subject",
                        "type": "text",
                        "label": "Subject"
                    },
                    {
                        "name": "from",
                        "type": "text",
                        "label": "From"
                    },
                    {
                        "name": "body",
                        "type": "text",
                        "label": "Body"
                    }
                ]
            }
        }
    
    def _create_ai_agent_module(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create AI agent module with appropriate prompt"""
        prompt = self._generate_ai_prompt(requirements)
        
        return {
            "id": self._get_next_id(),
            "module": "make-ai-agents",
            "version": 1,
            "parameters": {
                "agent": "{{ai_agent_connection}}",
                "messages": [
                    {
                        "role": "user",
                        "content": "{{1.subject}}\n\n{{1.body}}"
                    }
                ],
                "threadId": "{{1.threadId}}",
                "timeout": 300
            },
            "mapper": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Process this email:\nFrom: {{1.from}}\nSubject: {{1.subject}}\nBody: {{1.body}}\n\nAnalyze and determine appropriate action."
                    }
                ]
            },
            "metadata": {
                "designer": {
                    "x": 300,
                    "y": 0
                },
                "expect": [
                    {
                        "name": "response",
                        "type": "text",
                        "label": "AI Response"
                    },
                    {
                        "name": "category",
                        "type": "text",
                        "label": "Category"
                    },
                    {
                        "name": "action",
                        "type": "text",
                        "label": "Recommended Action"
                    }
                ]
            }
        }
    
    def _create_router_module(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create router module for conditional logic"""
        routes = []
        
        for i, output in enumerate(requirements["outputs"]):
            routes.append({
                "label": output.replace("_", " ").title(),
                "condition": f"{{{{2.category}}}} = \"{output}\"",
                "index": i + 1
            })
        
        return {
            "id": self._get_next_id(),
            "module": "builtin:router",
            "version": 1,
            "parameters": {},
            "mapper": {
                "routes": routes
            },
            "metadata": {
                "designer": {
                    "x": 600,
                    "y": 0
                }
            }
        }
    
    def _create_gmail_send_module(self) -> Dict[str, Any]:
        """Create Gmail send email module"""
        return {
            "id": self._get_next_id(),
            "module": "gmail",
            "version": 1,
            "parameters": {
                "sendEmail": True,
                "connection": "{{gmail_connection}}",
                "to": "{{1.from}}",
                "subject": "Re: {{1.subject}}",
                "content": "{{2.response}}",
                "contentType": "text/html"
            },
            "mapper": {},
            "metadata": {
                "designer": {
                    "x": 900,
                    "y": 0
                }
            }
        }
    
    def _create_scheduler_module(self) -> Dict[str, Any]:
        """Create scheduler module"""
        return {
            "id": self._get_next_id(),
            "module": "builtin:schedule",
            "version": 1,
            "parameters": {
                "schedule": "*/30 * * * *"  # Every 30 minutes
            },
            "metadata": {
                "designer": {
                    "x": 0,
                    "y": 0
                }
            }
        }
    
    def _create_webhook_module(self) -> Dict[str, Any]:
        """Create webhook module"""
        return {
            "id": self._get_next_id(),
            "module": "webhook",
            "version": 1,
            "parameters": {
                "hook": str(uuid.uuid4()),
                "restrictionType": "whitelist",
                "restrictionValue": ""
            },
            "metadata": {
                "designer": {
                    "x": 0,
                    "y": 0
                }
            }
        }
    
    def _create_mysql_module(self) -> Dict[str, Any]:
        """Create MySQL module"""
        return {
            "id": self._get_next_id(),
            "module": "mysql",
            "version": 1,
            "parameters": {
                "connection": "{{mysql_connection}}",
                "table": "automation_logs",
                "action": "insert"
            },
            "mapper": {
                "data": {
                    "timestamp": "{{now}}",
                    "email_id": "{{1.id}}",
                    "action_taken": "{{2.action}}",
                    "status": "completed"
                }
            },
            "metadata": {
                "designer": {
                    "x": 1200,
                    "y": 0
                }
            }
        }
    
    def _create_excel_watch_module(self) -> Dict[str, Any]:
        """Create Excel watch module"""
        return {
            "id": self._get_next_id(),
            "module": "microsoft365-excel",
            "version": 1,
            "parameters": {
                "connection": "{{excel_connection}}",
                "watch": "workbooks",
                "limit": 10
            },
            "metadata": {
                "designer": {
                    "x": 0,
                    "y": 0
                }
            }
        }
    
    def _create_excel_update_module(self) -> Dict[str, Any]:
        """Create Excel update module"""
        return {
            "id": self._get_next_id(),
            "module": "microsoft365-excel",
            "version": 1,
            "parameters": {
                "connection": "{{excel_connection}}",
                "action": "addWorksheet",
                "name": "AI_Report_{{formatDate(now, 'YYYY-MM-DD')}}"
            },
            "metadata": {
                "designer": {
                    "x": 900,
                    "y": 100
                }
            }
        }
    
    def _create_slack_module(self) -> Dict[str, Any]:
        """Create Slack module"""
        return {
            "id": self._get_next_id(),
            "module": "slack",
            "version": 1,
            "parameters": {
                "connection": "{{slack_connection}}",
                "channel": "#alerts",
                "text": "{{2.response}}"
            },
            "metadata": {
                "designer": {
                    "x": 900,
                    "y": -100
                }
            }
        }
    
    def _create_data_store_module(self) -> Dict[str, Any]:
        """Create data store logging module"""
        return {
            "id": self._get_next_id(),
            "module": "builtin:datastore",
            "version": 1,
            "parameters": {
                "action": "add",
                "dataStructure": "automation_log"
            },
            "mapper": {
                "data": {
                    "timestamp": "{{now}}",
                    "scenario_id": "{{scenario.id}}",
                    "execution_id": "{{execution.id}}",
                    "status": "success",
                    "details": "{{json(bundle)}}"
                }
            },
            "metadata": {
                "designer": {
                    "x": 1500,
                    "y": 0
                }
            }
        }
    
    def _generate_ai_prompt(self, requirements: Dict[str, Any]) -> str:
        """Generate appropriate AI prompt based on requirements"""
        base_prompt = "You are an intelligent automation assistant. "
        
        if "gmail" in requirements["triggers"]:
            base_prompt += "Analyze emails and determine appropriate actions. "
        
        if "mysql" in requirements["database_ops"]:
            base_prompt += "Process data for database operations. "
        
        base_prompt += """
        Respond in JSON format with:
        {
            "category": "urgent|normal|spam|info",
            "action": "reply|escalate|archive|process",
            "response": "generated response text",
            "confidence": 0.0-1.0
        }
        """
        
        return base_prompt.strip()
    
    def _generate_connections(self, requirements: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate required connections"""
        connections = []
        
        if "gmail" in requirements["triggers"] or "email_reply" in requirements["outputs"]:
            connections.append({
                "name": "gmail_connection",
                "type": "gmail",
                "description": "Gmail API connection for email operations"
            })
        
        if requirements["ai_needed"]:
            connections.append({
                "name": "ai_agent_connection",
                "type": "make-ai-agents",
                "description": "AI agent for processing and analysis"
            })
        
        if "mysql" in requirements["database_ops"]:
            connections.append({
                "name": "mysql_connection",
                "type": "mysql",
                "description": "MySQL database connection"
            })
        
        if "excel" in requirements["triggers"] or "report" in requirements["outputs"]:
            connections.append({
                "name": "excel_connection",
                "type": "microsoft365-excel",
                "description": "Excel/Microsoft 365 connection"
            })
        
        if "slack" in requirements["outputs"]:
            connections.append({
                "name": "slack_connection",
                "type": "slack",
                "description": "Slack workspace connection"
            })
        
        return connections
    
    def _add_error_handling(self, scenario: Dict[str, Any]) -> None:
        """Add comprehensive error handling to all modules"""
        for module in scenario["modules"]:
            if "metadata" not in module:
                module["metadata"] = {}
            
            module["metadata"]["errorHandlers"] = [
                {
                    "type": "ignore",
                    "resume": True,
                    "retryAttempts": 3,
                    "retryInterval": 60
                }
            ]
    
    def _generate_scenario_name(self, requirements: Dict[str, Any]) -> str:
        """Generate descriptive scenario name"""
        name_parts = []
        
        if "gmail" in requirements["triggers"]:
            name_parts.append("Gmail")
        if "excel" in requirements["triggers"]:
            name_parts.append("Excel")
        if requirements["ai_needed"]:
            name_parts.append("AI")
        if "mysql" in requirements["database_ops"]:
            name_parts.append("Database")
        
        name_parts.append("Automation")
        return "_".join(name_parts)
    
    def export_to_make_blueprint(self, scenario: Dict[str, Any]) -> str:
        """Export scenario as Make.com blueprint JSON"""
        blueprint = {
            "name": scenario["name"],
            "flow": scenario["modules"],
            "metadata": {
                "version": 1,
                "scenario": scenario["name"],
                "designer": {
                    "orphaned": False
                },
                "zone": "us1.make.com"
            }
        }
        
        return json.dumps(blueprint, indent=2)

def main():
    """Main function to demonstrate usage"""
    generator = AutomationGenerator()
    
    # Example usage
    description = "Monitor support emails in Gmail, use AI to categorize them, auto-reply to simple questions, and create tickets for complex issues in our MySQL database"
    
    automation = generator.generate_automation(description)
    blueprint = generator.export_to_make_blueprint(automation)
    
    print("Generated Make.com Automation:")
    print("=" * 50)
    print(f"Name: {automation['name']}")
    print(f"Description: {automation['description']}")
    print(f"Modules: {len(automation['modules'])}")
    print(f"Connections needed: {len(automation['connections'])}")
    
    print("\nMake.com Blueprint (copy to Make.com):")
    print("=" * 50)
    print(blueprint)
    
    print("\nConnections to configure:")
    print("=" * 30)
    for conn in automation['connections']:
        print(f"- {conn['name']}: {conn['description']}")

if __name__ == "__main__":
    main()