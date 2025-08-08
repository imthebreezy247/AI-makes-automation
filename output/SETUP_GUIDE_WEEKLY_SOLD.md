# Weekly Sold → Set-to-Pay Automation Setup Guide

## Overview
This automation runs weekly to process Gmail "Sold" emails, extract deals, log to Google Sheets, and generate Zelle payment text (25x5 format).

## Prerequisites
1. Gmail account with labels: "Sold", "Recorded", "Set to Pay"
2. Google Sheets spreadsheet named "Referral Payout Log"
3. Make.com account with Gmail and Google Sheets connections

## Step 1: Create Google Sheets Structure
Create a spreadsheet named "Referral Payout Log" with these sheets:

### Sheet 1: "Ledger"
| Column A | Column B | Column C | Column D | Column E | Column F | Column G | Column H | Column I | Column J |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| Run Date (YYYY-MM-DD) | Batch ID | Line # (1-5) | Client First | Client Last | Agent | Source Email ID | Message URL | Recorded Status | Recorded At |

### Sheet 2: "Weekly Batches"
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Run Date (YYYY-MM-DD) | Batch ID | Zelle Text (<=200 chars) | Deals in Batch | Email IDs (CSV) |

### Sheet 3: "Taxes"
| Column A | Column B | Column C | Column D | Column E | Column F | Column G |
|----------|----------|----------|----------|----------|----------|----------|
| Run Date (YYYY-MM-DD) | Client Full Name | Agent | Referral Type | Amount | Batch ID | Note |

## Step 2: Get Gmail Label IDs
1. In Gmail, find your label IDs for:
   - "Sold" label
   - "Recorded" label
   - "Set to Pay" label

## Step 3: Import to Make.com
1. Create new scenario in Make.com
2. Import the JSON blueprint
3. Update these placeholders:
   - Replace `12345` with your Gmail connection ID
   - Replace `67890` with your OpenAI API connection ID
   - Replace `Enter your Google Sheets ID here` with your actual Sheets ID
   - Replace label IDs in module 21

## Step 4: Configure Connections
1. **Gmail Connection**: Authorize access to read/modify emails
2. **Google Sheets Connection**: Authorize access to your spreadsheet
3. **OpenAI Connection**: Add your API key

## Step 5: Set Schedule
The automation is set to run:
- Every Monday at 9:00 AM EST
- Processes emails from last 8 days

## Step 6: Test the Automation
1. Add test emails to "Sold" label
2. Run scenario manually
3. Verify:
   - Deals extracted correctly
   - Google Sheets populated
   - Emails moved to "Recorded" and "Set to Pay"

## Key Features
- **Batch Processing**: Groups deals in sets of 5
- **Zelle Text**: Auto-generates payment descriptions (200 char limit)
- **Exclusions**: Skips deals where agent is "Chris Shanahan" or "Chris Shannahan"
- **Email Pattern**: Extracts "Client Name \ Agt: Agent Name" format

## Troubleshooting
- **No emails found**: Check Gmail search query and label names
- **Extraction errors**: Verify email format matches pattern
- **Sheets errors**: Confirm spreadsheet ID and sheet names
- **Label errors**: Update label IDs in final module

## Email Format Expected
```
1. John Smith \ Agt: Richard O -
2. JANE DOE \ Agt: Carlos V -
3. Mike Johnson \ Agt: Jordan G
```

## Output Example
**Zelle Text (Weekly Batches):**
```
25x5 Referral fee for
1. John Smith \ Agt: Richard O -
2. Jane Doe \ Agt: Carlos V -
3. Mike Johnson \ Agt: Jordan G
```