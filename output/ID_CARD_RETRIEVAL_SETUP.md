# 🆔 Automated ID Card Retrieval System - Setup Guide

## 📋 Overview

This automation system monitors HealthSherpa enrollment emails and automatically retrieves health insurance ID cards from carrier portals after a 48-hour delay, then emails them directly to clients.

### ✨ Key Features
- **Automatic Email Monitoring**: Watches for HealthSherpa enrollment confirmations
- **Smart Carrier Detection**: Identifies insurance carriers from email content
- **48-Hour Delay**: Ensures enrollment is fully processed before retrieval
- **Multi-Carrier Support**: Handles Ambetter, Oscar, BCBS (GA/FL), and more
- **Error Handling**: Comprehensive retry logic and manual fallback
- **Client Communication**: Automated confirmation and delivery emails

## 🏗️ Architecture Overview

```
HealthSherpa Email → Parse & Queue → Wait 48hrs → Carrier Router → Retrieve ID Card → Email Client
```

### Two-Scenario System
1. **Email Processor**: Captures and queues enrollment emails
2. **ID Card Retriever**: Runs hourly to process due retrievals

## 📦 Prerequisites

### Required Make.com Modules
- Gmail (OAuth connection)
- Google Sheets (for queue management)
- HTTP/Webhooks (for carrier APIs)
- Text Parser (for email parsing)
- Router (for carrier routing)
- Iterator (for batch processing)

### External Dependencies
- Google Sheets spreadsheet for queue management
- Python/Selenium server for complex portals
- Secure credential storage
- Optional: Browserless.io for headless automation

### Required Accounts & Credentials
- Gmail OAuth access
- Insurance carrier portal accounts:
  - Ambetter agent portal
  - Oscar provider access
  - BCBS state-specific portals
- Google Sheets API access

## 🚀 Setup Instructions

### Step 1: Create Google Sheets Database

Create a new Google Sheet with two tabs:

#### Tab 1: "ID_Card_Queue"
| Column | Header | Description |
|--------|--------|-------------|
| A | client_name | Full name from email |
| B | client_email | Email address |
| C | enrollment_date | When queued |
| D | retrieval_date | When to process (enrollment + 48hrs) |
| E | carrier | Detected carrier name |
| F | status | pending/processing/completed/failed |
| G | id_card_url | Download link if available |
| H | error_notes | Error messages |
| I | healthsherpa_email_id | Original email ID |
| J | phone_number | Client phone if available |

#### Tab 2: "Manual_ID_Cards"
Same structure for cards requiring manual processing.

### Step 2: Configure Gmail Connection

1. **Create Gmail OAuth Connection** in Make.com
   - Name: `Gmail_CJS_Insurance`
   - Account: `chris@cjsinsurancesolutions.com`
   - Scopes: Read, Modify, Send emails

2. **Set up Email Filter**
   ```
   from:no_reply@healthsherpa.com 
   subject:"Action required: Next steps to finalize your health insurance enrollment"
   ```

### Step 3: Set Up Scenario 1 - Email Processor

#### Module 1: Gmail Watch Emails
```json
{
  "connection": "Gmail_CJS_Insurance",
  "folder": "INBOX",
  "filter": "from:no_reply@healthsherpa.com subject:\"Action required: Next steps to finalize your health insurance enrollment\"",
  "maxResults": 10,
  "markAsRead": true,
  "addLabel": "ID_Card_Pending"
}
```

#### Module 2: Text Parser - Extract Client Data
```javascript
// Pattern for client name
(?<=Hi ).*?(?=,)

// Pattern for carrier detection
(Georgia Access|Ambetter|Oscar|BCBS|Blue Cross|Florida Blue|Peach State|CareSource)

// Pattern for phone number (if available)
\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}
```

#### Module 3: Add to Google Sheets Queue
Map fields:
- A: `{{2.client_name}}`
- B: `{{1.from}}`
- C: `{{now}}`
- D: `{{addDays(now; 2)}}`
- E: `{{2.carrier_detected}}`
- F: `"pending"`
- I: `{{1.id}}`

#### Module 4: Send Confirmation Email
```
Subject: ID Card Request Received - Processing in 48 Hours

Hi {{2.client_name}},

We've received your enrollment confirmation and will automatically retrieve your ID card in 48 hours.

Carrier: {{2.carrier_detected}}
Expected Processing: {{formatDate(addDays(now; 2); "MM/DD/YYYY")}}

You'll receive your ID card via email once it's available.

Best regards,
CJS Insurance Solutions
706-388-4513
```

