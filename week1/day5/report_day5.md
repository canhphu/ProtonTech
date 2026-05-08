# Report Day 5 - AI Email Summarizer

## Tong quan san pham
Project hoan thien gom CLI nhan email dau vao (file hoac stdin) va tra ve JSON co cau truc: summary (3-5 cau), action_items, priority, people. Co error handling co ban va test unit.

## Lenh da chay
```bash
python email_summarizer.py --input samples/email_1.txt
Get-Content samples/email_2.txt | python email_summarizer.py
python email_summarizer.py --input samples/email_1.txt --output output.json
```

## Ket qua mau
### Email 1
```json
{
  "summary": "This email is a follow-up to a recent weekly sync meeting. The team is requested to review an attached proposal and provide feedback by Friday at 3 PM. Minh will be responsible for updating the project timeline and distributing the revised plan. Lan will schedule a follow-up meeting for next Tuesday to discuss further.",
  "action_items": [
    "Review the attached proposal",
    "Send feedback on the proposal by Friday 3 PM",
    "Minh to update the timeline",
    "Minh to share the revised plan",
    "Lan to schedule a follow-up meeting for next Tuesday"
  ],
  "priority": "medium",
  "people": [
    "Minh",
    "Lan"
  ]
}
```

### Email 2
```json
{
  "summary": "The support team has been notified about intermittent failures occurring when customers attempt to pay with Visa cards. This issue has seen a significant spike in error rates following the most recent deployment. An urgent investigation is required to identify the root cause of these payment processing problems. An update on the situation is expected today.",
  "action_items": [
    "Investigate intermittent Visa card payment failures.",
    "Provide an update today.",
    "Loop in Thu from finance to confirm impacted transactions."
  ],
  "priority": "high",
  "people": [
    "Quang",
    "Thu"
  ]
}
```

## Kiem tra yeu cau
- Nhan email dau vao (text/file/stdin): Done
- Tra ve tom tat 3-5 cau: Done
- Action items, priority, people: Done
- Output JSON co cau truc: Done
- Error handling co ban: Done

## Ghi chu
- Output file da duoc tao: output.json
