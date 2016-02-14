from datetime import date
from datetime import datetime
import calendar


# This function constructs a file name string using a UTC timestamp
def get_next_filename():
    today = date.today()

    time_now = datetime.utcnow().strftime('%Y %m %d %H %M %S')

    time_pieces = time_now.split(' ')

    minutes = int(time_pieces[4])

    minutes_over_half = minutes % 30

    half_hour = minutes - minutes_over_half

    return 'KSBP2-' + calendar.month_abbr[int(time_pieces[1])] + '-' +  time_pieces[2] + '-' + time_pieces[0] + '-' + time_pieces[3] + '{0:02d}'.format(half_hour) + 'Z.mp3'
