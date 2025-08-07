#!/usr/bin/env python3
"""
Make.com Automation Templates
Pre-built templates for common automation patterns
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass

class AutomationTemplates:
    """Collection of pre-built automation templates"""
    
    @staticmethod
    def gmail_customer_support() -> Dict[str, Any]:
        """Complete Gmail customer support automation"""
        return {
            "name": "Gmail_Customer_Support_Automation",
            "description": "Monitor support emails, classify with AI, auto-respond to FAQs, create tickets for complex issues",
            "blueprint": {
                "name": "Gmail Customer Support AI",
                "flow": [
                    {
                        "id": 1,
                        "module": "gmail",
                        "version": 1,
                        "parameters": {
                            "watch": "emails",
                            "connection": "{{gmail_connection}}",
                            "folder": "INBOX",
                            "filter": "to:support@company.com is:unread -label:processed",
                            "maxResults": 20,
                            "markAsRead": False
                        },
                        "mapper": {},
                        "metadata": {
                            "designer": {"x": 0, "y": 0},
                            "restore": {
                                "parameters": {
                                    "folder": {"label": "INBOX"},
                                    "watch": {"label": "Emails"}
                                }
                            }
                        }
                    },
                    {
                        "id": 2,
                        "module": "make-ai-agents",
                        "version": 1,
                        "parameters": {
                            "agent": "{{support_ai_agent}}",
                            "messages": [],
                            "threadId": "{{1.threadId}}",
                            "timeout": 300
                        },
                        "mapper": {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": "Analyze this customer support email:\n\nFrom: {{1.from}}\nSubject: {{1.subject}}\nBody: {{substring(1.body; 0; 2000)}}\n\nClassify as:\n1. FAQ (can auto-respond)\n2. Bug Report (needs developer)\n3. Feature Request (needs product team)\n4. Billing Issue (needs billing team)\n5. Spam (ignore)\n\nProvide JSON response with category, confidence, and draft response if FAQ."
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 300, "y": 0}
                        }
                    },
                    {
                        "id": 3,
                        "module": "builtin:router",
                        "version": 1,
                        "parameters": {},
                        "mapper": {
                            "routes": [
                                {
                                    "label": "FAQ - Auto Reply",
                                    "condition": "{{contains(2.response; \"FAQ\")}}"
                                },
                                {
                                    "label": "Create Ticket",
                                    "condition": "{{or(contains(2.response; \"Bug\"); contains(2.response; \"Feature\"); contains(2.response; \"Billing\"))}}"
                                },
                                {
                                    "label": "Spam",
                                    "condition": "{{contains(2.response; \"Spam\")}}"
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 600, "y": 0}
                        }
                    },
                    {
                        "id": 4,
                        "module": "gmail",
                        "version": 1,
                        "parameters": {
                            "sendEmail": True,
                            "connection": "{{gmail_connection}}",
                            "to": "{{1.from}}",
                            "subject": "Re: {{1.subject}}",
                            "content": "{{parseJSON(2.response).draft_response}}",
                            "contentType": "text/html"
                        },
                        "filter": {
                            "condition": "{{3.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 900, "y": -100}
                        }
                    },
                    {
                        "id": 5,
                        "module": "mysql",
                        "version": 1,
                        "parameters": {
                            "connection": "{{mysql_connection}}",
                            "query": "INSERT INTO support_tickets (email_id, customer_email, subject, category, priority, status, created_at) VALUES (?, ?, ?, ?, ?, 'open', NOW())"
                        },
                        "mapper": {
                            "values": [
                                "{{1.id}}",
                                "{{1.from}}",
                                "{{1.subject}}",
                                "{{parseJSON(2.response).category}}",
                                "{{if(contains(parseJSON(2.response).category; 'Bug'); 'high'; 'normal')}}"
                            ]
                        },
                        "filter": {
                            "condition": "{{3.routeIndex = 2}}"
                        },
                        "metadata": {
                            "designer": {"x": 900, "y": 0}
                        }
                    },
                    {
                        "id": 6,
                        "module": "gmail",
                        "version": 1,
                        "parameters": {
                            "modifyLabels": True,
                            "connection": "{{gmail_connection}}",
                            "messageId": "{{1.id}}",
                            "addLabelIds": ["SPAM"],
                            "removeLabelIds": ["INBOX"]
                        },
                        "filter": {
                            "condition": "{{3.routeIndex = 3}}"
                        },
                        "metadata": {
                            "designer": {"x": 900, "y": 100}
                        }
                    },
                    {
                        "id": 7,
                        "module": "gmail",
                        "version": 1,
                        "parameters": {
                            "modifyLabels": True,
                            "connection": "{{gmail_connection}}",
                            "messageId": "{{1.id}}",
                            "addLabelIds": ["processed"]
                        },
                        "metadata": {
                            "designer": {"x": 1200, "y": 0}
                        }
                    }
                ],
                "metadata": {
                    "version": 1,
                    "scenario": "Gmail Customer Support AI",
                    "designer": {"orphaned": False}
                }
            },
            "ai_agent_config": {
                "name": "Support_Email_Classifier",
                "system_prompt": """You are a customer support email classifier. Analyze emails and categorize them accurately.

