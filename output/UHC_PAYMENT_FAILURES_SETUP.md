# UHC Payment Failures Automation Setup Guide

## Overview
Daily automation (8:30 AM ET) that processes UnitedHealthcare payment failure emails, extracts customer data, de-duplicates against a backlist, and creates a daily texting list.

## One-Time Setup Steps

### 1. Create Google Sheets Structure

Create spreadsheet named **`UHC_Payment_Failures`** with these 3 sheets:

#### Sheet 1: "To Text - Today"
| RunDate | SourceDate | FullName | FirstName | LastName | Email | Phone | PolicyID | Premium | Carrier | Notes |
|---------|------------|----------|-----------|----------|--------|--------|----------|---------|---------|--------|

#### Sheet 2: "Backlist"
| RunDate | SourceDate | FullName | FirstName | LastName | Email | Phone | PolicyID | Premium | Carrier | Notes |
|---------|------------|----------|-----------|----------|--------|--------|----------|---------|---------|--------|

#### Sheet 3: "Raw Inbox (history)"
| RunDate | SourceDate | FullName | FirstName | LastName | Email | Phone | PolicyID | Premium | Carrier | Notes |
|---------|------------|----------|-----------|----------|--------|--------|----------|---------|---------|--------|

### 2. Gmail Label Setup
Create label: `uhc-payment-failure/processed`

### 3. Book of Business Sheet
Ensure your BoB spreadsheet has columns:
- PolicyID
- Name
- Email  
- Phone

### 4. Make.com Connections
Set up these connections:
1. **Gmail Connection** (ID: 12345) - OAuth for email access
2. **Google Sheets Connection** (ID: 23456) - Access to both spreadsheets

## Import & Configure Blueprint

### 1. Import JSON
1. Create new scenario in Make.com
2. Import the JSON blueprint
3. Set schedule: Daily at 8:30 AM ET

### 2. Update IDs in Blueprint
Replace these placeholders:
- `ENTER_YOUR_BOB_SPREADSHEET_ID` - Your Book of Business sheet ID
- `ENTER_YOUR_UHC_SPREADSHEET_ID` - Your UHC_Payment_Failures sheet ID  
- `ENTER_YOUR_PROCESSED_LABEL_ID` - Gmail label ID for processed emails

### 3. Update Connection IDs
- Replace `12345` with your Gmail connection ID
- Replace `23456` with your Google Sheets connection ID

## Scenario Flow

### Email Processing
1. **Searches Gmail** for: `from:noreply@mail.uhcmemberhub.com subject:"Customers with Payment Failure as of" newer_than:7d`
2. **Skips** already processed emails (labeled)
3. **Parses** either CSV attachments or email body text

### Data Extraction
- **CSV Path**: Downloads and parses CSV files
- **Email Body Path**: Regex patterns extract:
  - Policy ID
  - Name
  - Email
  - Phone
  - Premium

### Enrichment & Normalization
- Splits full name → FirstName, LastName
- Cleans phone to digits only
- Removes $ and commas from premium
- Sets Carrier = "UnitedHealthcare (UHOne)"

### Cross-Reference & De-Dupe
1. **Book of Business lookup**:
   - Primary: PolicyID
   - Fallback: Email, then FullName
   - Pulls phone if missing
   
2. **Backlist check**:
   - Primary: PolicyID
   - Fallback: FullName + Phone
   - Skips if found

### Output Generation
1. **Clears** "To Text - Today" sheet
2. **Adds** new non-backlisted records
3. **Appends** all records to "Raw Inbox (history)"
4. **Updates** Backlist with new entries
5. **Labels** emails as processed

## Testing Checklist

1. ✅ Gmail search returns correct emails
2. ✅ CSV attachments download properly
3. ✅ Email body parsing extracts all fields
4. ✅ BoB lookup finds existing customers
5. ✅ Backlist prevents duplicates
6. ✅ "To Text - Today" only shows new entries
7. ✅ History tracks all processed records
8. ✅ Emails get labeled after processing

## Daily Output
Your texting program reads from:
- **Google Sheets**: `UHC_Payment_Failures` → "To Text - Today" tab
- Contains only new, de-duplicated customers for the current day

## Troubleshooting

### No emails found
- Check Gmail query syntax
- Verify sender email is correct
- Check date range (newer_than:7d)

### Parsing failures
- CSV: Verify column headers match
- Email body: Check regex patterns match actual format

### Missing phone numbers
- Check BoB sheet has phone data
- Verify PolicyID/Email matching works

### Duplicate texts
- Check Backlist is being updated
- Verify de-dupe logic conditions

## Notes
- Never re-texts same PolicyID unless manually removed from Backlist
- Processes multiple customers per email (CSV or body)
- Keeps audit trail in "Raw Inbox (history)"
- Phone may be blank if not found - fill manually or skip