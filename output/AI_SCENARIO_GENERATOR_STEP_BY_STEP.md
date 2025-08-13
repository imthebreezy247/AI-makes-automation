# AI Scenario Generator - Complete Step-by-Step Setup Guide

## 🎯 Project Overview
This automation creates Make.com scenario blueprints from natural language descriptions using AI. When you send a request to the webhook, GPT-4o generates a complete Make.com JSON blueprint and emails it to you.

## 📋 Prerequisites Checklist
- [ ] Make.com account (free tier works)
- [ ] OpenAI API account with GPT-4o access
- [ ] Gmail account for notifications
- [ ] Google Sheets for logging (optional but recommended)

---

## 🚀 STEP 1: Import the Blueprint

### 1.1 Create New Scenario
1. Go to Make.com dashboard
2. Click "Create a new scenario"
3. Click the settings gear ⚙️ in top right
4. Select "Import Blueprint"
5. Upload `ai_scenario_generator_clean.json`

### 1.2 Verify Import Success ✅
**CRITICAL CHECK**: Look at the module flow numbers (gray numbers on each module)
- All modules should show "1" (meaning they run once per webhook)
- If any show higher numbers, the import failed

---

## 🔧 STEP 2: Set Up Connections

### 2.1 Custom Webhook (Module 1)
**Status**: Already configured ✅
- No setup needed
- Will generate webhook URL automatically

### 2.2 OpenAI Connection (Module 5)
1. Click on the OpenAI module (ID: 5)
2. Click "Account" dropdown
3. Select "Add a connection"
4. Name: "OpenAI GPT-4o"
5. Enter your OpenAI API key
6. Test connection

**⚠️ CRITICAL**: Replace connection ID `78910` with your actual connection ID

### 2.3 Google Sheets Connection (Module 9 & 11)
1. Click on Google Sheets module (ID: 9)
2. Click "Account" dropdown  
3. Select "Add a connection"
4. Name: "AI Generator Logs"
5. Authorize with Google OAuth
6. Test connection

**⚠️ CRITICAL**: Replace connection ID `11223` with your actual connection ID

### 2.4 Gmail Connection (Module 10 & 12)
1. Click on Gmail module (ID: 10)
2. Click "Account" dropdown
3. Select "Add a connection" 
4. Name: "AI Generator Notifications"
5. Authorize with Gmail OAuth
6. Test connection

**⚠️ CRITICAL**: Replace connection ID `44556` with your actual connection ID

---

## 📊 STEP 3: Create Google Sheets Log (Optional)

### 3.1 Create Spreadsheet
1. Go to Google Sheets
2. Create new spreadsheet: "AI Scenario Generator Log"
3. Create sheet named "Generated_Scenarios"

### 3.2 Set Up Headers
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Timestamp | User Request | Scenario Name | Status | Blueprint/Error |

### 3.3 Update Spreadsheet ID
1. Copy spreadsheet ID from URL
2. In Make.com, find modules 9 & 11
3. Replace `Enter_Your_Spreadsheet_ID_Here` with your ID

---

## ⚙️ STEP 4: Configure Module Settings

### 4.1 Verify Variable References
**LESSON LEARNED**: Check these critical mappings:

**Module 5 (OpenAI) should reference**:
- `{{2.value}}` (userRequest variable)
- `{{3.value}}` (scenarioName variable)  
- `{{4.value}}` (timestamp variable)

**Module 6 should reference**:
- `{{5.choices[1].message.content}}` (OpenAI response)

### 4.2 Check Filter Logic (Module 8)
**LESSON LEARNED**: Filters must be properly configured
- Condition: `{{7.value}}` equals `true`
- This determines success vs. error path

---

## 🧪 STEP 5: Testing Protocol

### 5.1 Start Simple Test
1. Enable scenario (toggle switch)
2. Get webhook URL from module 1
3. Test with simple request first

### 5.2 Test Request Format
```json
{
  "automation_description": "Create an automation that sends me daily weather updates",
  "user_email": "your@email.com",
  "scenario_name": "Weather Updates Test"
}
```

