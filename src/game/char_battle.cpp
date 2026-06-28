




#ifdef ENABLE_BATTLEPASS_SYSTEM
	pkAttacker->SetBattlePassProgress(BATTLEPASS_GET_GOLD, iTotalGold);
#endif
	DBManager::instance().SendMoneyLog(MONEY_LOG_MONSTER, GetRaceNum(), iTotalGold);
}




#ifdef ENABLE_BATTLEPASS_SYSTEM
		owner->SetBattlePassProgress(BATTLEPASS_GET_ITEM, item->GetCount());
#endif
		item->AddToGround(GetMapIndex(), pos);
#ifdef ENABLE_DICE_SYSTEM
		if (owner->GetParty()) 
		{
			FPartyDropDiceRoll f(item, owner);
			f.Process(this);
		} 
		else
		{
			item->SetOwnership(owner);
		}
#else
		item->SetOwnership(owner);
#endif
		item->StartDestroyEvent();

		// Update position for next drop
		pos.x = GetX() + number(-7, 7) * 20;
		pos.y = GetY() + number(-7, 7) * 20;
		sys_log(0, "DROP_ITEM: %s %d %d by %s", item->GetName(), pos.x, pos.y, GetName());
	};
	
	
	
	if (pkKiller && pkKiller->IsPC())
	{
		if (pkKiller->m_pkChrTarget == this)
			pkKiller->SetTarget(nullptr);

		if (!IsPC() && pkKiller->GetDungeon())
			pkKiller->GetDungeon()->IncKillCount(pkKiller, this);

		isAgreedPVP = CPVPManager::instance().Dead(this, pkKiller->GetPlayerID());

		if (IsPC())
		{
			CGuild * g1 = GetGuild();
			CGuild * g2 = pkKiller->GetGuild();

			if (g1 && g2)
				if (g1->UnderWar(g2->GetID()))
					isUnderGuildWar = true;

			pkKiller->SetQuestNPCID(GetVID());
			quest::CQuestManager::instance().Kill(pkKiller->GetPlayerID(), quest::QUEST_NO_NPC);
			CGuildManager::instance().Kill(pkKiller, this);
#ifdef ENABLE_BATTLEPASS_SYSTEM
			if (pkKiller->GetLevel() - GetLevel() <= BATTLEPASS_MIN_LEVEL_GAP)
				pkKiller->SetBattlePassProgress(BATTLEPASS_KILL_PLAYERS);
#endif
		}
	}
	else // if you don't have this branch add it yourself
	{
		#ifdef ENABLE_BATTLEPASS_SYSTEM
			if (pkKiller->GetLevel() - GetLevel() <= BATTLEPASS_MIN_LEVEL_GAP)
			{
				if (IsStone()) {
					pkKiller->SetBattlePassProgress(BATTLEPASS_KILL_STONE);
				}
				else {
					bool isBoss = GetMobRank() == MOB_RANK_BOSS;
					if (pkKiller->GetDungeon()) {
						pkKiller->SetBattlePassProgress((isBoss) ? BATTLEPASS_KILL_DUNGEON : BATTLEPASS_KILL_MONSTER);
					}
					else {
						pkKiller->SetBattlePassProgress((isBoss) ? BATTLEPASS_KILL_BOSS : BATTLEPASS_KILL_MONSTER);
					}
				}
			}
		#endif
	}