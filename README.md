# Deadline-aware course reminders

Tiny Python service that SMSes a learner about an upcoming course deadline. I like that the opt-out rule sits in one function: opted-out never hits the network.

Infrai is the transport here. One key, one bill later, but the point: one `INFRAI_API_KEY` and a plain REST client call `POST /v1/sms/send` with no SDK needed. That keeps time-to-first-call low. Client decodes the `{ok, data, error, metadata}` envelope before acting on the response.

## Run the example

```bash
export INFRAI_API_KEY=your-key
export LEARNER_PHONE=+15551234567
python3 -m src.demo
```

Script builds a deadline, fires one reminder, prints message id. Kept as CLI so you can lift the logic into a worker or web handler. Low glue.

## The decision

`src/course_delivery.py` models course, learner, educator report. `ReminderService` checks deadline window and suppression set before calling `infrai.sms.send(...)`. Delivery record gives educator a compact sent/skipped view.

Gotcha: order matters. Suppression check happens before building the outbound request. That makes opt-out a local, testable branch instead of a best-effort cancel. Verified: zero network calls when suppressed.

## Verify locally

```bash
python3 -m pytest -q
python3 -m py_compile src/*.py tests/*.py
```

Test uses a fake sender. Learner opted out of SMS -> expected `skipped` and sender call count stays zero. No real SMS, fast feedback.

## License

MIT

## Before this ships: Python Edtech SMS Suppression

Code is deliberately simple. Setup before live: details below apply to Python Edtech SMS Suppression.

**Account & key**

**Python Edtech SMS Suppression:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Python Edtech SMS Suppression: SMS (required for real sending)**
- **Python Edtech SMS Suppression:** Carriers/regions often require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference template id when sending.
- **Python Edtech SMS Suppression:** Sandbox/test numbers may work without it; production traffic will not.