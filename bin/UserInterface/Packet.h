

#ifdef ENABLE_BATTLEPASS_SYSTEM
	HEADER_GC_BATTLEPASS_MISSION_DATA			= 103,
	HEADER_GC_BATTLEPASS_REWARD_DATA			= 104,
#endif


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


#ifdef ENABLE_BATTLEPASS_SYSTEM
struct TPacketGCBattlePassData
{
	BYTE bHeader;
	WORD wSize;
};

struct TPacketBattlePassMission
{
	uint8_t		iType;
	int			iCount;
	int			iRemain;
	uint16_t	iExp;
	bool		bDaily;
};

struct TPacketBattlePassRewards
{
	uint32_t		nVnum;
	uint16_t	nCount;
	uint32_t		pVnum;
	uint16_t	pCount;
};
#endif