### Step 4: Set Up Scenario 2 - ID Card Retriever

**Schedule**: Every hour (`0 * * * *`)

#### Module 1: Search Google Sheets
Filter: `retrieval_date <= NOW() AND status = 'pending'`

#### Module 2: Iterator
Process each due card individually

#### Module 3: Router - Carrier-Specific Logic

##### Route 1: AMBETTER
```javascript
// Filter condition
{{carrier}} contains "Ambetter"

// HTTP Request to Ambetter API
URL: https://member.ambetter.com/api/idcard
Method: POST
Headers: {
  "Authorization": "Bearer {{dataStore.ambetter_token}}",
  "Content-Type": "application/json"
}
Body: {
  "member_name": "{{client_name}}",
  "policy_number": "{{policy_number}}"
}
```

##### Route 2: OSCAR
```javascript
// Webhook to Python Selenium script
URL: https://your-server.com/retrieve_oscar
Method: POST
Body: {
  "client_name": "{{client_name}}",
  "member_id": "{{member_id}}",
  "dob": "{{date_of_birth}}"
}
```

##### Route 3: BCBS Georgia
```javascript
// Complex portal navigation
URL: https://www.bcbsga.com/member/login
// Use Browserless.io or custom Selenium
```

##### Route 4: BCBS Florida
```javascript
URL: https://www.floridablue.com/members/login
// State-specific portal handling
```

##### Route 5: Manual Fallback
```javascript
// Add to manual processing queue
// Send Slack notification
// Email operations team
```

#### Module 4: Send ID Card Email
```
Subject: Your {{carrier}} Health Insurance ID Card

Dear {{client_name}},

Your health insurance ID card is attached to this email.

Carrier: {{carrier}}
Policy Effective Date: {{effective_date}}

Please save this ID card for your records. You can present it at your healthcare provider or pharmacy.

Important reminders:
• Keep a copy on your phone for easy access
• Some providers may accept digital copies
• Contact us if you need assistance accessing care

Best regards,
CJS Insurance Solutions
706-388-4513
```

#### Module 5: Update Status
Mark as "completed" in Google Sheets with timestamp

### Step 5: Error Handling Configuration

#### Retry Logic
```json
{
  "maxRetries": 3,
  "retryInterval": 3600,
  "backoffStrategy": "exponential",
  "retryOn": ["timeout", "rate_limit", "server_error"]
}
```

#### Fallback Actions
1. **First Failure**: Retry after 1 hour
2. **Second Failure**: Retry after 4 hours
3. **Third Failure**: Route to manual queue
4. **Critical Error**: Immediate Slack alert

### Step 6: External Python Service (Optional)

For complex portals requiring Selenium:

