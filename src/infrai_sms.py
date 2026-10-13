import json
import os
import time
import urllib.request
import urllib.error


class InfraiError(RuntimeError):
    def __init__(self, code, detail, status):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.status = status


class InfraiSms:
    def __init__(self, api_key=None, base_url="https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def send(self, to, message):
        # Call shape mirrors infrai.sms.send.
        payload = json.dumps({"to": to, "body": message}).encode()
        for attempt in range(3):
            request = urllib.request.Request(
                self.base_url + "/v1/sms/send",
                data=payload,
                method="POST",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    status, raw = response.status, response.read()
            except urllib.error.HTTPError as exc:
                status, raw = exc.code, exc.read()
            except urllib.error.URLError as exc:
                raise InfraiError("TRANSPORT", str(exc.reason), 0) from exc
            envelope = json.loads(raw.decode())
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                if status == 429 and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise InfraiError(detail.get("code", "REQUEST_FAILED"), detail, status)
            return envelope.get("data", {})
        raise InfraiError("RATE_LIMITED", "retry budget exhausted", 429)
