

	short	stat_reset_count;

	DWORD	logoff_interval;

	int		aiPremiumTimes[PREMIUM_MAX_NUM];

#ifdef ENABLE_BATTLEPASS_SYSTEM
	int 	iBattlePassDailyMissions[BATTLEPASS_MAX_MISSION_COUNT][BATTLEPASS_MISSION_INFO_MAX];
	int 	iBattlePassWeeklyMissions[BATTLEPASS_MAX_MISSION_COUNT][BATTLEPASS_MISSION_INFO_MAX];
	int 	iBattlePassPlayerData[BATTLEPASS_PLAYER_MAX];
#endif

} TPlayerTable;