```python
# deploy to your server or cloud function
from flask import Flask, request, jsonify
import os
from selenium import webdriver
import time

app = Flask(__name__)

@app.route('/retrieve_oscar', methods=['POST'])
def retrieve_oscar_card():
    data = request.json
    
    # Set up headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to Oscar portal
        driver.get("https://member.hioscar.com/login")
        
        # Login with stored credentials
        driver.find_element("id", "username").send_keys(os.environ['OSCAR_USERNAME'])
        driver.find_element("id", "password").send_keys(os.environ['OSCAR_PASSWORD'])
        driver.find_element("button", "Login").click()
        
        # Navigate to ID cards section
        time.sleep(3)
        driver.find_element("link text", "ID Cards").click()
        
        # Search for member
        search_box = driver.find_element("id", "member-search")
        search_box.send_keys(data['client_name'])
        search_box.submit()
        
        # Download ID card
        download_link = driver.find_element("class", "id-card-download")
        pdf_url = download_link.get_attribute('href')
        
        return jsonify({
            "success": True,
            "pdf_url": pdf_url
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## 🔐 Security Configuration

### Credential Management
1. **Use Make.com Data Stores** for encrypted credential storage
2. **Never log credentials** in scenario history
3. **Rotate credentials** quarterly
4. **Use OAuth where available** instead of passwords

### Data Protection
- Client data encrypted in transit and at rest
- Google Sheets with restricted access
- Regular audit logs review
- HIPAA compliance considerations

## 📊 Monitoring & Analytics

### Key Metrics to Track
- **Success Rate**: Target >85% automated retrieval
- **Processing Time**: Average <5 minutes per card
- **Error Types**: Categorize failures for improvement
- **Manual Fallback Rate**: Minimize to <15%

### Alerting Setup
```json
{
  "alerts": [
    {
      "condition": "3 consecutive failures",
      "action": "Slack notification to #ops-alerts"
    },
    {
      "condition": "Success rate <80% in 24hrs",
      "action": "Email to operations manager"
    },
    {
      "condition": "Queue backlog >50 items",
      "action": "Scale alert and manual intervention"
    }
  ]
}
```

## 🧪 Testing Procedures

### Pre-Launch Testing
1. **Test with dummy enrollments** for each carrier
2. **Verify email filtering** accuracy
3. **Test 48-hour delay** with accelerated timeline
4. **Validate error handling** with invalid credentials
5. **Check manual fallback** routing

### Production Testing
1. **Monitor first 10 live retrievals** closely
2. **Verify client satisfaction** with delivery format
3. **Check carrier portal rate limits**
4. **Validate data privacy** compliance

## 🚀 Go-Live Checklist

- [ ] Gmail OAuth connection tested and working
- [ ] Google Sheets database created with correct structure
- [ ] All carrier credentials secured in Data Store
- [ ] Email templates customized with CJS branding
- [ ] Error handling configured with appropriate notifications
- [ ] Manual fallback process documented for team
- [ ] Monitoring alerts configured
- [ ] Python service deployed (if using complex portals)
- [ ] Test scenarios executed successfully
- [ ] Team trained on monitoring and troubleshooting

## 🔧 Troubleshooting Guide

### Common Issues

#### 1. Email Not Triggering
- **Check Gmail filter syntax**
- **Verify OAuth permissions**
- **Confirm folder path is correct**

#### 2. Carrier API Failures
- **Check credential expiration**
- **Verify API endpoint URLs**
- **Monitor rate limits**

#### 3. PDF Download Issues
- **Check file size limits**
- **Verify PDF format compatibility**
- **Test attachment delivery**

#### 4. High Manual Fallback Rate
- **Review carrier detection patterns**
- **Update portal automation scripts**
- **Check for carrier portal changes**

### Debug Steps
1. **Check Make.com execution history**
2. **Review error logs in detail**
3. **Test individual modules in isolation**
4. **Verify data mapping between modules**
5. **Check external service availability**

## 📈 Optimization Opportunities

### Phase 2 Enhancements
- **Add more carriers** (UnitedHealth, Aetna, etc.)
- **Implement OCR** for complex document parsing
- **Add SMS notifications** for urgent cards
- **Create client portal** for self-service access

### Performance Improvements
- **Parallel processing** for multiple carriers
- **Intelligent retry scheduling** based on carrier patterns
- **Predictive failure detection** using ML
- **API response caching** where appropriate

## 💰 Cost Analysis

### Make.com Operations
- **Email processing**: ~1,000 operations/month
- **Sheet operations**: ~2,000 operations/month
- **HTTP requests**: ~500 operations/month
- **Total estimated**: 3,500 operations/month

### External Services
- **Browserless.io**: $29/month for 1,000 requests
- **Cloud hosting**: $10-20/month for Python service
- **Total estimated**: $40-50/month

### ROI Calculation
- **Time saved**: 10 minutes per ID card × 100 cards/month = 16.7 hours/month
- **Cost savings**: 16.7 hours × $25/hour = $417.50/month
- **Net savings**: $417.50 - $50 = $367.50/month

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- **Weekly**: Review error logs and success rates
- **Monthly**: Update carrier credentials if needed
- **Quarterly**: Security audit and credential rotation
- **Annually**: Full system review and optimization

### Escalation Process
1. **Level 1**: Automated retry and error handling
2. **Level 2**: Manual queue processing by operations team
3. **Level 3**: Technical team involvement for system issues
4. **Level 4**: Vendor support for carrier portal changes

---

## 🎯 Success Criteria

### Go-Live Success
- **85%+ automated retrieval rate** in first month
- **Zero data breaches** or security incidents
- **<2 minute average** processing time per card
- **95%+ client satisfaction** with delivery experience

### Long-term Success
- **90%+ automation rate** within 6 months
- **Expansion to 10+ carriers** within 1 year
- **Integration with agency management system**
- **Client self-service portal** deployment

---

*This automation represents a significant advancement in client service delivery for CJS Insurance Solutions, providing immediate value while establishing a foundation for future digital transformation initiatives.*