Categories:
- FAQ: Common questions with standard responses
- Bug Report: Technical issues that need development team
- Feature Request: New feature suggestions for product team  
- Billing Issue: Payment, subscription, or billing questions
- Spam: Irrelevant or promotional content

For FAQ emails, provide a helpful response. For others, classify only.

Response format (JSON):
{
  "category": "FAQ|Bug Report|Feature Request|Billing Issue|Spam",
  "confidence": 0.0-1.0,
  "draft_response": "response text for FAQ only",
  "urgency": "low|normal|high"
}""",
                "max_tokens": 1000,
                "temperature": 0.3
            },
            "connections": [
                {
                    "name": "gmail_connection",
                    "type": "gmail",
                    "scopes": ["https://www.googleapis.com/auth/gmail.modify"]
                },
                {
                    "name": "support_ai_agent",
                    "type": "make-ai-agents",
                    "model": "gpt-4o-mini"
                },
                {
                    "name": "mysql_connection",
                    "type": "mysql",
                    "database": "support_system"
                }
            ]
        }
    
    @staticmethod
    def excel_mysql_sync() -> Dict[str, Any]:
        """Excel to MySQL data synchronization"""
        return {
            "name": "Excel_MySQL_Data_Sync",
            "description": "Watch Excel workbooks for changes and sync data to MySQL with AI validation",
            "blueprint": {
                "name": "Excel MySQL Sync with AI Validation",
                "flow": [
                    {
                        "id": 1,
                        "module": "builtin:schedule",
                        "version": 1,
                        "parameters": {
                            "schedule": "0 */1 * * *"  # Every hour
                        },
                        "metadata": {
                            "designer": {"x": 0, "y": 0}
                        }
                    },
                    {
                        "id": 2,
                        "module": "microsoft365-excel",
                        "version": 1,
                        "parameters": {
                            "connection": "{{excel_connection}}",
                            "watch": "workbooks",
                            "modifiedAfter": "{{addHours(now; -1)}}"
                        },
                        "metadata": {
                            "designer": {"x": 300, "y": 0}
                        }
                    },
                    {
                        "id": 3,
                        "module": "microsoft365-excel",
                        "version": 1,
                        "parameters": {
                            "connection": "{{excel_connection}}",
                            "workbookId": "{{2.id}}",
                            "action": "listWorksheets"
                        },
                        "metadata": {
                            "designer": {"x": 600, "y": 0}
                        }
                    },
                    {
                        "id": 4,
                        "module": "builtin:iterator",
                        "version": 1,
                        "parameters": {
                            "array": "{{3.worksheets}}"
                        },
                        "metadata": {
                            "designer": {"x": 900, "y": 0}
                        }
                    },
                    {
                        "id": 5,
                        "module": "microsoft365-excel",
                        "version": 1,
                        "parameters": {
                            "connection": "{{excel_connection}}",
                            "workbookId": "{{2.id}}",
                            "worksheetId": "{{4.id}}",
                            "action": "listRows",
                            "range": "A1:Z1000"
                        },
                        "metadata": {
                            "designer": {"x": 1200, "y": 0}
                        }
                    },
                    {
                        "id": 6,
                        "module": "make-ai-agents",
                        "version": 1,
                        "parameters": {
                            "agent": "{{data_validator_agent}}",
                            "timeout": 300
                        },
                        "mapper": {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": "Validate this Excel data for database import:\n\nWorksheet: {{4.name}}\nData: {{json(5.values)}}\n\nCheck for:\n1. Data completeness\n2. Format consistency\n3. Required fields\n4. Duplicate detection\n\nReturn JSON with validation results and cleaned data."
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 1500, "y": 0}
                        }
                    },
                    {
                        "id": 7,
                        "module": "builtin:router",
                        "version": 1,
                        "mapper": {
                            "routes": [
                                {
                                    "label": "Valid Data",
                                    "condition": "{{parseJSON(6.response).valid = true}}"
                                },
                                {
                                    "label": "Invalid Data",
                                    "condition": "{{parseJSON(6.response).valid = false}}"
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 1800, "y": 0}
                        }
                    },
                    {
                        "id": 8,
                        "module": "mysql",
                        "version": 1,
                        "parameters": {
                            "connection": "{{mysql_connection}}",
                            "action": "beginTransaction"
                        },
                        "filter": {
                            "condition": "{{7.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 2100, "y": -100}
                        }
                    },
                    {
                        "id": 9,
                        "module": "builtin:iterator",
                        "version": 1,
                        "parameters": {
                            "array": "{{parseJSON(6.response).cleaned_data}}"
                        },
                        "filter": {
                            "condition": "{{7.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 2400, "y": -100}
                        }
                    },
                    {
                        "id": 10,
                        "module": "mysql",
                        "version": 1,
                        "parameters": {
                            "connection": "{{mysql_connection}}",
                            "query": "INSERT INTO excel_data (worksheet_name, row_data, imported_at, source_file) VALUES (?, ?, NOW(), ?) ON DUPLICATE KEY UPDATE row_data = VALUES(row_data), updated_at = NOW()"
                        },
                        "mapper": {
                            "values": [
                                "{{4.name}}",
                                "{{json(9.value)}}",
                                "{{2.name}}"
                            ]
                        },
                        "filter": {
                            "condition": "{{7.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 2700, "y": -100}
                        }
                    },
                    {
                        "id": 11,
                        "module": "mysql",
                        "version": 1,
                        "parameters": {
                            "connection": "{{mysql_connection}}",
                            "action": "commit"
                        },
                        "filter": {
                            "condition": "{{7.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 3000, "y": -100}
                        }
                    },
                    {
                        "id": 12,
                        "module": "builtin:datastore",
                        "version": 1,
                        "parameters": {
                            "action": "add",
                            "dataStructure": "error_log"
                        },
                        "mapper": {
                            "data": {
                                "timestamp": "{{now}}",
                                "error_type": "data_validation",
                                "details": "{{parseJSON(6.response).errors}}",
                                "source": "{{2.name}} - {{4.name}}"
                            }
                        },
                        "filter": {
                            "condition": "{{7.routeIndex = 2}}"
                        },
                        "metadata": {
                            "designer": {"x": 2100, "y": 100}
                        }
                    }
                ]
            },
            "ai_agent_config": {
                "name": "Excel_Data_Validator",
                "system_prompt": """You are a data validation specialist for Excel-to-Database imports.

