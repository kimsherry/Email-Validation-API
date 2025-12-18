from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import re
import json

app = FastAPI(
    title="Email Validation API",
    description="Email validation + domain blocking + JSON logging",
    version="1.1.0"
)

EMAIL_REGEX = re.compile(
    r"^(?=.{1,254}$)(?=.{1,64}@)[A-Za-z0-9._%+-]+@"
    r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$"
)

# Blocked Domains
BLOCKED_DOMAINS: List[str] = [
    "gmail.com",
    "naver.com",
]

LOG_FILE = "logs.jsonl"


# Models 

class EmailRequest(BaseModel):
    email: str


# Utils

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def is_blocked_domain(email: str) -> bool:
    domain = email.split("@")[1].lower()
    return any(
        domain == blocked or domain.endswith("." + blocked)
        for blocked in BLOCKED_DOMAINS
    )


def get_client_ip(request: Request) -> str:
    return request.headers.get(
        "x-forwarded-for",
        request.client.host
    ).split(",")[0].strip()


def write_log(ip: str, email: str, result: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": ip,
        "email": email,
        "result": result
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


# API

@app.post("/validate/email")
async def validate_email(request: Request, body: EmailRequest):
    ip = get_client_ip(request)
    email = body.email.strip()

    if not is_valid_email(email):
        write_log(ip, email, "INVALID_FORMAT")
        return {"valid": False}

    if is_blocked_domain(email):
        write_log(ip, email, "BLOCKED_DOMAIN")
        return {"valid": False}

    write_log(ip, email, "OK")
    return {"valid": True}
