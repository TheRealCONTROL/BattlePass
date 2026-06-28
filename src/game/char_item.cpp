

// END_OF_REFINE_COST

#ifdef ENABLE_BATTLEPASS_SYSTEM
	if (GetLevel() - item->GetLevelLimit() <= BATTLEPASS_MIN_LEVEL_GAP)
		SetBattlePassProgress(BATTLEPASS_REFINE_ITEM);
#endif

	if (prob <= prt->prob)	
	{
		LPITEM pkNewItem = ITEM_MANAGER::instance().CreateItem(result_vnum, 1, 0, false);

		if (pkNewItem)
		{




/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////




	pkItemScroll->SetCount(pkItemScroll->GetCount() - 1);
#ifdef ENABLE_REFINE_RENEWAL	
	success_prob += CRefineManager::instance().Result(this);
#endif
#ifdef ENABLE_BATTLEPASS_SYSTEM
	if (GetLevel() - item->GetLevelLimit() <= BATTLEPASS_MIN_LEVEL_GAP)
		SetBattlePassProgress(BATTLEPASS_REFINE_ITEM);
#endif
	if (prob <= success_prob)
	{

		LPITEM pkNewItem = ITEM_MANAGER::instance().CreateItem(result_vnum, 1, 0, false);

		if (pkNewItem)
		{
	


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////



									{
										char buf[21];
										snprintf(buf, sizeof(buf), "%u", item2->GetID());
										LogManager::instance().ItemLog(this, item, "CHANGE_ATTRIBUTE", buf);
#ifdef ENABLE_BATTLEPASS_SYSTEM
										if (GetLevel() - item2->GetLevelLimit() <= BATTLEPASS_MIN_LEVEL_GAP)
											SetBattlePassProgress(BATTLEPASS_ENCHANT_ITEM);
#endif
									}



/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////



		if (bSuccess)
		{
			dwItemVnums.emplace_back(dwVnum);
			dwItemCounts.emplace_back(dwCount);
			item_gets.emplace_back(item_get);
			count++;
		}
		else
		{
			return false;
		}
	}
#ifdef ENABLE_BATTLEPASS_SYSTEM
	if (bSuccess)
		SetBattlePassProgress(BATTLEPASS_BOX_OPEN);
#endif
	return bSuccess;
}