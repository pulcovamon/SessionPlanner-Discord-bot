from datetime import date, timedelta

class SessionPlanner:
    def __init__(self, from_date=date.today(), to_date=date.today+timedelta(days=7)):
        """_summary_

        Args:
            from_date (_type_, optional): _description_. Defaults to date.today().
            to_date (_type_, optional): _description_. Defaults to date.today+timedelta(days=7).
        """
        self.calendar = []
        delta = timedelta(days=1)
        
        while from_date <= to_date:
            self.calendar.append(from_date)
            from_date += delta