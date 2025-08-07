# 🤖 AI Makes Automation - Make.com Automation Generator

**Generate complete Make.com automations in seconds with AI** - No more spending hours manually configuring modules and connections!

## 🚀 Quick Start

1. **Describe what you want**: "I want to monitor the label Sold deal in my gmail account which is chris@cjsinsurancesolutions.com. I then want to extract 5 deals at a time once a week until the emails in the labels have all been marked off in a txt format.. This is the format of batches of 5 deals at a time it has to fit inside a 200 character message limit: 25x5 Referral fee for 1. Jennifer Sandoval \ Agt: Steeve G - 2. AMBER DRINKWATER \ Agt: Charlie R - 3. Alyson Freeman \ Agt: Richard O - 4. Erin Bade \ Agt: Steeve G  -  5. Helena Austine \  Agt: Summer L so what this is doing is pulling the first and last name of the client which is normally 9 times out of 10 in the subject line then pulling the agent name which is the person who sent me the emails first name and first initial of last name the only name you are never to extract is Chris Shannahan or Christopher Shannahan. As you can see here is an email 
2. Michael Ujlaky 719-412-6369
External
ACA Leads to be worked/ACA deals/ CO/KY / Jeff Deals/ACA deals/ CO/KY / Jeff Deals Sold
ACA Leads to be worked/Sold deal
Steeve asked who was calling Michael Ujlaky, who needed extra care.
You informed Steeve that the sale was complete and asked to check Michael Fenton.
By Gemini; there may be mistakes. Learn more

Steeve G
Attachments
Thu, Jul 24, 3:15 PM (13 days ago)
to me, Sevy

Let me know who is calling this needs extra care 

--
Steeve L. Gabriel
Senior Consultant
NOLIMIT SG LLC
US Health Advisors
USHEALTH Group honored as Gold winner in the 2016 Golden Bridge Awards ...


E: steveg.ushealth@gmail.com T: 561-541-3230

Confidentiality Statement: This email and any files transmitted with it are confidential and intended solely for the use of the individual or entity to whom they are addressed. If you have received this email in error, please notify the sender immediately by e-mail and delete the message along with any attached files. Please note that any unauthorized use, dissemination, distribution, or copying of this message or any attached files is strictly prohibited. Thank you for your cooperation.


 4 Attachments
  •  Scanned by Gmail
5

Christopher Shannahan
Sun, Jul 27, 2:36 PM (10 days ago)
Sold: "

As you can see the subject line has first and last name of client so: Michael Ujlaky and the agent name is anything but Christopher Shannahan so it would be Steeve G then you would put them here as the first name of a batch of 5 which would look like this: 1. Michael Ujlaky \ Agt: Steeve G  2. \ Agt: -   3. \ Agt:  -   4.\ Agt:  -  5. \  Agt: then you fill the other 4 once you complete 5 you then start a new one and go to the next email: 25x5 Referral fee for 1. \ Agt:  -  2. \ Agt: -   3. \ Agt:  -   4.\ Agt:  -  5. \  Agt:        THIS RUNS ONCE A WEEK

1. **Get complete automation**: Full Make.com configuration with all modules and connections
2. **Copy and run**: Paste into Make.com and activate - done!

```bash
# Interactive mode
python cli.py --interactive

# Single automation
python cli.py --description "Monitor Gmail for invoices and save to Google Drive"

# Use pre-built template
python cli.py --template gmail_customer_support
```

## ✨ Features

- 🎯 **Natural Language Input**: Describe automations in plain English
- 🏗️ **Complete Configurations**: Generated JSON ready for Make.com
- 🔧 **Pre-built Templates**: Common automation patterns ready to use  
- ✅ **Validation & Error Checking**: Ensures configurations work correctly
- 🔌 **Connection Management**: Automatic connection setup instructions
- 📊 **Multiple Output Formats**: JSON blueprints, validation reports

## 📋 Available Templates

### 1. Gmail Customer Support
- **Trigger**: Monitor support emails
- **AI Processing**: Categorize and analyze emails
- **Actions**: Auto-reply, create tickets, escalate
- **Use case**: "Handle customer support emails automatically"

