from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Course:
    course_id: str
    title: str
    deadline: date


@dataclass(frozen=True)
class Learner:
    learner_id: str
    phone: str
    opted_out: bool = False


class ReminderService:
    def __init__(self, sms_sender, suppressed_numbers=None):
        self.sms_sender = sms_sender
        self.suppressed_numbers = set(suppressed_numbers or ())

    def remind(self, course, learner, today=None):
        today = today or date.today()
        days_left = (course.deadline - today).days
        if learner.opted_out or learner.phone in self.suppressed_numbers:
            return {"status": "skipped", "reason": "suppressed", "learner_id": learner.learner_id}
        if days_left < 0 or days_left > 7:
            return {"status": "skipped", "reason": "outside_window", "learner_id": learner.learner_id}
        message = f"{course.title} deadline is {course.deadline.isoformat()} ({days_left} days left)."
        result = self.sms_sender.send(learner.phone, message)
        return {"status": "sent", "learner_id": learner.learner_id, "message_id": result.get("message_id")}

    def educator_report(self, results):
        return {"sent": sum(r["status"] == "sent" for r in results), "skipped": sum(r["status"] == "skipped" for r in results)}
