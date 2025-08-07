# CLAUDE.md - AI-Powered Make.com Automation Creation Guide

## Overview
This guide enables you to describe what automation you want, and the AI will generate a complete, working Make.com automation diagram with all configurations ready to run.

## Quick Start Process

### 1. Describe Your Automation
Simply type what you want to automate in plain language:
- "I want to automatically respond to customer support emails and create tickets for complex issues"
- "Create an automation that syncs data from Excel to MySQL every hour"
- "Build a workflow that monitors Gmail and uses AI to categorize and process emails"

### 2. AI Will Generate
The AI will create:
- Complete scenario structure
- All module configurations
- Connection requirements
- Error handling setup
- Testing procedures

### 3. Implementation
Copy the generated configuration directly into Make.com - no manual configuration needed.

## Standard Automation Structure

### Core Components
Every automation follows this pattern:
```
Trigger → AI Processing → Router → Actions → Error Handling
```

### Module Naming Convention
- Scenarios: `[Action]_[Object]_[Type]`
- Connections: `[Service]_[Environment]_Connection`
- AI Agents: `[Purpose]_Agent`

## Available Modules & Templates

### 1. Gmail Automations
**Email Response System**
- Trigger: Watch emails with filter
- AI: Analyze and categorize
- Actions: Auto-reply, create draft, or escalate
- Example: "Monitor support@company.com and auto-respond to FAQs"

### 2. Excel Processing
**Data Sync Pipeline**
- Trigger: Watch workbook changes
- AI: Analyze data patterns
- Actions: Update database, generate reports
- Example: "Sync Excel sales data to MySQL hourly"

### 3. HTTP Agent (Enterprise)
**Internal API Integration**
- Trigger: Webhook or schedule
- AI: Process API responses
- Actions: Update systems, trigger workflows
- Example: "Fetch data from internal API and update CRM"

### 4. Database Operations
**MySQL Transaction Management**
- Trigger: Any source
- AI: Validate and transform data
- Actions: Insert/update with transactions
- Example: "Process incoming orders with validation"

### 5. AI Services
**Claude/xAI Integration**
- Trigger: Data input
- AI: Advanced analysis or generation
- Actions: Store insights, trigger workflows
- Example: "Analyze customer feedback with Claude"

## Prompt Templates

### Basic Automation Request
```
Create a Make.com automation that:
- Triggers when: [describe trigger]
- Processes: [what should happen]
- Outputs to: [where results go]
- Handles errors by: [error strategy]
```

### Advanced Automation Request
```
Build an enterprise Make.com workflow:
- Multiple triggers: [list triggers]
- AI analysis: [describe AI role]
- Database: [MySQL operations needed]
- Error handling: Comprehensive with retry
- Testing: Include test scenarios
```

## Configuration Templates

### Gmail Module Configuration
```
Watch Emails:
- Filter: is:unread -label:processed
- Max Results: 10
- Mark as Read: No

AI Agent Prompt:
"Analyze emails for:
1. Category (urgent/normal/spam)
2. Required action
3. Response draft if needed"
```

### MySQL Configuration
```
Transaction Setup:
- Auto-commit: Disabled
- Isolation: READ COMMITTED
- Error handling: Rollback on failure
- Retry logic: 3 attempts
```

### Error Handler Configuration
```
Error Routes:
1. Temporary → Retry with backoff
2. Data Error → Clean and retry
3. Critical → Stop and alert
4. Rate Limit → Queue for later
```

## Testing Protocol

### 1. Component Testing
- Test each module individually
- Verify connections work
- Check data mappings

### 2. Integration Testing
- Run end-to-end scenarios
- Test error conditions
- Verify output formatting

### 3. Performance Testing
- Monitor execution time
- Check API limits
- Optimize token usage

## Common Patterns

### Pattern 1: Email to Task
```
Gmail → AI Extract Tasks → Create in Project Tool → Reply Confirmation
```

### Pattern 2: Data Validation Pipeline
```
Input → MySQL Validate → AI Process → Router → Update Systems
```

### Pattern 3: Multi-Channel Alert
```
Trigger → AI Analyze → Router → (Email + Slack + SMS)
```

## Best Practices

### 1. Connection Management
- Use descriptive connection names
- Store credentials securely
- Test connections before use

### 2. AI Agent Design
- Keep prompts focused
- Limit token usage
- Include clear constraints

### 3. Error Handling
- Always add error handlers
- Use appropriate retry logic
- Log errors for debugging

### 4. Performance
- Batch operations when possible
- Set appropriate timeouts
- Monitor API quotas

## Troubleshooting

### Common Issues
1. **Connection Failed**: Check OAuth/API key
2. **Timeout Errors**: Increase timeout or reduce batch size
3. **AI Token Limit**: Optimize prompts, reduce context
4. **Rate Limits**: Add delays or queue requests

### Debug Steps
1. Check scenario history
2. Review error logs
3. Test modules individually
4. Verify data formats

## Quick Reference

### Required Information for AI
When requesting an automation, provide:
1. **Trigger**: What starts the automation
2. **Data Sources**: Where data comes from
3. **Processing**: What should happen
4. **Output**: Where results go
5. **Error Handling**: How to handle failures

### Module Limits
- Gmail: 25MB attachments
- Excel: 1M cells per workbook
- MySQL: Depends on server config
- AI Tokens: Model-specific limits

## Example Requests

### Simple Request
"Create an automation that watches my Gmail for invoices and saves them to Google Drive"

### Complex Request
"Build a customer support system that:
- Monitors support@company.com
- Uses AI to categorize emails
- Auto-responds to common questions
- Creates tickets for complex issues
- Updates our MySQL database
- Sends Slack notifications for urgent items"

### Enterprise Request
"Design an enterprise workflow with:
- HTTP Agent fetching from internal API
- MySQL transaction processing
- Claude AI for analysis
- Excel report generation
- Comprehensive error handling
- Automatic retry logic"

## Success Metrics

Track these KPIs:
- Execution success rate > 99%
- Average processing time < 2 minutes
- AI accuracy > 95%
- Error recovery rate > 90%

## Next Steps

1. **Describe your automation** in plain language
2. **Review the generated configuration**
3. **Copy to Make.com** and test
4. **Iterate** based on results

Remember: The more specific your description, the better the generated automation will be. Include details about data formats, error handling preferences, and any special requirements.