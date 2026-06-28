

		LPITEM item = ch->AutoGiveItem(itemVnum, fractionCount, -1, false);
		if (item)
		{
#ifdef ENABLE_BATTLEPASS_SYSTEM
			ch->SetBattlePassProgress(BATTLEPASS_FISHING);
#endif
			ch->ChatPacket(CHAT_TYPE_INFO, "كان الصيد ناجحاً.");
		}
		
		
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
		
		
		
				if (item_vnum)
				{
					FishingSuccess(ch);

					TPacketGCFishing p;
					p.header = HEADER_GC_FISHING;
					p.subheader = FISHING_SUBHEADER_GC_FISH;
					p.info = item_vnum;
					ch->GetDesc()->Packet(&p, sizeof(TPacketGCFishing));

					LPITEM item = ch->AutoGiveItem(item_vnum, 1, -1, false);
					if (item)
					{
#ifdef ENABLE_BATTLEPASS_SYSTEM
						ch->SetBattlePassProgress(BATTLEPASS_FISHING);
#endif
						item->SetSocket(0,GetFishLength(info->fish_id));
						if (test_server)
						{
							ch->ChatPacket(CHAT_TYPE_INFO, "طول السمكة التي تم اصطيادها هذه المرة هو %.2fcm", item->GetSocket(0)/100.f);
						}
					}