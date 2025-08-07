# 🛠️ Setup Instructions for AI Makes Automation

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **Make.com account** (free or paid)
3. **Gmail account** with API access
4. **Text editor** for viewing generated files

## 🚀 Step-by-Step Setup

### Step 1: Clone and Setup
```bash
git clone <repository-url>
cd AI-makes-automation
chmod +x cli.py
```

### Step 2: Test the System
```bash
python3 demo.py
```
This will create sample files in the `output/` directory.

### Step 3: Generate Your Specific Automation

Based on your requirements in the README, run:

```bash
python3 cli.py --interactive
```

When prompted, enter:
```
Monitor Gmail label 'Sold deal' for chris@cjsinsurancesolutions.com, extract client names from subject lines and agent names from sender, batch 5 deals per message in format '25x5 Referral fee for 1. [Client Name] \ Agt: [Agent Name]', run weekly, exclude Christopher Shannahan, output to text format under 200 characters
```

### Step 4: Configure Make.com

1. **Login to Make.com**
   - Go to make.com
   - Create new scenario

2. **Import the Generated Blueprint**
   - Copy JSON from generated file
   - Paste into Make.com scenario

3. **Configure Gmail Connection**
   - Add Gmail connection
   - Authorize with chris@cjsinsurancesolutions.com
   - Grant necessary permissions:
     - Read emails
     - Modify labels
     - Send emails (if needed)

4. **Configure AI Agent**
   - Create AI agent in Make.com
   - Use the generated system prompt
   - Set appropriate token limits

## 🔧 Your Specific Automation Requirements

### Input Details:
- **Email**: chris@cjsinsurancesolutions.com
- **Gmail Label**: "Sold deal"
- **Frequency**: Weekly
- **Batch Size**: 5 deals per message
- **Character Limit**: 200 characters max

### Output Format:
```
25x5 Referral fee for 1. [Client Name] \ Agt: [Agent First Name + Last Initial] - 2. [Client Name] \ Agt: [Agent] - 3. [Client Name] \ Agt: [Agent] - 4. [Client Name] \ Agt: [Agent] - 5. [Client Name] \ Agt: [Agent]
```

### Extraction Logic:
- **Client Name**: From email subject line (first and last name)
- **Agent Name**: From email sender (first name + first initial of last)
- **Exclusion**: Never extract "Christopher Shannahan" or "Chris Shannahan"

## 🎯 Custom Generation Command

For your exact requirements, use:

```bash
python3 cli.py --description "Create Gmail automation for chris@cjsinsurancesolutions.com that monitors 'Sold deal' label, extracts client names from subject lines and agent names from senders, batches 5 deals in 200-character format '25x5 Referral fee for 1. ClientName \ Agt: AgentName', runs weekly, excludes Christopher Shannahan, processes emails sequentially and marks as processed"
```

## 📄 Generated Files Location

After running the generator, check:
- `output/[AutomationName].json` - Complete automation config
- Blueprint section - Copy this to Make.com
- Validation report - Fix any errors before deploying

## 🔌 Required Connections in Make.com

1. **Gmail Connection**
   - Name: `gmail_connection`
   - Account: chris@cjsinsurancesolutions.com
   - Scopes: gmail.modify, gmail.readonly

2. **AI Agent Connection**
   - Name: `deal_processor_agent`
   - Model: GPT-4 (recommended for text extraction)
   - System Prompt: (generated in automation file)

## ⚙️ Make.com Configuration Steps

### Gmail Module Setup:
- **Watch**: Emails
- **Folder**: Look for label "Sold deal"
- **Filter**: `label:"Sold deal" is:unread`
- **Max Results**: 5 (to process 5 at a time)
- **Schedule**: Weekly (every 7 days)

### AI Agent Prompt:
```
You are a deal processing agent that extracts client and agent information from sold deal emails.

Extract from each email:
1. Client name from subject line (first and last name)
2. Agent name from email sender (first name + first initial of last name)
3. NEVER extract "Christopher Shannahan" or "Chris Shannahan" as agent

Format output as:
"25x5 Referral fee for 1. [ClientName] \ Agt: [AgentName] - 2. [ClientName] \ Agt: [AgentName] - ..."

Keep under 200 characters total. Process exactly 5 deals per batch.
```

## 🔄 Automation Flow

1. **Trigger**: Every 7 days
2. **Gmail**: Fetch 5 emails from "Sold deal" label
3. **AI Process**: Extract names and format
4. **Output**: Generate formatted text
5. **Gmail**: Mark emails as processed
6. **Repeat**: Until all emails processed

## 🐛 Troubleshooting

### Common Issues:

**"No emails found"**
- Check Gmail label name exactly matches "Sold deal"
- Verify account permissions
- Check filter syntax

**"AI extraction errors"**
- Review email format consistency
- Adjust AI prompt for your specific email patterns
- Test with sample emails first

**"Character limit exceeded"**
- Shorten client/agent names if needed
- Adjust format template
- Split into multiple messages

### Testing Steps:

1. **Test Gmail connection** - Fetch a few emails manually
2. **Test AI extraction** - Send sample email to AI
3. **Test full flow** - Run with 1-2 emails first
4. **Scale up** - Process full batch once tested

## 📞 Support

If you encounter issues:
1. Check the generated validation report
2. Review Make.com execution logs  
3. Test each module individually
4. Verify all connections are active

## 🎉 Success Indicators

Your automation is working when:
- ✅ Emails are fetched from correct label
- ✅ Client names extracted from subject lines
- ✅ Agent names extracted from senders (excluding Christopher)
- ✅ Format matches: "25x5 Referral fee for 1. Name \ Agt: Agent..."
- ✅ Messages stay under 200 characters
- ✅ Processed emails are marked/labeled
- ✅ Runs weekly automatically

Ready to automate your deal processing! 🚀