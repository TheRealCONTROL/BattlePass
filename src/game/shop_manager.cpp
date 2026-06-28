
	sys_log(0, "SHOP: SELL: %s item name: %s(x%d):%u price: %u", ch->GetName(), item->GetName(), bCount, item->GetID(), dwPrice);

	if (iVal > 0)
		ch->ChatPacket(CHAT_TYPE_INFO, "سيتم فرض %d %% من مبلغ المبيعات كضريبة.", iVal);

	DBManager::instance().SendMoneyLog(MONEY_LOG_SHOP, item->GetVnum(), dwPrice);
#ifdef ENABLE_BATTLEPASS_SYSTEM
	ch->SetBattlePassProgress(BATTLEPASS_SELL_ITEM, bCount);
#endif
	if (bCount == item->GetCount())
		ITEM_MANAGER::instance().RemoveItem(item, "SELL");
	else
		item->SetCount(item->GetCount() - bCount);

	ch->PointChange(POINT_GOLD, dwPrice, false);
	ch->SyncQuickslot(QUICKSLOT_TYPE_ITEM, bCell, 255);
}