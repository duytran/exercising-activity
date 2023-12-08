def time_to_seconds(time_str):
    total_seconds = 0
    try:
        # split the time string to hours, minutes and seconds
        hours, minutes, seconds = map(int, time_str.split(":"))
        # calculator the numberical representation
        total_seconds = (hours * 60 * 60) + (minutes * 60) + seconds
    except:
        print("Exeptions")

    return total_seconds


def parse_seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return hours, minutes, remaining_seconds
