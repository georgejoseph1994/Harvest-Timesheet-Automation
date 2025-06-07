"""
Date utilities for handling workdays, weekends, and public holidays.
"""
from datetime import datetime, timedelta
from typing import List
import holidays


class DateUtils:
    """Utility class for date operations with holiday and weekend awareness."""

    def __init__(self, country: str = "AU", state: str = "VIC"):
        """
        Initialize DateUtils with holiday configuration.

        Args:
            country: Country code for holidays (default: "AU" for Australia)
            state: State/province code for regional holidays (default: "VIC" for Victoria/Melbourne)
        """
        self.country = country
        self.state = state
        self._holidays_cache = {}

    def get_holidays_for_year(self, year: int):
        """Get holidays for a specific year, with caching."""
        if year not in self._holidays_cache:
            self._holidays_cache[year] = holidays.country_holidays(
                self.country,
                state=self.state,
                years=year
            )
        return self._holidays_cache[year]

    def is_holiday(self, date: datetime) -> bool:
        """Check if a date is a public holiday."""
        year_holidays = self.get_holidays_for_year(date.year)
        return date.date() in year_holidays

    def is_workday(self, date: datetime) -> bool:
        """
        Check if a date is a workday (not weekend and not a public holiday).

        Args:
            date: The date to check

        Returns:
            True if the date is a workday, False otherwise
        """
        # Check if it's a weekend (Saturday=5, Sunday=6)
        if date.weekday() >= 5:
            return False

        # Check if it's a public holiday
        if self.is_holiday(date):
            return False

        return True

    def get_current_week_dates(self, verbose: bool = True) -> List[datetime]:
        """Get workdays for the current week (Monday to Friday, excluding holidays)."""
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        week_dates = [monday + timedelta(days=i) for i in range(5)]
        workdays = [date for date in week_dates if self.is_workday(date)]

        if verbose:
            skipped_dates = [date for date in week_dates if not self.is_workday(date)]
            if skipped_dates:
                print("Note: Skipping the following non-workdays in current week:")
                for date in skipped_dates:
                    reasons = []
                    if self.is_holiday(date):
                        holiday_name = self.get_holiday_name(date)
                        reasons.append(f"holiday ({holiday_name})")
                    reason_text = ', '.join(reasons) if reasons else "holiday"
                    print(f"  {date.strftime('%d/%m/%Y')} ({date.strftime('%A')}) - {reason_text}")
                print()

        return workdays

    def get_date_range(self, start_str: str, end_str: str, date_format: str = "%d/%m/%Y") -> List[datetime]:
        """
        Get all workdays between start and end dates (inclusive).

        Args:
            start_str: Start date as string
            end_str: End date as string
            date_format: Date format string (default: "%d/%m/%Y")

        Returns:
            List of datetime objects for workdays in the range
        """
        start = datetime.strptime(start_str, date_format)
        end = datetime.strptime(end_str, date_format)
        all_dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]
        return [date for date in all_dates if self.is_workday(date)]

    def get_holiday_name(self, date: datetime) -> str:
        """Get the name of the holiday for a given date, if it is a holiday."""
        year_holidays = self.get_holidays_for_year(date.year)
        return year_holidays.get(date.date(), "")

    def process_date_range(self, start_str: str, end_str: str, date_format: str = "%d/%m/%Y", verbose: bool = True) -> tuple:
        """
        Process a date range and return workdays with optional user feedback.

        Args:
            start_str: Start date as string
            end_str: End date as string
            date_format: Date format string (default: "%d/%m/%Y")
            verbose: Whether to print feedback to the user

        Returns:
            Tuple of (workdays_list, skipped_dates_info)
        """
        if verbose:
            print(f"Processing date range: {start_str} to {end_str}")

        start = datetime.strptime(start_str, date_format)
        end = datetime.strptime(end_str, date_format)

        # Calculate total days in range
        total_days = (end - start).days + 1
        all_dates = [start + timedelta(days=i) for i in range(total_days)]

        # Separate workdays and non-workdays
        workdays = []
        skipped_dates = []

        for date in all_dates:
            if self.is_workday(date):
                workdays.append(date)
            else:
                reason = []
                if date.weekday() >= 5:
                    reason.append("weekend")
                if self.is_holiday(date):
                    holiday_name = self.get_holiday_name(date)
                    reason.append(f"holiday ({holiday_name})")

                skipped_dates.append({
                    'date': date,
                    'reasons': reason
                })

        if verbose:
            print(f"Found {len(workdays)} workdays out of {total_days} total days")

            if skipped_dates:
                print("Skipping the following non-workdays:")
                for skip_info in skipped_dates:
                    date = skip_info['date']
                    reasons = ', '.join(skip_info['reasons'])
                    print(f"  {date.strftime('%d/%m/%Y')} ({date.strftime('%A')}) - {reasons}")
                print()

        return workdays, skipped_dates


# Default instance for Melbourne, Australia
melbourne_date_utils = DateUtils(country="AU", state="VIC")
