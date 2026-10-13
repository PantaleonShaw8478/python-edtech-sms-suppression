import os
from datetime import date, timedelta

from .course_delivery import Course, Learner, ReminderService
from .infrai_sms import InfraiSms


def main():
    learner = Learner("learner-7", os.environ.get("LEARNER_PHONE", "+15551234567"))
    course = Course("python-101", "Python foundations", date.today() + timedelta(days=3))
    result = ReminderService(InfraiSms()).remind(course, learner)
    print(result)


if __name__ == "__main__":
    main()
