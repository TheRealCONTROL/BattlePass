
		// MiniMap Info
		bool RecvNPCList();
		bool RecvTargetCreatePacket();
		bool RecvTargetCreatePacketNew();
		bool RecvTargetUpdatePacket();
		bool RecvTargetDeletePacket();

#ifdef ENABLE_BATTLEPASS_SYSTEM
		bool RecvBattlePassMissionInfo();
		bool RecvBattlePassRewardInfo();
#endif