Validate data for:
1. Required fields present
2. Data types match expected formats  
3. No duplicate records
4. Proper formatting (dates, numbers, emails)
5. Business logic compliance

Response format (JSON):
{
  "valid": true/false,
  "errors": ["list of validation errors"],
  "warnings": ["list of warnings"],
  "cleaned_data": [cleaned/normalized data array],
  "summary": "validation summary"
}""",
                "max_tokens": 2000,
                "temperature": 0.1
            }
        }
    
    @staticmethod
    def http_api_orchestrator() -> Dict[str, Any]:
        """HTTP API data orchestrator for enterprise systems"""
        return {
            "name": "Enterprise_API_Orchestrator",
            "description": "Fetch data from internal APIs, process with AI, and distribute to multiple systems",
            "blueprint": {
                "name": "Enterprise API Data Orchestrator",
                "flow": [
                    {
                        "id": 1,
                        "module": "builtin:schedule",
                        "version": 1,
                        "parameters": {
                            "schedule": "*/15 * * * *"  # Every 15 minutes
                        },
                        "metadata": {
                            "designer": {"x": 0, "y": 0}
                        }
                    },
                    {
                        "id": 2,
                        "module": "http",
                        "version": 3,
                        "parameters": {
                            "url": "https://internal-api.company.com/data/latest",
                            "method": "GET",
                            "headers": [
                                {
                                    "name": "Authorization",
                                    "value": "Bearer {{api_token}}"
                                },
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "timeout": 30
                        },
                        "metadata": {
                            "designer": {"x": 300, "y": 0}
                        }
                    },
                    {
                        "id": 3,
                        "module": "make-ai-agents",
                        "version": 1,
                        "parameters": {
                            "agent": "{{api_data_processor}}",
                            "timeout": 300
                        },
                        "mapper": {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": "Process this API response data:\n\n{{2.data}}\n\nAnalyze for:\n1. Data quality issues\n2. Anomalies or outliers\n3. Trends and patterns\n4. Required actions\n5. Distribution routing\n\nProvide structured analysis and routing decisions."
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 600, "y": 0}
                        }
                    },
                    {
                        "id": 4,
                        "module": "builtin:router",
                        "version": 1,
                        "mapper": {
                            "routes": [
                                {
                                    "label": "Database Update",
                                    "condition": "{{contains(3.response; 'database')}}"
                                },
                                {
                                    "label": "Alert Required",
                                    "condition": "{{contains(3.response; 'alert')}}"
                                },
                                {
                                    "label": "Report Generation",
                                    "condition": "{{contains(3.response; 'report')}}"
                                }
                            ]
                        },
                        "metadata": {
                            "designer": {"x": 900, "y": 0}
                        }
                    },
                    {
                        "id": 5,
                        "module": "mysql",
                        "version": 1,
                        "parameters": {
                            "connection": "{{mysql_connection}}",
                            "query": "CALL process_api_data(?)"
                        },
                        "mapper": {
                            "values": ["{{json(2.data)}}"]
                        },
                        "filter": {
                            "condition": "{{4.routeIndex = 1}}"
                        },
                        "metadata": {
                            "designer": {"x": 1200, "y": -100}
                        }
                    },
                    {
                        "id": 6,
                        "module": "slack",
                        "version": 1,
                        "parameters": {
                            "connection": "{{slack_connection}}",
                            "channel": "#alerts",
                            "text": "🚨 API Data Alert:\n{{parseJSON(3.response).alert_message}}\n\nData: {{substring(2.data; 0; 500)}}..."
                        },
                        "filter": {
                            "condition": "{{4.routeIndex = 2}}"
                        },
                        "metadata": {
                            "designer": {"x": 1200, "y": 0}
                        }
                    },
                    {
                        "id": 7,
                        "module": "microsoft365-excel",
                        "version": 1,
                        "parameters": {
                            "connection": "{{excel_connection}}",
                            "action": "addWorksheet",
                            "name": "API_Report_{{formatDate(now; 'YYYY-MM-DD_HH-mm')}}"
                        },
                        "filter": {
                            "condition": "{{4.routeIndex = 3}}"
                        },
                        "metadata": {
                            "designer": {"x": 1200, "y": 100}
                        }
                    }
                ]
            }
        }
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Return all available templates"""
        return {
            "gmail_customer_support": AutomationTemplates.gmail_customer_support(),
            "excel_mysql_sync": AutomationTemplates.excel_mysql_sync(),
            "http_api_orchestrator": AutomationTemplates.http_api_orchestrator()
        }
    
    @staticmethod
    def get_template_by_keywords(keywords: List[str]) -> Dict[str, Any]:
        """Get template based on keywords in description"""
        templates = AutomationTemplates.get_all_templates()
        
        keyword_map = {
            "email": "gmail_customer_support",
            "gmail": "gmail_customer_support", 
            "support": "gmail_customer_support",
            "customer": "gmail_customer_support",
            "excel": "excel_mysql_sync",
            "spreadsheet": "excel_mysql_sync",
            "mysql": "excel_mysql_sync",
            "database": "excel_mysql_sync",
            "sync": "excel_mysql_sync",
            "api": "http_api_orchestrator",
            "http": "http_api_orchestrator",
            "webhook": "http_api_orchestrator",
            "enterprise": "http_api_orchestrator"
        }
        
        for keyword in keywords:
            if keyword.lower() in keyword_map:
                return templates[keyword_map[keyword.lower()]]
        
        # Default to Gmail support if no match
        return templates["gmail_customer_support"]

def main():
    """Demonstrate template usage"""
    templates = AutomationTemplates.get_all_templates()
    
    print("Available Automation Templates:")
    print("=" * 50)
    
    for name, template in templates.items():
        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"  Description: {template['description']}")
        print(f"  Modules: {len(template['blueprint']['flow'])}")
        if 'connections' in template:
            print(f"  Connections: {len(template['connections'])}")
    
    # Example: Get template for Gmail automation
    print("\n" + "="*50)
    print("Example: Gmail Customer Support Template")
    print("="*50)
    
    gmail_template = AutomationTemplates.gmail_customer_support()
    blueprint_json = json.dumps(gmail_template['blueprint'], indent=2)
    
    print("Blueprint (copy to Make.com):")
    print(blueprint_json[:1000] + "..." if len(blueprint_json) > 1000 else blueprint_json)

if __name__ == "__main__":
    main()