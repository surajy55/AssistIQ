import datetime

def get_date_time(request):
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")

    if "date" in request and "time" in request:
        response = f"Today is {date} and the current time is {time}."
    elif "date" in request:
        response = f"Today's date is {date}."
    elif "time" in request:
        response = f"The current time is {time}."
    else:
        response = "I'm not sure whether you wanted the date or time. Could you please clarify?"

    return response
