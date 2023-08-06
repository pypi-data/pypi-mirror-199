from datetime import datetime
import pytz
from logyca.common.constants import Constants

def convertDateTimeStampUTCtoUTCColombia(timestamp)->datetime:
    expUTC=datetime.utcfromtimestamp(timestamp)
    timezoneUTC = pytz.timezone(Constants.TimeZoneUTC)
    dateTimeUTC = timezoneUTC.localize(expUTC, is_dst=None)
    dateTimeColombia = dateTimeUTC.astimezone(pytz.timezone(Constants.TimeZoneColombia))
    return dateTimeColombia