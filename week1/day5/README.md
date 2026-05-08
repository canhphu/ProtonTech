# AI Email Summarizer

Mini project: nhan email dau vao, tra ve tom tat (3-5 cau), action items, muc do uu tien va nguoi lien quan. Output la JSON co cau truc.

## Yeu cau
- Python 3.10+ (khuyen nghi)
- API key trong `.env`

## Cai dat
```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

## Cau hinh
Tao file `.env`:
```
GEMINI_API_KEY = 
```

## Cach chay
Doc tu file:
```bash
python email_summarizer.py --input samples/email_1.txt
```

Doc tu stdin:
```bash
Get-Content samples/email_2.txt | python email_summarizer.py
```

Ghi output ra file:
```bash
python email_summarizer.py --input samples/email_1.txt --output output.json
```

## Dinh dang output
```json
{
  "summary": "...",
  "action_items": ["..."],
  "priority": "low|medium|high",
  "people": ["..."]
}
```

## Test nhanh
```bash
python -m unittest discover -s tests
```

## Ghi chu
- Neu response khong phai JSON, tool se co gang trich xuat JSON va bao loi neu that bai.
- Co the thay doi model bang `--model` hoac env var `OPENAI_MODEL`.
