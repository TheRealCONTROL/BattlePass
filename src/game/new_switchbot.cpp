// only if you have this system !

			if (itemVnumSelected == 71084)
			{
				LPITEM switchItem = pkOwner->GetItem(TItemPos(SWITCHBOT, enchantSlot));
				if (switchItem)
				{
					const WORD itemCount = switchItem->GetCount();
					if (itemCount <= SWITCHBOT_PRICE_AMOUNT)
						m_table.items[enchantSlot] = 0;
					switchItem->SetCount(itemCount - SWITCHBOT_PRICE_AMOUNT);
#ifdef ENABLE_BATTLEPASS_SYSTEM
					pkOwner->SetBattlePassProgress(BATTLEPASS_ENCHANT_ITEM);
#endif
				}
				else
				{
					return;
				}
			}