


	m_fAttMul = 1.0f;
	m_fDamMul = 1.0f;

	m_pointsInstant.iDragonSoulActiveDeck = -1;

	memset(&m_tvLastSyncTime, 0, sizeof(m_tvLastSyncTime));
	m_iSyncHackCount = 0;

#ifdef ENABLE_BATTLEPASS_SYSTEM
	memset(&m_iBattlePassDailyMissions, 0, sizeof(m_iBattlePassDailyMissions));
	memset(&m_iBattlePassWeeklyMissions, 0, sizeof(m_iBattlePassWeeklyMissions));
	memset(&m_iBattlePassPlayerData, 0, sizeof(m_iBattlePassPlayerData));
#endif



/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


	if (dwPlayedTime > 60000)
	{
		const int gevinTime = dwPlayedTime / 60000;
		if (GetSectree() && !GetSectree()->IsAttr(GetX(), GetY(), ATTR_BANPK))
		{
			if (GetRealAlignment() < 0)
			{
				if (IsEquipUniqueItem(UNIQUE_ITEM_FASTER_ALIGNMENT_UP_BY_TIME))
					UpdateAlignment(120 * gevinTime);
				else
					UpdateAlignment(60 * gevinTime);
			}
			else
				UpdateAlignment(5 * gevinTime);
		}
#ifdef ENABLE_BATTLEPASS_SYSTEM
		SetBattlePassProgress(BATTLEPASS_PLAYTIME, MAX(1, (gevinTime / 60))); // Minutes
#endif
		SetRealPoint(POINT_PLAYTIME, GetRealPoint(POINT_PLAYTIME) + gevinTime);
		ResetPlayTime(dwPlayedTime % 60000);
	}

	
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


	tab.stamina = GetStamina();

	tab.sRandomHP = m_points.iRandomHP;
	tab.sRandomSP = m_points.iRandomSP;
	
	for (int i = 0; i < QUICKSLOT_MAX_NUM; ++i) {
		tab.quickslot[i] = m_pointsInstant.playerSlots->m_quickslot[i];

	std::memcpy(tab.parts, m_pointsInstant.parts, sizeof(tab.parts));
	std::memcpy(tab.skills, m_pSkillLevels.get(), sizeof(TPlayerSkill) * SKILL_MAX_NUM);

#ifdef ENABLE_BATTLEPASS_SYSTEM
	std::memcpy(tab.iBattlePassDailyMissions, GetBattlePassDailyMissions(), sizeof(tab.iBattlePassDailyMissions));
	std::memcpy(tab.iBattlePassWeeklyMissions, GetBattlePassWeeklyMissions(), sizeof(tab.iBattlePassWeeklyMissions));
	std::memcpy(tab.iBattlePassPlayerData, GetBattlePassPlayerData(), sizeof(tab.iBattlePassPlayerData));
#endif



/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////



	if (GetLevel() < PK_PROTECT_LEVEL)
		m_bPKMode = PK_MODE_PROTECT;

	std::memcpy(m_aiPremiumTimes, t->aiPremiumTimes, sizeof(t->aiPremiumTimes));

	m_dwLogOffInterval = t->logoff_interval;

	sys_log(0, "PLAYER_LOAD: %s PREMIUM %d %d, LOGGOFF_INTERVAL %u PTR: %p", t->name, m_aiPremiumTimes[0], m_aiPremiumTimes[1], t->logoff_interval, this);

#ifdef ENABLE_BATTLEPASS_SYSTEM
	std::memcpy(m_iBattlePassDailyMissions, t->iBattlePassDailyMissions, sizeof(m_iBattlePassDailyMissions));
	std::memcpy(m_iBattlePassWeeklyMissions, t->iBattlePassWeeklyMissions, sizeof(m_iBattlePassWeeklyMissions));
	std::memcpy(m_iBattlePassPlayerData, t->iBattlePassPlayerData, sizeof(m_iBattlePassPlayerData));
#endif


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////

#ifdef ENABLE_BATTLEPASS_SYSTEM
		SetBattlePassProgress(BATTLEPASS_ACCE_REFINE);
#endif
		TItemPos tPos;
		tPos.window_type = INVENTORY;
		tPos.cell = 0;

		TPacketAcce sPacket;
		sPacket.header = HEADER_GC_ACCE;
		sPacket.subheader = ACCE_SUBHEADER_CG_REFINED;
		sPacket.bWindow = m_bAcceCombination;
		sPacket.dwPrice = dwPrice;
		sPacket.bPos = 0;
		sPacket.tPos = tPos;
		sPacket.dwItemVnum = 0;
		sPacket.dwMinAbs = 0;
		if (bSucces)
			sPacket.dwMaxAbs = 100;
		else
			sPacket.dwMaxAbs = 0;

		GetDesc()->Packet(sPacket);
	}
	
	