### 5.3 Debug Checklist
**LESSON LEARNED**: Check these in order:

1. **Module Execution Numbers**
   - [ ] All modules show "1" execution
   - [ ] No modules running multiple times

2. **Variable Storage**
   - [ ] Module 2: userRequest stored
   - [ ] Module 3: scenarioName stored  
   - [ ] Module 4: timestamp stored

3. **OpenAI Response**
   - [ ] Module 5: Returns valid JSON
   - [ ] Module 6: Blueprint extracted
   - [ ] Module 7: Validation passes

4. **Output Path**
   - [ ] Success: Modules 9 & 10 execute
   - [ ] Error: Modules 11 & 12 execute

---

## 📧 STEP 6: Email Configuration

### 6.1 Success Email Template (Module 10)
**Already configured** with:
- Subject: "✅ Your Make.com Scenario Blueprint is Ready"
- Includes complete JSON blueprint
- Step-by-step import instructions

### 6.2 Error Email Template (Module 12)  
**Already configured** with:
- Subject: "❌ Scenario Generation Failed"
- Error details and retry instructions

---

## 🚨 STEP 7: Common Issues & Solutions

### 7.1 "Modules Running Multiple Times"
**SOLUTION**: This blueprint uses individual variables (not aggregators)
- Check: No Text Aggregators present ✅
- Check: No Array Aggregators present ✅  
- Variables pass data without multiplication

### 7.2 "OpenAI Connection Failed"
**SOLUTIONS**:
- Verify API key is correct
- Check OpenAI account has GPT-4o access
- Test connection in Make.com

### 7.3 "Blueprint Validation Failed"
**SOLUTIONS**:
- Check OpenAI prompt clarity
- Verify response contains "flow" keyword
- Review generated JSON for syntax errors

### 7.4 "Email Not Received"
**SOLUTIONS**:
- Check Gmail connection
- Verify recipient email format
- Check spam folder
- Test Gmail connection separately

---

## ✅ STEP 8: Final Verification

### 8.1 Complete Test Run
1. Send webhook request
2. Check scenario execution log
3. Verify email received
4. Test generated blueprint

### 8.2 Production Setup
1. Document webhook URL
2. Share with team/users
3. Monitor Google Sheets log
4. Set up error monitoring

---

## 🎯 Usage Instructions

### Webhook Request Format
```json
{
  "automation_description": "Your automation description here",
  "user_email": "notifications@yourdomain.com",
  "scenario_name": "Custom Scenario Name"
}
```

### Fields Explained
- `automation_description` **(required)**: Plain English description
- `user_email` *(optional)*: Where to send blueprint
- `scenario_name` *(optional)*: Custom name, auto-generated if empty

### Example Requests
```json
{
  "automation_description": "Monitor Gmail for invoices and save attachments to Google Drive",
  "user_email": "user@example.com"
}
```

```json
{
  "automation_description": "Create daily reports from Google Sheets and email to team",
  "user_email": "reports@company.com",
  "scenario_name": "Daily Team Reports"
}
```

---

## 📊 Success Metrics

### What Good Looks Like
- [ ] Webhook responds within 30 seconds
- [ ] OpenAI generates valid JSON blueprint  
- [ ] Email delivered with complete blueprint
- [ ] Generated blueprint imports successfully to Make.com
- [ ] All modules execute exactly once

### Troubleshooting Decision Tree
```
Request Fails?
├─ Check webhook URL and request format
├─ Verify all connections are active
└─ Review scenario execution log

OpenAI Fails?  
├─ Check API key and quota
├─ Verify prompt clarity
└─ Test with simpler request

Email Fails?
├─ Check Gmail connection
├─ Verify recipient address
└─ Check spam folder

Blueprint Invalid?
├─ Review OpenAI response
├─ Check JSON syntax
└─ Verify Make.com compatibility
```

## 🎉 You're Ready!

Your AI Scenario Generator is now configured and ready to create Make.com automations from natural language descriptions. The system leverages GPT-4o to understand your requirements and generate complete, working blueprints that you can import directly into Make.com.