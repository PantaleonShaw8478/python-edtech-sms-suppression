from datetime import date, timedelta

from src.course_delivery import Course, Learner, ReminderService


class FakeSms:
    def __init__(self):
        self.calls = []

    def send(self, to, message):
        self.calls.append((to, message))
        return {"message_id": "msg-1"}


def test_opted_out_learner_is_skipped_before_send():
    sender = FakeSms()
    service = ReminderService(sender)
    course = Course("c1", "Algebra", date(2026, 9, 7))
    learner = Learner("l1", "+15550001", opted_out=True)
    result = service.remind(course, learner, today=date(2026, 9, 4))
    assert result["status"] == "skipped"
    assert sender.calls == []


def test_deadline_reminder_returns_message_id():
    sender = FakeSms()
    result = ReminderService(sender).remind(Course("c1", "Algebra", date(2026, 9, 7)), Learner("l1", "+15550001"), date(2026, 9, 4))
    assert result == {"status": "sent", "learner_id": "l1", "message_id": "msg-1"}
