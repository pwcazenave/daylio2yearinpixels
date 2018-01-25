from __future__ import division

import sys
import pandas as pd
import numpy as np
import calendar

from datetime import datetime


def read_daylio(filename):
    """
    Read the daylio exported data.

    Return the dates and numeric mood.

    """

    # Manually specify the column headers so we can handle irregular number of
    # columns (terrible, terrible output formatting from daylio).
    columns = ['year', 'date', 'day', 'time', 'mood', 'activities', 'note']
    mood = pd.read_csv(filename, names=columns, skiprows=1)

    # Convert the horrible dates to datetimes.
    daymonth = [i.split(' ') for i in mood['date']]
    dates = np.column_stack((mood['year'].astype(str),
                             ['{:02d} {}'.format(int(i[0]), i[1]) for i in daymonth]))
    horrid = '%Y %d %B'
    dates = [datetime.strptime(' '.join(i), horrid) for i in dates]

    # Convert mood to a numeric value (higher = better).
    convert = {'rad': 5,
               'good': 4,
               'meh': 3,
               'fugly': 2,
               'awful': 1}
    for entry in convert:
        mood[mood['mood'] == entry] = convert[entry]

    return dates, mood['mood'].tolist()


def write_year_in_pixels(daylio, output, year=None):
    """
    Take the output of read_daylio() and export it to the format expected by
    Year in Pixels.

    Parameters
    ----------
    daylio : tuple
        Tuple of dates (as datetime objects) and the recorded Daylio moods as
        numbers (low = bad, high = good).
    output : str
        File name to which to save the output.
    year : int, optional
        The year we're extracting from the Daylio output. If omitted, uses the
        year from the first entry in daylio.

    """

    # Year in Pixels wants the data shaped as a single line of digits, where
    # zero represents no data. Should be easy enough.

    if not year:
        year = daylio[0][0].year

    # Year in Pixels doesn't support leap days.
    yip = np.zeros(365)

    for (day, felt) in zip(daylio[0], daylio[1]):
        if day.year == year:
            # Year in Pixels doesn't support leap days, so drop them here.
            if calendar.isleap(year) and day.month == 2 and day.day == 28:
                print('Skipping leap day.')
                pass

            # 1st of January needs to be 0, not 1
            dayofyear = int(day.strftime('%j')) - 1

            # We have to remove a day to the index to account for Life in
            # Pixels not supporting leap years, but only in leap years.
            if calendar.isleap(year):
                if day.month >= 2 and dayofyear > 60:
                    dayofyear -= 1

            yip[dayofyear] = felt

    np.savetxt(output, yip, '%d', newline='')


if __name__ == '__main__':

    daylio = read_daylio(sys.argv[1])
    write_year_in_pixels(daylio, sys.argv[2], year=2017)

