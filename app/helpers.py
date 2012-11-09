from datetime import datetime, timedelta


def time_ago(date):

    if date is None:
        return

    diff = datetime.now() - date
    delta = "a few moments ago"

    if diff.days:
        years = diff.days / 365
        if years:
            delta = "%s years ago" % str(years)
        elif (diff.days / 30):
            delta = "%s months ago" % str(diff.days / 30)
        elif (diff.days / 7):
            delta = "%s weeks ago" % str(diff.days / 7)
        else:
            delta = "%s days ago" % str(diff.days)
    else:
        if (diff.seconds / 3600):
            delta = "%s hours ago" % str(diff.seconds / 3600)
        elif (diff.seconds / 60):
            delta = "%s minutes ago" % str(diff.seconds / 60)

    return delta
