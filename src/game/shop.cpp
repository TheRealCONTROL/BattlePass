
	if (iEmptyPos < 0)
	{
		{
			sys_log(1, "Shop::Buy : Inventory full : %s size %d", ch->GetName(), item->GetSize());
			M2_DESTROY_ITEM(item);
			return SHOP_SUBHEADER_GC_INVENTORY_FULL;
		}
	}

	ch->PointChange(POINT_GOLD, -dwPrice, false);
#ifdef ENABLE_BATTLEPASS_SYSTEM
	ch->SetBattlePassProgress(BATTLEPASS_BUY_ITEM, item->GetCount());
#endif
	{
		