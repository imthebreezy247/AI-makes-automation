#!/usr/bin/env python3
"""
Make.com Schema Generator
Generates and validates JSON schemas for Make.com module configurations
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ModuleSchema:
    """Schema definitions for Make.com modules"""
    
    @staticmethod
    def base_module_schema() -> Dict[str, Any]:
        """Base schema for all Make.com modules"""
        return {
            "type": "object",
            "required": ["id", "module", "version"],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Unique module identifier",
                    "minimum": 1
                },
                "module": {
                    "type": "string",
                    "description": "Module type identifier",
                    "pattern": "^[a-zA-Z0-9-_:]+$"
                },
                "version": {
                    "type": "integer",
                    "description": "Module version",
                    "minimum": 1
                },
                "parameters": {
                    "type": "object",
                    "description": "Module-specific parameters"
                },
                "mapper": {
                    "type": "object",
                    "description": "Data mapping configuration"
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "designer": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"}
                            },
                            "required": ["x", "y"]
                        },
                        "restore": {
                            "type": "object",
                            "description": "UI restoration data"
                        },
                        "expect": {
                            "type": "array",
                            "description": "Expected output fields",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "label": {"type": "string"}
                                },
                                "required": ["name", "type"]
                            }
                        },
                        "errorHandlers": {
                            "type": "array",
                            "description": "Error handling configuration",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["ignore", "resume", "commit", "rollback", "break"]
                                    },
                                    "resume": {"type": "boolean"},
                                    "retryAttempts": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "retryInterval": {"type": "integer", "minimum": 1}
                                },
                                "required": ["type"]
                            }
                        }
                    }
                },
                "filter": {
                    "type": "object",
                    "properties": {
                        "condition": {
                            "type": "string",
                            "description": "Filter condition using Make.com syntax"
                        }
                    }
                }
            },
            "additionalProperties": False
        }
    
    @staticmethod
    def gmail_watch_schema() -> Dict[str, Any]:
        """Schema for Gmail watch emails module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "watch": {
                "type": "string",
                "enum": ["emails"],
                "description": "What to watch for"
            },
            "connection": {
                "type": "string",
                "description": "Gmail connection identifier",
                "pattern": "^{{.*}}$"
            },
            "folder": {
                "type": "string",
                "description": "Gmail folder/label to watch",
                "default": "INBOX"
            },
            "filter": {
                "type": "string",
                "description": "Gmail search filter",
                "examples": ["is:unread", "from:example@domain.com", "has:attachment"]
            },
            "maxResults": {
                "type": "integer",
                "description": "Maximum emails to process",
                "minimum": 1,
                "maximum": 100,
                "default": 10
            },
            "markAsRead": {
                "type": "boolean",
                "description": "Mark emails as read after processing",
                "default": False
            }
        }
        base["properties"]["parameters"]["required"] = ["watch", "connection"]
        return base
    
    @staticmethod
    def gmail_send_schema() -> Dict[str, Any]:
        """Schema for Gmail send email module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "sendEmail": {
                "type": "boolean",
                "const": True
            },
            "connection": {
                "type": "string",
                "pattern": "^{{.*}}$"
            },
            "to": {
                "type": "string",
                "description": "Recipient email address"
            },
            "cc": {
                "type": "string",
                "description": "CC recipients"
            },
            "bcc": {
                "type": "string", 
                "description": "BCC recipients"
            },
            "subject": {
                "type": "string",
                "description": "Email subject"
            },
            "content": {
                "type": "string",
                "description": "Email body content"
            },
            "contentType": {
                "type": "string",
                "enum": ["text/plain", "text/html"],
                "default": "text/html"
            },
            "attachments": {
                "type": "array",
                "description": "Email attachments",
                "items": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "data": {"type": "string"},
                        "contentType": {"type": "string"}
                    }
                }
            }
        }
        base["properties"]["parameters"]["required"] = ["sendEmail", "connection", "to", "subject", "content"]
        return base
    
    @staticmethod
    def ai_agent_schema() -> Dict[str, Any]:
        """Schema for AI Agent module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "agent": {
                "type": "string",
                "description": "AI agent connection",
                "pattern": "^{{.*}}$"
            },
            "messages": {
                "type": "array",
                "description": "Conversation messages",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["system", "user", "assistant"]
                        },
                        "content": {
                            "type": "string",
                            "description": "Message content"
                        }
                    },
                    "required": ["role", "content"]
                }
            },
            "threadId": {
                "type": "string",
                "description": "Thread ID for conversation continuity"
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds",
                "minimum": 30,
                "maximum": 600,
                "default": 300
            },
            "tools": {
                "type": "array",
                "description": "Available tools for the agent",
                "items": {
                    "type": "string"
                }
            }
        }
        base["properties"]["parameters"]["required"] = ["agent"]
        return base
    
    @staticmethod
    def mysql_schema() -> Dict[str, Any]:
        """Schema for MySQL module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "connection": {
                "type": "string",
                "pattern": "^{{.*}}$"
            },
            "query": {
                "type": "string",
                "description": "SQL query to execute"
            },
            "table": {
                "type": "string",
                "description": "Table name for operations"
            },
            "action": {
                "type": "string",
                "enum": ["select", "insert", "update", "delete", "query", "beginTransaction", "commit", "rollback"]
            },
            "values": {
                "type": "array",
                "description": "Parameter values for prepared statements"
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10000
            }
        }
        base["properties"]["parameters"]["required"] = ["connection"]
        return base
    
    @staticmethod
    def router_schema() -> Dict[str, Any]:
        """Schema for Router module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["mapper"]["properties"] = {
            "routes": {
                "type": "array",
                "description": "Routing conditions",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {
                            "type": "string",
                            "description": "Route label"
                        },
                        "condition": {
                            "type": "string",
                            "description": "Routing condition using Make.com syntax"
                        },
                        "index": {
                            "type": "integer",
                            "minimum": 1
                        }
                    },
                    "required": ["label", "condition"]
                },
                "minItems": 1
            }
        }
        base["properties"]["mapper"]["required"] = ["routes"]
        return base
    
    @staticmethod
    def webhook_schema() -> Dict[str, Any]:
        """Schema for Webhook module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "hook": {
                "type": "string",
                "description": "Webhook UUID",
                "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
            },
            "restrictionType": {
                "type": "string",
                "enum": ["none", "whitelist", "blacklist"],
                "default": "none"
            },
            "restrictionValue": {
                "type": "string",
                "description": "IP restriction values"
            },
            "validateJSON": {
                "type": "boolean",
                "default": True
            },
            "responseMode": {
                "type": "string",
                "enum": ["default", "custom"],
                "default": "default"
            }
        }
        return base
    
    @staticmethod
    def excel_schema() -> Dict[str, Any]:
        """Schema for Microsoft Excel module"""
        base = ModuleSchema.base_module_schema()
        base["properties"]["parameters"]["properties"] = {
            "connection": {
                "type": "string",
                "pattern": "^{{.*}}$"
            },
            "action": {
                "type": "string",
                "enum": ["watch", "listWorkbooks", "listWorksheets", "listRows", "addWorksheet", "updateRow", "addTable"]
            },
            "workbookId": {
                "type": "string",
                "description": "Excel workbook ID"
            },
            "worksheetId": {
                "type": "string",
                "description": "Excel worksheet ID"
            },
            "range": {
                "type": "string",
                "description": "Excel range (e.g., A1:Z100)",
                "pattern": "^[A-Z]+[0-9]+:[A-Z]+[0-9]+$"
            },
            "name": {
                "type": "string",
                "description": "Worksheet or table name"
            },
            "modifiedAfter": {
                "type": "string",
                "description": "Filter by modification date"
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
            }
        }
        base["properties"]["parameters"]["required"] = ["connection"]
        return base

class SchemaValidator:
    """Validates Make.com automation configurations"""
    
    def __init__(self):
        self.schemas = {
            "gmail": ModuleSchema.gmail_watch_schema(),
            "gmail_send": ModuleSchema.gmail_send_schema(),
            "make-ai-agents": ModuleSchema.ai_agent_schema(),
            "mysql": ModuleSchema.mysql_schema(),
            "builtin:router": ModuleSchema.router_schema(),
            "webhook": ModuleSchema.webhook_schema(),
            "microsoft365-excel": ModuleSchema.excel_schema()
        }
    
    def validate_module(self, module: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate a single module against its schema"""
        errors = []
        
        # Check required base fields
        if "module" not in module:
            errors.append("Missing required field: module")
            return False, errors
        
        module_type = module["module"]
        schema = self.schemas.get(module_type, ModuleSchema.base_module_schema())
        
        # Validate against schema
        validation_errors = self._validate_against_schema(module, schema)
        errors.extend(validation_errors)
        
        return len(errors) == 0, errors
    
    def validate_scenario(self, scenario: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate entire scenario"""
        errors = []
        
        # Check scenario structure
        required_fields = ["name", "flow"]
        for field in required_fields:
            if field not in scenario:
                errors.append(f"Missing required scenario field: {field}")
        
        # Validate modules
        if "flow" in scenario:
            for i, module in enumerate(scenario["flow"]):
                is_valid, module_errors = self.validate_module(module)
                if not is_valid:
                    for error in module_errors:
                        errors.append(f"Module {i+1}: {error}")
        
        # Check module ID uniqueness
        if "flow" in scenario:
            ids = [module.get("id") for module in scenario["flow"] if "id" in module]
            if len(ids) != len(set(ids)):
                errors.append("Duplicate module IDs found")
        
        return len(errors) == 0, errors
    
    def _validate_against_schema(self, data: Any, schema: Dict[str, Any], path: str = "") -> List[str]:
        """Recursively validate data against schema"""
        errors = []
        
        if schema.get("type") == "object":
            if not isinstance(data, dict):
                errors.append(f"{path}: Expected object, got {type(data).__name__}")
                return errors
            
            # Check required fields
            required = schema.get("required", [])
            for field in required:
                if field not in data:
                    errors.append(f"{path}: Missing required field '{field}'")
            
            # Check properties
            properties = schema.get("properties", {})
            for field, value in data.items():
                if field in properties:
                    field_path = f"{path}.{field}" if path else field
                    field_errors = self._validate_against_schema(value, properties[field], field_path)
                    errors.extend(field_errors)
        
        elif schema.get("type") == "array":
            if not isinstance(data, list):
                errors.append(f"{path}: Expected array, got {type(data).__name__}")
                return errors
            
            items_schema = schema.get("items")
            if items_schema:
                for i, item in enumerate(data):
                    item_path = f"{path}[{i}]"
                    item_errors = self._validate_against_schema(item, items_schema, item_path)
                    errors.extend(item_errors)
        
        elif schema.get("type") == "string":
            if not isinstance(data, str):
                errors.append(f"{path}: Expected string, got {type(data).__name__}")
            elif "enum" in schema and data not in schema["enum"]:
                errors.append(f"{path}: Value '{data}' not in allowed values: {schema['enum']}")
            elif "pattern" in schema:
                import re
                if not re.match(schema["pattern"], data):
                    errors.append(f"{path}: Value '{data}' doesn't match pattern '{schema['pattern']}'")
        
        elif schema.get("type") == "integer":
            if not isinstance(data, int):
                errors.append(f"{path}: Expected integer, got {type(data).__name__}")
            elif "minimum" in schema and data < schema["minimum"]:
                errors.append(f"{path}: Value {data} below minimum {schema['minimum']}")
            elif "maximum" in schema and data > schema["maximum"]:
                errors.append(f"{path}: Value {data} above maximum {schema['maximum']}")
        
        elif schema.get("type") == "boolean":
            if not isinstance(data, bool):
                errors.append(f"{path}: Expected boolean, got {type(data).__name__}")
        
        return errors

class SchemaGenerator:
    """Generate schemas for custom module configurations"""
    
    @staticmethod
    def generate_custom_schema(module_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate schema for custom module type"""
        base = ModuleSchema.base_module_schema()
        
        # Infer parameter types
        parameter_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param, value in parameters.items():
            param_schema = SchemaGenerator._infer_type_schema(value)
            parameter_schema["properties"][param] = param_schema
        
        base["properties"]["parameters"] = parameter_schema
        return base
    
    @staticmethod
    def _infer_type_schema(value: Any) -> Dict[str, Any]:
        """Infer JSON schema from value"""
        if isinstance(value, str):
            schema = {"type": "string"}
            if value.startswith("{{") and value.endswith("}}"):
                schema["description"] = "Make.com variable mapping"
                schema["pattern"] = "^{{.*}}$"
            return schema
        elif isinstance(value, int):
            return {"type": "integer"}
        elif isinstance(value, float):
            return {"type": "number"}
        elif isinstance(value, bool):
            return {"type": "boolean"}
        elif isinstance(value, list):
            if value:
                item_schema = SchemaGenerator._infer_type_schema(value[0])
                return {"type": "array", "items": item_schema}
            else:
                return {"type": "array"}
        elif isinstance(value, dict):
            properties = {}
            for k, v in value.items():
                properties[k] = SchemaGenerator._infer_type_schema(v)
            return {"type": "object", "properties": properties}
        else:
            return {"type": "string", "description": "Unknown type"}

def main():
    """Demonstrate schema validation"""
    validator = SchemaValidator()
    
    # Test Gmail module
    gmail_module = {
        "id": 1,
        "module": "gmail",
        "version": 1,
        "parameters": {
            "watch": "emails",
            "connection": "{{gmail_connection}}",
            "folder": "INBOX",
            "maxResults": 10
        },
        "metadata": {
            "designer": {"x": 0, "y": 0}
        }
    }
    
    is_valid, errors = validator.validate_module(gmail_module)
    print(f"Gmail Module Valid: {is_valid}")
    if errors:
        for error in errors:
            print(f"  Error: {error}")
    
    # Test scenario
    scenario = {
        "name": "Test Scenario",
        "flow": [gmail_module],
        "metadata": {
            "version": 1
        }
    }
    
    is_valid, errors = validator.validate_scenario(scenario)
    print(f"\nScenario Valid: {is_valid}")
    if errors:
        for error in errors:
            print(f"  Error: {error}")
    
    # Generate schema for custom module
    custom_params = {
        "api_key": "{{secret_key}}",
        "timeout": 30,
        "retry": True,
        "endpoints": ["api1", "api2"]
    }
    
    schema = SchemaGenerator.generate_custom_schema("custom-api", custom_params)
    print(f"\nGenerated Schema for custom-api:")
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    main()