### 2. Excel MySQL Sync  
- **Trigger**: Excel file changes
- **AI Validation**: Data quality checks
- **Actions**: Sync to database with transactions
- **Use case**: "Keep database in sync with Excel reports"

### 3. Enterprise API Orchestrator
- **Trigger**: Schedule or HTTP calls
- **AI Analysis**: Process API responses
- **Actions**: Route to multiple systems
- **Use case**: "Process internal API data and distribute"

## 🛠️ Installation

```bash
# Clone the repository
git clone <repo-url>
cd AI-makes-automation

# Install dependencies (if any)
pip install -r requirements.txt

# Make CLI executable
chmod +x cli.py
```

## 💬 Usage Examples

### Interactive Mode
```bash
python cli.py --interactive
```
Then describe what you want:
- "Monitor emails and create tasks from them"
- "Sync Excel data to MySQL every hour"  
- "Process API data with AI and generate reports"

### Command Line
```bash
# Generate from description
python cli.py --description "Watch Gmail for customer complaints and alert Slack"

# Use template
python cli.py --template excel_mysql_sync

# Process multiple descriptions
python cli.py --batch descriptions.txt

# List available templates
python cli.py --list-templates
```

### Batch Processing
Create `descriptions.txt`:
```
Monitor support emails and create tickets
Sync Excel sales data to database hourly  
Process webhook data and update CRM
Generate reports from API responses
```

Then run:
```bash
python cli.py --batch descriptions.txt
```

## 📁 File Structure

```
AI-makes-automation/
├── CLAUDE.md              # Instructions for AI assistants
├── README.md              # This file
├── cli.py                 # Interactive command-line interface
├── automation_generator.py # Core automation generation logic
├── templates.py           # Pre-built automation templates
├── schema_generator.py    # JSON schema validation
├── validator.py           # Comprehensive validation system
└── output/               # Generated automations
    ├── automation_1.json
    └── template_gmail.json
```

## 🎯 Supported Modules

### ✉️ Email & Communication
- **Gmail**: Watch emails, send replies, manage labels
- **Slack**: Send messages, create channels
- **Microsoft Teams**: Post messages, create tasks

### 🗄️ Data & Storage  
- **MySQL**: CRUD operations, transactions, stored procedures
- **Microsoft Excel**: Watch files, read/write data, create reports
- **Google Sheets**: Similar to Excel functionality
- **Data Store**: Logging and temporary storage

### 🤖 AI & Processing
- **Make AI Agents**: OpenAI, Anthropic Claude, xAI
- **HTTP Agent**: Enterprise internal API calls
- **Router**: Conditional logic and branching
- **Iterator**: Process arrays and collections

### 🔗 Triggers & Webhooks
- **Custom Webhooks**: Receive HTTP requests
- **Schedule**: Time-based triggers
- **File Watchers**: Monitor file changes

## 🔧 Configuration

### Connection Types
Each automation specifies required connections:

```json
{
  "name": "gmail_connection",
  "type": "gmail", 
  "scopes": ["https://www.googleapis.com/auth/gmail.modify"]
}
```

### AI Agent Setup
```json
{
  "name": "Support_Email_Classifier",
  "system_prompt": "You are a customer support assistant...",
  "max_tokens": 1000,
  "temperature": 0.3
}
```

### Error Handling
All modules include comprehensive error handling:
- **Retry Logic**: Automatic retries with exponential backoff
- **Fallback Actions**: Alternative paths on failures  
- **Logging**: Complete execution tracking
- **Alerts**: Notifications on critical errors

## ✅ Validation Features

The validator checks for:

### ❌ Errors (Must Fix)
- Missing required fields
- Invalid module configurations
- Duplicate module IDs
- Malformed connections

### ⚠️ Warnings (Should Fix)  
- High API rate limits
- Security issues (unprotected webhooks)
- Performance concerns (large batch sizes)
- Dangerous database operations

