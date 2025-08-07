#!/usr/bin/env python3
"""
Make.com Automation Validator
Comprehensive validation and error checking for generated configurations
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from schema_generator import SchemaValidator

class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    level: ValidationLevel
    message: str
    module_id: Optional[int] = None
    field: Optional[str] = None
    suggestion: Optional[str] = None

class AutomationValidator:
    """Comprehensive validator for Make.com automations"""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.results: List[ValidationResult] = []
    
    def validate_automation(self, automation: Dict[str, Any]) -> Tuple[bool, List[ValidationResult]]:
        """Validate complete automation configuration"""
        self.results = []
        
        # Validate basic structure
        self._validate_structure(automation)
        
        # Validate modules
        if "modules" in automation:
            self._validate_modules(automation["modules"])
        
        # Validate connections
        if "connections" in automation:
            self._validate_connections(automation["connections"])
        
        # Validate flow logic
        if "modules" in automation:
            self._validate_flow_logic(automation["modules"])
        
        # Check for best practices
        self._check_best_practices(automation)
        
        # Determine if validation passed
        has_errors = any(result.level == ValidationLevel.ERROR for result in self.results)
        
        return not has_errors, self.results
    
    def _validate_structure(self, automation: Dict[str, Any]):
        """Validate basic automation structure"""
        required_fields = ["name", "modules"]
        
        for field in required_fields:
            if field not in automation:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    suggestion=f"Add '{field}' to automation configuration"
                ))
        
        # Check name format
        if "name" in automation:
            name = automation["name"]
            if not re.match(r'^[A-Za-z0-9_-]+$', name):
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Automation name '{name}' contains special characters",
                    suggestion="Use only letters, numbers, underscores, and hyphens"
                ))
            
            if len(name) > 100:
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Automation name is very long ({len(name)} characters)",
                    suggestion="Keep names under 100 characters for better readability"
                ))
    
    def _validate_modules(self, modules: List[Dict[str, Any]]):
        """Validate individual modules"""
        if not modules:
            self.results.append(ValidationResult(
                ValidationLevel.ERROR,
                "No modules defined in automation",
                suggestion="Add at least one trigger module"
            ))
            return
        
        module_ids = set()
        has_trigger = False
        
        for i, module in enumerate(modules):
            # Validate using schema
            is_valid, schema_errors = self.schema_validator.validate_module(module)
            
            for error in schema_errors:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Module {i+1}: {error}",
                    module_id=module.get("id")
                ))
            
            # Check for duplicate IDs
            if "id" in module:
                if module["id"] in module_ids:
                    self.results.append(ValidationResult(
                        ValidationLevel.ERROR,
                        f"Duplicate module ID: {module['id']}",
                        module_id=module["id"],
                        suggestion="Ensure each module has a unique ID"
                    ))
                module_ids.add(module["id"])
            
            # Check for trigger modules
            if self._is_trigger_module(module):
                has_trigger = True
            
            # Validate specific module types
            self._validate_specific_module(module, i)
        
        if not has_trigger:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "No trigger module found",
                suggestion="Add a trigger module (Gmail, Webhook, Schedule, etc.)"
            ))
    
    def _validate_specific_module(self, module: Dict[str, Any], index: int):
        """Validate specific module types"""
        module_type = module.get("module", "")
        
        if module_type == "gmail":
            self._validate_gmail_module(module, index)
        elif module_type == "make-ai-agents":
            self._validate_ai_agent_module(module, index)
        elif module_type == "mysql":
            self._validate_mysql_module(module, index)
        elif module_type == "builtin:router":
            self._validate_router_module(module, index)
        elif module_type == "webhook":
            self._validate_webhook_module(module, index)
    
    def _validate_gmail_module(self, module: Dict[str, Any], index: int):
        """Validate Gmail-specific configuration"""
        params = module.get("parameters", {})
        
        # Check filter syntax
        if "filter" in params:
            filter_str = params["filter"]
            if not self._is_valid_gmail_filter(filter_str):
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Gmail filter may be invalid: '{filter_str}'",
                    module_id=module.get("id"),
                    suggestion="Check Gmail search operators documentation"
                ))
        
        # Check rate limiting
        max_results = params.get("maxResults", 10)
        if max_results > 50:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                f"High maxResults value ({max_results}) may hit rate limits",
                module_id=module.get("id"),
                suggestion="Consider reducing maxResults to 20 or less"
            ))
    
    def _validate_ai_agent_module(self, module: Dict[str, Any], index: int):
        """Validate AI agent configuration"""
        params = module.get("parameters", {})
        
        # Check timeout
        timeout = params.get("timeout", 300)
        if timeout > 600:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                f"Very high timeout ({timeout}s) for AI agent",
                module_id=module.get("id"),
                suggestion="Consider reducing timeout to avoid long waits"
            ))
        
        # Check message structure
        messages = params.get("messages", [])
        if not messages:
            self.results.append(ValidationResult(
                ValidationLevel.INFO,
                "No pre-defined messages for AI agent",
                module_id=module.get("id"),
                suggestion="Consider adding system message for consistent behavior"
            ))
        
        # Check for proper variable mapping
        mapper = module.get("mapper", {})
        if "messages" in mapper:
            for msg in mapper["messages"]:
                content = msg.get("content", "")
                if "{{" in content and "}}" in content:
                    # Good - has variable mapping
                    pass
                else:
                    self.results.append(ValidationResult(
                        ValidationLevel.INFO,
                        "AI agent message without variable mapping",
                        module_id=module.get("id"),
                        suggestion="Use {{variable}} syntax to pass dynamic data"
                    ))
    
    def _validate_mysql_module(self, module: Dict[str, Any], index: int):
        """Validate MySQL configuration"""
        params = module.get("parameters", {})
        
        # Check for SQL injection risks
        query = params.get("query", "")
        if query and "?" not in query and any(var in query for var in ["{{", "}}"]):
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "SQL query with variables but no prepared statement",
                module_id=module.get("id"),
                suggestion="Use ? placeholders and values array for security"
            ))
        
        # Check for dangerous operations
        dangerous_keywords = ["DROP", "TRUNCATE", "DELETE FROM", "UPDATE "]
        for keyword in dangerous_keywords:
            if keyword.upper() in query.upper():
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Potentially dangerous SQL operation: {keyword}",
                    module_id=module.get("id"),
                    suggestion="Ensure proper WHERE clauses and backup strategies"
                ))
    
    def _validate_router_module(self, module: Dict[str, Any], index: int):
        """Validate router configuration"""
        mapper = module.get("mapper", {})
        routes = mapper.get("routes", [])
        
        if not routes:
            self.results.append(ValidationResult(
                ValidationLevel.ERROR,
                "Router module without routes",
                module_id=module.get("id"),
                suggestion="Add at least one route condition"
            ))
        
        # Check route conditions
        for i, route in enumerate(routes):
            condition = route.get("condition", "")
            if not condition:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Route {i+1} missing condition",
                    module_id=module.get("id"),
                    suggestion="Add condition for route logic"
                ))
    
    def _validate_webhook_module(self, module: Dict[str, Any], index: int):
        """Validate webhook configuration"""
        params = module.get("parameters", {})
        
        # Check security settings
        restriction_type = params.get("restrictionType", "none")
        if restriction_type == "none":
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Webhook without IP restrictions",
                module_id=module.get("id"),
                suggestion="Consider adding IP whitelist for security"
            ))
    
    def _validate_connections(self, connections: List[Dict[str, Any]]):
        """Validate connection configurations"""
        connection_names = set()
        
        for conn in connections:
            if "name" not in conn:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    "Connection missing name field",
                    suggestion="Add name field to connection"
                ))
                continue
            
            name = conn["name"]
            if name in connection_names:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Duplicate connection name: {name}",
                    suggestion="Ensure unique connection names"
                ))
            
            connection_names.add(name)
            
            # Check naming convention
            if not re.match(r'^[a-z_]+_connection$', name):
                self.results.append(ValidationResult(
                    ValidationLevel.INFO,
                    f"Connection name '{name}' doesn't follow convention",
                    suggestion="Use format: service_environment_connection"
                ))
    
    def _validate_flow_logic(self, modules: List[Dict[str, Any]]):
        """Validate automation flow logic"""
        # Check for unreachable modules
        trigger_modules = [m for m in modules if self._is_trigger_module(m)]
        if len(trigger_modules) > 1:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Multiple trigger modules found",
                suggestion="Consider using a single trigger or router"
            ))
        
        # Check for modules without error handling
        modules_without_handlers = []
        for module in modules:
            metadata = module.get("metadata", {})
            if "errorHandlers" not in metadata:
                modules_without_handlers.append(module.get("id", "unknown"))
        
        if modules_without_handlers:
            self.results.append(ValidationResult(
                ValidationLevel.INFO,
                f"Modules without error handlers: {modules_without_handlers}",
                suggestion="Add error handlers for robust automation"
            ))
    
    def _check_best_practices(self, automation: Dict[str, Any]):
        """Check for best practice adherence"""
        modules = automation.get("modules", [])
        
        # Check for logging/monitoring
        has_logging = any(
            m.get("module") == "builtin:datastore" for m in modules
        )
        
        if not has_logging:
            self.results.append(ValidationResult(
                ValidationLevel.INFO,
                "No logging module found",
                suggestion="Add data store module for execution logging"
            ))
        
        # Check for reasonable module count
        if len(modules) > 20:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                f"Large number of modules ({len(modules)})",
                suggestion="Consider breaking into smaller scenarios"
            ))
        
        # Check for AI token optimization
        ai_modules = [m for m in modules if m.get("module") == "make-ai-agents"]
        if len(ai_modules) > 3:
            self.results.append(ValidationResult(
                ValidationLevel.INFO,
                f"Multiple AI modules ({len(ai_modules)}) may increase costs",
                suggestion="Consider consolidating AI processing"
            ))
    
    def _is_trigger_module(self, module: Dict[str, Any]) -> bool:
        """Check if module is a trigger"""
        trigger_modules = [
            "gmail", "webhook", "builtin:schedule", 
            "microsoft365-excel", "slack", "trello"
        ]
        
        module_type = module.get("module", "")
        return any(module_type.startswith(trigger) for trigger in trigger_modules)
    
    def _is_valid_gmail_filter(self, filter_str: str) -> bool:
        """Basic Gmail filter syntax validation"""
        # Check for common Gmail operators
        valid_operators = [
            "is:", "has:", "from:", "to:", "subject:", "label:",
            "category:", "filename:", "older_than:", "newer_than:",
            "larger:", "smaller:", "cc:", "bcc:"
        ]
        
        # Simple validation - check if it contains valid operators
        return any(op in filter_str for op in valid_operators) or filter_str.strip() == ""

class ValidationReporter:
    """Generate validation reports"""
    
    @staticmethod
    def generate_report(results: List[ValidationResult]) -> str:
        """Generate human-readable validation report"""
        if not results:
            return "✅ All validations passed!"
        
        report = []
        errors = [r for r in results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in results if r.level == ValidationLevel.WARNING]
        info = [r for r in results if r.level == ValidationLevel.INFO]
        
        # Summary
        report.append(f"📊 Validation Summary:")
        report.append(f"   Errors: {len(errors)}")
        report.append(f"   Warnings: {len(warnings)}")
        report.append(f"   Info: {len(info)}")
        report.append("")
        
        # Errors
        if errors:
            report.append("❌ Errors (must fix):")
            for error in errors:
                report.append(f"   • {error.message}")
                if error.suggestion:
                    report.append(f"     💡 {error.suggestion}")
            report.append("")
        
        # Warnings
        if warnings:
            report.append("⚠️  Warnings (should fix):")
            for warning in warnings:
                report.append(f"   • {warning.message}")
                if warning.suggestion:
                    report.append(f"     💡 {warning.suggestion}")
            report.append("")
        
        # Info
        if info:
            report.append("ℹ️  Information (consider):")
            for item in info:
                report.append(f"   • {item.message}")
                if item.suggestion:
                    report.append(f"     💡 {item.suggestion}")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_json_report(results: List[ValidationResult]) -> str:
        """Generate JSON validation report"""
        report_data = {
            "summary": {
                "total": len(results),
                "errors": len([r for r in results if r.level == ValidationLevel.ERROR]),
                "warnings": len([r for r in results if r.level == ValidationLevel.WARNING]),
                "info": len([r for r in results if r.level == ValidationLevel.INFO])
            },
            "results": [
                {
                    "level": result.level.value,
                    "message": result.message,
                    "module_id": result.module_id,
                    "field": result.field,
                    "suggestion": result.suggestion
                }
                for result in results
            ]
        }
        
        return json.dumps(report_data, indent=2)

def main():
    """Demonstrate validation functionality"""
    # Sample automation for testing
    test_automation = {
        "name": "Test_Gmail_Automation",
        "description": "Test automation for validation",
        "modules": [
            {
                "id": 1,
                "module": "gmail",
                "version": 1,
                "parameters": {
                    "watch": "emails",
                    "connection": "{{gmail_connection}}",
                    "filter": "is:unread",
                    "maxResults": 100  # High value to trigger warning
                },
                "metadata": {
                    "designer": {"x": 0, "y": 0}
                }
            },
            {
                "id": 2,
                "module": "make-ai-agents",
                "version": 1,
                "parameters": {
                    "agent": "{{ai_agent}}",
                    "timeout": 300
                },
                "metadata": {
                    "designer": {"x": 300, "y": 0}
                }
            }
        ],
        "connections": [
            {
                "name": "gmail_connection",
                "type": "gmail"
            },
            {
                "name": "ai_agent",
                "type": "make-ai-agents"
            }
        ]
    }
    
    validator = AutomationValidator()
    is_valid, results = validator.validate_automation(test_automation)
    
    print(f"Validation Result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    print()
    
    # Generate reports
    text_report = ValidationReporter.generate_report(results)
    print(text_report)
    
    print("\n" + "="*50)
    print("JSON Report:")
    json_report = ValidationReporter.generate_json_report(results)
    print(json_report)

if __name__ == "__main__":
    main()