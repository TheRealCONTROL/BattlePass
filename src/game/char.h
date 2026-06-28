



#ifdef ENABLE_BATTLEPASS_SYSTEM
	private:
		void 						SendBattlePassPlayerData();
		void 						SendBattlePassRewards();
		void 						SendBattlePassMissions(bool isDaily);
		
	public:
		void 						CheckBattlePassTimers(bool isSend);
		void 						OnLoginBattlePass();
		void 						ResetPlayerMonth(bool isSend);
		void 						ResetMission(bool isDaily, bool isSend);
		void 						SetBattlePassProgress(uint8_t iType, uint32_t iValue = 1);
		void 						SetBattlePassExp(uint16_t iExp);
		void 						GetBattlePassReward(bool Primium);
		void 						SetPrimiumUpgrade();
		void 						SetBattlePassLevelUp();
		void						BattlepassMissionSkip(bool isDaily);
		void 						ResetBattlepassMission(uint8_t iSlot, bool isDaily);

	private:
		//////////////// System Data /////////////////
		int* 						GetBattlePassDailyMissions();
		int 						m_iBattlePassDailyMissions[BATTLEPASS_MAX_MISSION_COUNT][BATTLEPASS_MISSION_INFO_MAX];

		int* 						GetBattlePassWeeklyMissions();
		int 						m_iBattlePassWeeklyMissions[BATTLEPASS_MAX_MISSION_COUNT][BATTLEPASS_MISSION_INFO_MAX];

		int* 						GetBattlePassPlayerData();
		int 						m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MAX];
		//////////////// System Data /////////////////
#endif

};

ESex GET_SEX(LPCHARACTER ch);

