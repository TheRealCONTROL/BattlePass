


			case HEADER_GC_HANDSHAKE:
				RecvHandshakePacket();
				return;
				break;

			case HEADER_GC_HANDSHAKE_OK:
				RecvHandshakeOKPacket();
				return;
				break;

#ifdef ENABLE_BATTLEPASS_SYSTEM
			case HEADER_GC_BATTLEPASS_MISSION_DATA:
				ret = RecvBattlePassMissionInfo();
				break;
			
			case HEADER_GC_BATTLEPASS_REWARD_DATA:
				ret = RecvBattlePassRewardInfo();
				break;
#endif


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


#ifdef ENABLE_BATTLEPASS_SYSTEM
bool CPythonNetworkStream::RecvBattlePassMissionInfo()
{
	TPacketGCBattlePassData Packet;
	if (!Recv(sizeof(Packet), &Packet)) {
		TraceError("RecvBattlePassMissionInfo Error");
		return false;
	}
	
	int missionCount = (Packet.wSize - sizeof(Packet)) / sizeof(TPacketBattlePassMission);
	if (missionCount <= 0) {
		return true;
	}
	
	PyObject* pMissionsList = PyList_New(missionCount);
	uint8_t slot = 0;
	
	for (int iPacketSize = Packet.wSize - sizeof(Packet); iPacketSize > 0; iPacketSize -= sizeof(TPacketBattlePassMission)) 
	{
		TPacketBattlePassMission SMissionInfo;
		if (!Recv(sizeof(SMissionInfo), &SMissionInfo)) {
			TraceError("RecvBattlePassMissionInfo Mission Error");
			Py_DECREF(pMissionsList);
			return false;
		}
		
		PyObject* pMissionData = Py_BuildValue("(iiiiii)",
			slot,
			SMissionInfo.iType,
			SMissionInfo.iCount,
			SMissionInfo.iRemain,
			SMissionInfo.iExp,
			SMissionInfo.bDaily);
			
		PyList_SetItem(pMissionsList, slot, pMissionData);
		slot += 1;
	}
	
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetBattlePassMissions", 
						 Py_BuildValue("(O)", pMissionsList));
	Py_DECREF(pMissionsList);
	
	return true;
}

bool CPythonNetworkStream::RecvBattlePassRewardInfo()
{
	TPacketGCBattlePassData Packet;
	if (!Recv(sizeof(Packet), &Packet)) {
		TraceError("RecvBattlePassRewardInfo Error");
		return false;
	}
	
	int rewardCount = (Packet.wSize - sizeof(Packet)) / sizeof(TPacketBattlePassRewards);
	if (rewardCount <= 0) {
		return true;
	}
	
	PyObject* pRewardsList = PyList_New(rewardCount);
	int index = 0;
	
	for (int iPacketSize = Packet.wSize - sizeof(Packet); iPacketSize > 0; iPacketSize -= sizeof(TPacketBattlePassRewards)) {
		TPacketBattlePassRewards SRewardInfo;
		if (!Recv(sizeof(SRewardInfo), &SRewardInfo)) {
			TraceError("RecvBattlePassRewardInfo Reward Error");
			Py_DECREF(pRewardsList);
			return false;
		}
		
		PyObject* pRewardData = Py_BuildValue("(iiii)", 
			SRewardInfo.nVnum, 
			SRewardInfo.nCount, 
			SRewardInfo.pVnum, 
			SRewardInfo.pCount);
			
		PyList_SetItem(pRewardsList, index, pRewardData);
		index += 1;
	}
	
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetRewardItems", 
						 Py_BuildValue("(O)", pRewardsList));
	Py_DECREF(pRewardsList);
	
	return true;
}
#endif