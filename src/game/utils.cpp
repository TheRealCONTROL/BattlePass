

// add all of this

time_t GetTimeToNextWeekend()
{
	const time_t cur_Time = time(0);
	struct tm vKey = *localtime(&cur_Time);
	
	vKey.tm_sec = 0;
	vKey.tm_min = 0;
	vKey.tm_hour = 0;
	
	// Thursday is day 4 (0 = Sunday, 1 = Monday, ..., 4 = Thursday)
	if (vKey.tm_wday < 4) {
		// If current day is before Thursday, calculate days until Thursday
		vKey.tm_mday += 4 - vKey.tm_wday;
	} else {
		// If current day is Thursday or after, calculate days until next Thursday
		vKey.tm_mday += 7 - (vKey.tm_wday - 4);
	}
	
	time_t nextThursdayTimestamp = mktime(&vKey);
	return nextThursdayTimestamp - cur_Time;
}
time_t GetTimeToNextDay()
{
	const time_t cur_Time = time(0);
	struct tm vKey = *localtime(&cur_Time);

	// Set to the next day
	vKey.tm_sec = 0;
	vKey.tm_min = 0;
	vKey.tm_hour = 0;
	vKey.tm_mday += 1;

	time_t nextDayTimestamp = mktime(&vKey);

	// Calculate the time difference in seconds
	return nextDayTimestamp - cur_Time;
}

time_t GetTimeToNextWeek() 
{
	const time_t cur_Time = time(0);
	struct tm vKey = *localtime(&cur_Time);

	// Set to the next week (7 days later)
	vKey.tm_sec = 0;
	vKey.tm_min = 0;
	vKey.tm_hour = 0;
	vKey.tm_mday += 7 - vKey.tm_wday; // Adjust to the start of the next week

	time_t nextWeekTimestamp = mktime(&vKey);

	// Calculate the time difference in seconds
	return nextWeekTimestamp - cur_Time;
}

time_t GetTimeToNextMonth()
{
	const time_t cur_Time = time(0);
	const struct tm vKey = *localtime(&cur_Time);
	int currentMonth = vKey.tm_mon;

	// Calculate the next month
	int nextMonth = currentMonth + 1;
	int nextYear = vKey.tm_year + 1900;
	if (nextMonth > 11) {
		nextMonth = 0; // Wrap around to January
		nextYear++; // Increment the year
	}

	struct tm nextMonthTime = {0};
	nextMonthTime.tm_sec = 0;
	nextMonthTime.tm_min = 0;
	nextMonthTime.tm_hour = 0;
	nextMonthTime.tm_mday = 1;
	nextMonthTime.tm_mon = nextMonth;
	nextMonthTime.tm_year = nextYear - 1900;

	time_t nextMonthTimestamp = mktime(&nextMonthTime);

	// Calculate the time difference in seconds
	return nextMonthTimestamp - cur_Time;
}

int GetDayIndex()
{
	time_t now = get_global_time();
	struct tm* timeinfo = localtime(&now);
	return timeinfo->tm_wday;
}

int GetWeekIndex()
{
	time_t now = get_global_time();
	struct tm* timeinfo = localtime(&now);

	int year = timeinfo->tm_year + 1900;

	struct tm startOfYear = {0};
	startOfYear.tm_year = timeinfo->tm_year;
	startOfYear.tm_mon  = 0;
	startOfYear.tm_mday = 1;

	time_t tStartOfYear = mktime(&startOfYear);
	int daysSinceYearStart = static_cast<int>((now - tStartOfYear) / 86400);

	int weekOfYear = daysSinceYearStart / 7;

	return year * 100 + weekOfYear;
}

int GetMonthIndex()
{
	time_t now = get_global_time();

	struct tm timeinfo;
	localtime_r(&now, &timeinfo);

	return timeinfo.tm_mon;
}

time_t GetFirstDayHour()
{
	time_t now = get_global_time();
	struct tm * time_struct = localtime(&now);
	time_struct->tm_hour = 0;
	time_struct->tm_min = 0;
	time_struct->tm_sec = 0;

	time_t time_stamp_hour = mktime(time_struct);
	return time_stamp_hour;
}
