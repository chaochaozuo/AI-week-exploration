# Weekend Email -> Slack Alerts (Zapier)

This repository documents a ready-to-configure Zapier workflow that posts Slack alerts only when emails arrive on weekends.

## Goal

When a new email is received on **Saturday** or **Sunday**, send a Slack alert that includes an `@ai-analytics` reference.

## Zap Configuration

### 1) Trigger: New Email

Choose one of these trigger apps based on your mailbox:

- **Gmail** -> `New Email` (or `New Email Matching Search`)
- **Microsoft Outlook** -> `New Email`
- **IMAP by Zapier** -> `New Email`

Recommended trigger settings:

- Watch the inbox (or a specific label/folder).
- If available, fetch subject, sender, received time, and snippet/body preview.

### 2) Formatter: Extract Day of Week

Add **Formatter by Zapier**:

- Event: `Date / Time`
- Transform: `Format`
- Input: `{{zap_meta_human_now}}`
- To Format: `dddd`
- To Timezone: your local timezone (for example, `America/New_York`)

This creates a weekday value like `Saturday`, `Sunday`, `Monday`, etc.

### 3) Filter: Weekend Only

Add **Filter by Zapier** and configure **ANY** of the following conditions:

- Formatted weekday `Exactly matches` `Saturday`
- Formatted weekday `Exactly matches` `Sunday`

If false, the Zap stops and no Slack message is sent.

### 4) Action: Send Slack Message

Add **Slack** action:

- Event: `Send Channel Message` (or `Send Direct Message`)
- Select destination channel (for example `#alerts-email-weekend`)
- Message text template:

```text
@ai-analytics Weekend email alert

From: {{From Name}} <{{From Email}}>
Subject: {{Subject}}
Received: {{Date}}
Snippet: {{Body Plain}}
```

If your trigger does not provide all fields above, keep the ones it does provide.

## Optional Hardening

- Add a second **Filter** for importance (for example, sender domain, subject keywords).
- Add **Storage by Zapier** dedupe key (message ID) to avoid duplicate alerts.
- Use Slack thread replies if you want all weekend alerts grouped in one message thread.

## Test Checklist

1. Turn Zap on.
2. Send a test email to your inbox on a weekend (or temporarily disable weekend filter for testing).
3. Confirm Slack receives the alert and includes `@ai-analytics`.
4. Confirm weekday emails do not send alerts.

## Rule for Prompt and Message Templates

Always include `@ai-analytics` in automation prompt/message templates for this workflow.
