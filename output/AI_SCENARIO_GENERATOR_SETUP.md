# AI Scenario Generator - Clean Setup Guide

## Overview
This automation creates Make.com scenario blueprints from natural language descriptions using AI. Completely cleaned for Make.com compliance with no sensitive data.

## What Was Fixed
- ✅ Removed all API tokens and keys
- ✅ Fixed module structure to match Make.com format
- ✅ Cleaned connection references (use placeholder IDs)
- ✅ Removed HTTP Agent references (requires Enterprise)
- ✅ Simplified variable handling
- ✅ Fixed filter conditions syntax
- ✅ Proper metadata structure

## Required Connections
You need to set up these connections in Make.com:

1. **Custom Webhook** (ID: 123456)
   - Automatic webhook URL generation
   
2. **OpenAI Connection** (ID: 78910)
   - Add your OpenAI API key
   - Used for blueprint generation

3. **Google Sheets Connection** (ID: 11223) 
   - For logging generated scenarios
   - Needs access to your tracking spreadsheet

4. **Gmail Connection** (ID: 44556)
   - For sending notification emails
   - Requires Gmail OAuth

## Setup Steps

### 1. Import Blueprint
1. Create new scenario in Make.com
2. Import the cleaned JSON blueprint
3. Update connection IDs with your actual connection IDs

### 2. Create Google Sheets Log
Create a spreadsheet with sheet named "Generated_Scenarios":
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Timestamp | User Request | Scenario Name | Status | Blueprint/Error |

### 3. Update Spreadsheet ID
Replace `Enter_Your_Spreadsheet_ID_Here` with your actual Google Sheets ID.

### 4. Test Webhook
1. Enable scenario
2. Get webhook URL from module 1
3. Test with POST request:
```json
{
  "automation_description": "Create an automation that sends me daily weather updates",
  "user_email": "your@email.com",
  "scenario_name": "Weather Updates"
}
```

## Key Features
- **AI Blueprint Generation**: Creates complete Make.com scenarios
- **Email Notifications**: Sends blueprint via email
- **Error Handling**: Logs failed generations
- **Clean Output**: No API keys or sensitive data in JSON

## Webhook Fields
- `automation_description` (required): What automation you want
- `user_email` (optional): Where to send the blueprint
- `scenario_name` (optional): Custom name for the scenario

## Example Usage
POST to webhook URL:
```json
{
  "automation_description": "Monitor Gmail for invoices and save attachments to Google Drive",
  "user_email": "user@example.com"
}
```

Returns: Complete Make.com blueprint via email

## Important Notes
- No sensitive data stored in blueprint
- All connection IDs are placeholders
- Blueprint generates valid Make.com JSON
- Requires manual connection setup
- Works with free Make.com accounts

## Troubleshooting
- **Import fails**: Check JSON syntax in import
- **Connections fail**: Verify all 4 connections are set up
- **No email received**: Check Gmail connection and spam folder
- **Blueprint invalid**: Check OpenAI connection and quota