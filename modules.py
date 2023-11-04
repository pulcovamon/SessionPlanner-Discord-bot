from datetime import date, timedelta


class SessionPlanner(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionPlanner, cls).__new__(cls)
        return cls.instance

    def __str__(self) -> str:
        return f"vote from: {self.calendar[0]}, to: {self.calendar[-1]}"

    def set_calendar(self, from_date, to_date):
        if not from_date:
            from_date = date.today()
        if not to_date:
            to_date = from_date + timedelta(days=6)
        self.calendar = []
        delta = timedelta(days=1)

        while from_date <= to_date:
            self.calendar.append(from_date)
            from_date += delta

    def get_calendar(self):
        if not self.calendar:
            return None
        calendar_text = []
        space = "\u00A0"
        for day in self.calendar:
            calendar_text.append(
                f"{day.strftime('%A')}{space}{day.day}.{space}{day.month}.{space}{day.year}"
            )
        return calendar_text
