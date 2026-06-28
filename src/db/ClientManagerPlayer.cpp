


#ifdef ENABLE_BATTLEPASS_SYSTEM
	CDBManager::instance().EscapeString(text, pkTab->iBattlePassDailyMissions, sizeof(pkTab->iBattlePassDailyMissions));
	queryLen += snprintf(pszQuery + queryLen, querySize - queryLen, "battlepass_daily_missions = '%s', ", text);
	
	CDBManager::instance().EscapeString(text, pkTab->iBattlePassWeeklyMissions, sizeof(pkTab->iBattlePassWeeklyMissions));
	queryLen += snprintf(pszQuery + queryLen, querySize - queryLen, "battlepass_weekly_missions = '%s', ", text);
	
	CDBManager::instance().EscapeString(text, pkTab->iBattlePassPlayerData, sizeof(pkTab->iBattlePassPlayerData));
	queryLen += snprintf(pszQuery + queryLen, querySize - queryLen, "battlepass_player_data = '%s', ", text);
#endif

// Awlways Add Things Above This Line !!
	CDBManager::instance().EscapeString(text, pkTab->quickslot, sizeof(pkTab->quickslot));
	queryLen += snprintf(pszQuery + queryLen, querySize - queryLen, "quickslot = '%s' ", text);

	queryLen += snprintf(pszQuery + queryLen, querySize - queryLen, " WHERE id=%d", pkTab->id);
	return queryLen;
}





/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////



	else
	{
		sys_log(0, "[PLAYER_LOAD] Load from PlayerDB pid[%d]", packet->player_id);

		char queryStr[QUERY_MAX_LEN];

		//--------------------------------------------------------------

		//--------------------------------------------------------------
		snprintf(queryStr, sizeof(queryStr),
				"SELECT "
				"id,name,job,voice,dir,x,y,z,map_index,exit_x,exit_y,exit_map_index,hp,mp,stamina,random_hp,random_sp,playtime,"
				"gold,level,level_step,st,ht,dx,iq,exp,"
				"stat_point,skill_point,sub_skill_point,stat_reset_count,part_base,part_hair,"
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
				"part_acce, "
#endif
#ifdef ENABLE_BATTLEPASS_SYSTEM
				"battlepass_daily_missions, "
				"battlepass_weekly_missions, "
				"battlepass_player_data, "
#endif







/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////




	if (row[col])
		thecore_memcpy(pkTab->skills, row[col], sizeof(pkTab->skills));
	else
		memset(&pkTab->skills, 0, sizeof(pkTab->skills));

	col++;


#ifdef ENABLE_BATTLEPASS_SYSTEM
	if (row[col])
		memcpy(pkTab->iBattlePassDailyMissions, row[col], sizeof(pkTab->iBattlePassDailyMissions));
	else
		memset(pkTab->iBattlePassDailyMissions, 0, sizeof(pkTab->iBattlePassDailyMissions));
	
	col++;
	if (row[col])
		memcpy(pkTab->iBattlePassWeeklyMissions, row[col], sizeof(pkTab->iBattlePassWeeklyMissions));
	else
		memset(pkTab->iBattlePassWeeklyMissions, 0, sizeof(pkTab->iBattlePassWeeklyMissions));
	
	col++;
	if (row[col])
		memcpy(pkTab->iBattlePassPlayerData, row[col], sizeof(pkTab->iBattlePassPlayerData));
	else
		memset(pkTab->iBattlePassPlayerData, 0, sizeof(pkTab->iBattlePassPlayerData));
	
	col++;
#endif

	if (row[col])
		thecore_memcpy(pkTab->quickslot, row[col], sizeof(pkTab->quickslot));
	else
		memset(pkTab->quickslot, 0, sizeof(pkTab->quickslot));

	col++;

	str_to_number(pkTab->skill_group, row[col++]);
	str_to_number(pkTab->lAlignment, row[col++]);