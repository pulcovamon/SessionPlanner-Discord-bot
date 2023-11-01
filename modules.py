from datetime import date, timedelta

class SessionPlanner:
    def __init__(self, from_date, to_date):
        """_summary_

        Args:
            from_date (_type_, optional): _description_. Defaults to date.today().
            to_date (_type_, optional): _description_. Defaults to date.today+timedelta(days=7).
        """
        if not from_date:
            from_date = date.today()
        if not to_date:
            to_date = from_date + timedelta(days=7)
        self.calendar = []
        delta = timedelta(days=1)
        
        while from_date <= to_date:
            self.calendar.append(from_date)
            from_date += delta
            
    def __str__(self) -> str:
        return f"from: {self.calendar[0]}, to: {self.calendar[-1]}"
    
    def get_calendar(self):
        calendar_text = ""
        space = u"\u00A0"
        for day in self.calendar:
            calendar_text += f"{day.day}.{space}{day.month}.{space}{day.year}\n\n"
        return calendar_text