### ℹ️ Info (Consider)
- Missing error handlers
- Best practice recommendations
- Cost optimization suggestions
- Monitoring improvements

## 📊 Example Output

### Generated Automation
```json
{
  "name": "Gmail_Customer_Support_AI",  
  "description": "Monitor support emails, classify with AI, auto-respond",
  "modules": [
    {
      "id": 1,
      "module": "gmail",
      "parameters": {
        "watch": "emails",
        "filter": "to:support@company.com is:unread"
      }
    },
    {
      "id": 2, 
      "module": "make-ai-agents",
      "parameters": {
        "agent": "{{support_classifier}}"
      }
    }
  ],
  "connections": [
    {
      "name": "gmail_connection",
      "type": "gmail"
    }
  ]
}
```

### Validation Report
```
✅ Validation Summary:
   Errors: 0
   Warnings: 1  
   Info: 2

⚠️ Warnings:
   • High maxResults value (100) may hit rate limits
     💡 Consider reducing maxResults to 20 or less

ℹ️ Information:
   • No logging module found
     💡 Add data store module for execution logging
   • AI agent message without variable mapping  
     💡 Use {{variable}} syntax to pass dynamic data
```

## 🎨 Keywords & Patterns

The AI understands these keywords:

### Triggers
- **email**, **gmail** → Gmail watch module
- **schedule**, **every**, **hourly** → Schedule module  
- **webhook**, **api** → Custom webhook
- **excel**, **spreadsheet** → Excel watch module

### Processing  
- **AI**, **analyze**, **categorize** → AI agent module
- **validate**, **check**, **process** → Data processing
- **route**, **conditional** → Router module

### Actions
- **reply**, **respond** → Send email
- **save**, **store** → Database operations
- **alert**, **notify** → Slack/Teams message
- **create**, **update** → CRUD operations

### Examples
- "**Monitor** support **emails** and **auto-reply** to common questions"
- "**Sync Excel** data to **MySQL** every **hour** with **AI validation**"  
- "**Watch Gmail** for **invoices** and **save** to Google Drive"

## 🔄 Workflow

1. **Input**: Natural language description or template selection
2. **Parse**: Extract triggers, processing needs, and outputs  
3. **Generate**: Create module chain with proper configurations
4. **Validate**: Check for errors, warnings, and best practices
5. **Output**: JSON blueprint ready for Make.com
6. **Deploy**: Copy to Make.com and configure connections

## 🚀 Advanced Features

### Custom Module Support
```python
# Add support for new modules
def _create_custom_module(self) -> Dict[str, Any]:
    return {
        "id": self.module_counter,
        "module": "custom-service",  
        "parameters": {...}
    }
```

### Batch Processing
Process multiple automations from file:
```bash
python cli.py --batch automations.txt --output my_automations/
```

### Template Creation
Create your own templates:
```python
@staticmethod  
def my_custom_template() -> Dict[str, Any]:
    return {
        "name": "My_Custom_Automation",
        "blueprint": {...}
    }
```

## 🐛 Troubleshooting

### Common Issues

**"Module validation failed"**
- Check required fields are present
- Verify connection names match
- Ensure proper variable mapping

**"No trigger module found"**  
- Add Gmail, Webhook, or Schedule module
- Check trigger keywords in description

**"Connection errors"**
- Verify OAuth scopes in Make.com
- Check API key permissions  
- Test connections individually

### Debug Mode
```bash
python cli.py --description "your automation" --debug
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new modules
4. Update documentation  
5. Submit pull request

### Adding New Modules
1. Add to `ModuleType` enum
2. Create generation method
3. Add validation rules
4. Update templates if needed

## 📄 License

MIT License - Feel free to use and modify for your projects!

## 🆘 Support

- 📖 Check `CLAUDE.md` for detailed AI instructions
- 🐛 Report issues in GitHub
- 💡 Suggest new features and templates
- 📧 Contact for enterprise support

---

**🎉 Start generating automations in seconds instead of hours!**

```bash
python cli.py --interactive
# Describe: "Monitor emails and create tasks"  
# Result: Complete Make.com automation ready to run!
```