from datetime import datetime, timedelta

def get_next_dose_time(medication,reminders):
    now = datetime.now()
    start_date = medication.start_date
    end_date = medication.end_date
    frequency = medication.frequency

    if not start_date or not frequency:
        return None

    try:
        frequency = int(frequency)
    except ValueError:
        frequency = 1  # Default to once per day if frequency is not a number

    # Calculate the next dose date based on frequency
    days_since_start = (now.date() - start_date).days
    if days_since_start < 0:
        # Medication hasn't started yet
        next_dose_date = start_date
    else:
        next_dose_date = start_date + timedelta(days=days_since_start + 1)

    # Check if the medication has ended
    if end_date and next_dose_date > end_date:
        return None

    # Get the earliest reminder time for the medication
    
    if reminders:
        earliest_reminder_time = min(reminder.reminder_time for reminder in reminders)
    else:
        # Default to 09:00 if no reminders are set
        earliest_reminder_time = datetime.strptime("09:00", "%H:%M").time()

    next_dose_time = datetime.combine(next_dose_date, earliest_reminder_time)

    return next_dose_time