


	if (test_server && (iPulse % PASSES_PER_SEC(60)) == 0)
	{
		sys_log(0, "CHARACTER COUNT vid %zu pid %zu", m_map_pkChrByVID.size(), m_map_pkChrByPID.size());
	}

#ifdef ENABLE_BATTLEPASS_SYSTEM
	if ((iPulse % PASSES_PER_SEC(60)) == 0)
		ResetBattlePass();
#endif
	FlushPendingDestroy();
}


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////




#ifdef ENABLE_BATTLEPASS_SYSTEM
void CHARACTER_MANAGER::ResetBattlePass()
{
	const auto currentTime = get_global_time();
	const auto currentMonthIndex = GetMonthIndex();

	const auto dailyResetRemaining =
		quest::CQuestManager::instance().GetEventFlag("daily_battlepass_time") - currentTime;

	const auto weeklyResetRemaining =
		quest::CQuestManager::instance().GetEventFlag("weekly_battlepass_time") - currentTime;

	const auto storedMonthIndex =
		quest::CQuestManager::instance().GetEventFlag("month_battlepass_index");

	const bool needsDailyReset = dailyResetRemaining <= 0;
	const bool needsWeeklyReset = weeklyResetRemaining <= 0;
	const bool needsMonthlyReset = storedMonthIndex != currentMonthIndex;

	if (!needsDailyReset && !needsWeeklyReset && !needsMonthlyReset)
		return;

	if (g_bChannel == 99)
	{
		if (needsDailyReset)
			quest::CQuestManager::instance().RequestSetEventFlag("daily_battlepass_time", currentTime + GetTimeToNextDay());

		if (needsWeeklyReset)
			quest::CQuestManager::instance().RequestSetEventFlag("weekly_battlepass_time", currentTime + GetTimeToNextWeek());

		if (needsMonthlyReset)
			quest::CQuestManager::instance().RequestSetEventFlag("month_battlepass_index", currentMonthIndex);
	}

	for (const auto& desc : DESC_MANAGER::instance().GetClientSet())
	{
		LPCHARACTER ch = desc->GetCharacter();
		if (!ch)
			continue;

		if (needsDailyReset || needsWeeklyReset)
			ch->CheckBattlePassTimers(true);

		if (needsMonthlyReset)
			ch->ResetPlayerMonth(true);
	}
}
#endif