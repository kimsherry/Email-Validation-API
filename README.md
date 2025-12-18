# Email Validation API

**Fast API** 기반의 간단한 **REST API**로,
이메일 주소 형식 검증, 차단 도메인 관리, 요청 로그 기록 기능을 제공합니다.

API 학습용, 회원가입 전처리, 디스코드 인증봇 등
다른 서비스에 가볍게 통합하기 좋은 구조입니다.

---

## 기능

> 이메일 형식 검증합니다.
> 특정 도메인 차단 (스팸 / 임시 이메일 등)
> 요청 로그 기록 (IP, 이메일, 결과, 타임스탬프)
> JSON 기반 API 입니다.
> 로컬 실행이 가능합니다.

---

## 패키지 설치

```bash
pip install -r requirements.txt
```

---

## 사용방법

### API 서버에서 실행

```bash
uvicorn app.main:app --reload
```

---

## API 엔드포인트

### 이메일 검증

입력한 이메일이 형식상 유효한지 및
차단된 도메인인지를 검사합니다.

```bash
POST /validate/email
```

---

## 요청형식

### Headers

```https
Content-Type: application/json
```

### Body

```json
{
  "email": "test@example.com"
}

```

---

## 응답형식

### 정상 이메일

```json
{
  "valid": true
}

```

### 차단 도메인

```json
{
  "valid": false
}
```

### 잘못된 이메일 형식

```json
{
  "valid": false
}
```

---

## curl 사용 예시

```bash
curl -X POST http://127.0.0.1:8000/validate/email \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

---

## 로그기록

모든 요청은 `logs.jsonl` 파일에 **JSON Lines** 형식으로 기록됩니다.
(파일은 자동으로 생성됩니다.)

### 로그 예시

```json
{"timestamp":"2025-12-13T02:12:01Z","ip":"127.0.0.1","email":"user@example.com","result":"OK"}
```
파일이 없으면 자동 생성

---

## 차단 도메인 설정

```pyhon
BLOCKED_DOMAINS = [
    "gmail.com",
    "naver.com",
]
```
서브도메인까지 차단됩니다.

---
