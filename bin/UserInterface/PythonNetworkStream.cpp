

			Set(HEADER_GC_SPECIFIC_EFFECT,	CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCSpecificEffect), STATIC_SIZE_PACKET));
			Set(HEADER_GC_DRAGON_SOUL_REFINE,		CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCDragonSoulRefine), STATIC_SIZE_PACKET));
			
#ifdef ENABLE_BATTLEPASS_SYSTEM
			Set(HEADER_GC_BATTLEPASS_MISSION_DATA,			CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCBattlePassData), DYNAMIC_SIZE_PACKET));
			Set(HEADER_GC_BATTLEPASS_REWARD_DATA,			CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCBattlePassData), DYNAMIC_SIZE_PACKET));
#endif