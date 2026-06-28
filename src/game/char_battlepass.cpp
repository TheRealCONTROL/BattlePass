// Credits                                                               //
//                                                                       //
//This system was developed by **CONTROL**.                              //
//                                                                       //
//**Discord:** `control69`                                               //
//                                                                       //
//For more free and premium Metin2 systems, tools, and resources, visit: //
//                                                                       //
//https://pay2win-store.vercel.app/                                      //
///////////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "constants.h"
#include "utils.h"
#include "config.h"
#include "char.h"
#include "item.h"
#include "item_manager.h"
#include "locale_service.h"
#include "questmanager.h"
#include "packet.h"
#include "desc_client.h"
#include "desc_manager.h"
#include "buffer_manager.h"
#include "char_battlepass.h"
#include <vector>
#include <algorithm>
#include <random>
#include <set>

#define SINGLE_REWARDS_TABLE TRUE
#define MULTI_MISSION_PROGRESS TRUE
constexpr int MAX_BATTLEPASS_LEVEL = 20;

#ifdef ENABLE_BATTLEPASS_SYSTEM

static std::mt19937& GetRNG()
{
	static std::mt19937 rng{std::random_device{}()};
	return rng;
}

void CHARACTER::CheckBattlePassTimers(bool isSend)
{
	const auto now = get_global_time();
	const auto dayTime = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_DAILY_TIME] - now;
	const auto weekTime = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_WEEKLY_TIME] - now;

	// Month Check
	const auto playerMonth = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MONTH];
	if (playerMonth != GetMonthIndex())
	{
		ResetPlayerMonth(isSend);
		
		if (dayTime <= 0)
			m_iBattlePassPlayerData[BATTLEPASS_PLAYER_DAILY_TIME] = GetTimeToNextDay() + now;
		
		if (weekTime <= 0)
			m_iBattlePassPlayerData[BATTLEPASS_PLAYER_WEEKLY_TIME] = GetTimeToNextWeek() + now;
	}
	else
	{
		if (dayTime <= 0) 
		{
			ResetMission(true, isSend);
			m_iBattlePassPlayerData[BATTLEPASS_PLAYER_DAILY_TIME] = GetTimeToNextDay() + now;
		}
		
		if (weekTime <= 0) 
		{
			ResetMission(false, isSend);
			m_iBattlePassPlayerData[BATTLEPASS_PLAYER_WEEKLY_TIME] = GetTimeToNextWeek() + now;
		}
	}
}

void CHARACTER::OnLoginBattlePass()
{
	CheckBattlePassTimers(false);
	SendBattlePassPlayerData();
	SendBattlePassRewards();
	SendBattlePassMissions(true);
	SendBattlePassMissions(false);
}

void CHARACTER::ResetPlayerMonth(bool isSend)
{	
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MONTH]          = GetMonthIndex();
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL]          = 0;
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_EXP]            = 0;
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_NORMAL_REWARD]  = 0;
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_PRIMIUM_REWARD] = 0;
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_IS_PRIMIUM]     = false;
	
	if (isSend)
	{
		SendBattlePassPlayerData();
		SendBattlePassRewards();
	}
	
	ResetMission(true, isSend);
	ResetMission(false, isSend);
}

void CHARACTER::ResetMission(bool isDaily, bool isSend)
{
	if (isDaily)
	{
		std::shuffle(dailyMissionsData.begin(), dailyMissionsData.end(), GetRNG());
		
		for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) 
		{
			const uint8_t randomized = number(0, 2);
			m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_TYPE]    = dailyMissionsData[i][0];
			m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_COUNT]   = 0;
			m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_REMINING] = dailyMissionsData[i][1 + randomized];
			m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_EXP]     = dailyExpTable[randomized];
		}
		
		ChatPacket(CHAT_TYPE_INFO, "[«·»« · »«”]  „  ÃœÌœ „Â«„ «·»« · »«” «·ÌÊ„Ì…");
	}
	else
	{
		std::shuffle(weeklyMissionsData.begin(), weeklyMissionsData.end(), GetRNG());
		
		for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) 
		{
			const uint8_t randomized = number(0, 2);
			m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_TYPE]    = weeklyMissionsData[i][0];
			m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_COUNT]   = 0;
			m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_REMINING] = weeklyMissionsData[i][1 + randomized];
			m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_EXP]     = weeklyExpTable[randomized];
		}
		
		ChatPacket(CHAT_TYPE_INFO, "[«·»« · »«”]  „  ÃœÌœ „Â«„ «·»« · »«” «·√”»Ê⁄Ì…");
	}
	
	if (isSend)
		SendBattlePassMissions(isDaily);
}

void CHARACTER::SendBattlePassPlayerData()
{
	const auto now = get_global_time();
	// ? Direct access
	ChatPacket(CHAT_TYPE_COMMAND, "battlepass_data %d %d %d %d %d %d %d %d %d",
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MONTH],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_EXP],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_NORMAL_REWARD],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_PRIMIUM_REWARD],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_IS_PRIMIUM],
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_DAILY_TIME] - now,
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_WEEKLY_TIME] - now,
	GetTimeToNextMonth()
	);
}

void CHARACTER::SendBattlePassRewards()
{
    if (!GetDesc())
        return;
    
    const uint8_t rewardsCount = BATTLEPASS_MAX_REWARDS;
    const size_t packetSize = sizeof(TPacketGCBattlePassData) + (sizeof(TPacketBattlePassRewards) * rewardsCount);
    
    TEMP_BUFFER buf(packetSize);
    
    TPacketGCBattlePassData packet;
    packet.bHeader = HEADER_GC_BATTLEPASS_REWARD_DATA;
    packet.wSize = static_cast<uint16_t>(packetSize);
    
    buf.write(&packet, sizeof(packet));
    
    // ? Direct access
    const uint8_t CurrentMonth = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MONTH];
    
    std::vector<TPacketBattlePassRewards> rewardVec;
    rewardVec.reserve(rewardsCount);
    
    for (int i = 0; i < rewardsCount; i++) {
        TPacketBattlePassRewards reward;
        if (SINGLE_REWARDS_TABLE)
        {
            reward.nVnum = NormalRewards[0][i][0];
            reward.nCount = NormalRewards[0][i][1];
            reward.pVnum = PrimiumRewards[0][i][0];
            reward.pCount = PrimiumRewards[0][i][1];
        }
        else
        {
            reward.nVnum = NormalRewards[CurrentMonth][i][0];
            reward.nCount = NormalRewards[CurrentMonth][i][1];
            reward.pVnum = PrimiumRewards[CurrentMonth][i][0];
            reward.pCount = PrimiumRewards[CurrentMonth][i][1];
        }
        
        rewardVec.push_back(reward);
    }
    
    if (!rewardVec.empty())
        buf.write(rewardVec.data(), sizeof(TPacketBattlePassRewards) * rewardVec.size());
    
    GetDesc()->Packet(buf.read_peek(), buf.size());
}

void CHARACTER::SendBattlePassMissions(bool isDaily)
{
    if (!GetDesc())
        return;
    
    const uint8_t missionCount = BATTLEPASS_MAX_MISSION_COUNT;
    const size_t packetSize = sizeof(TPacketGCBattlePassData) + (sizeof(TPacketBattlePassMission) * missionCount);
    
    TEMP_BUFFER buf(packetSize);
    
    TPacketGCBattlePassData packet;
    packet.bHeader = HEADER_GC_BATTLEPASS_MISSION_DATA;
    packet.wSize = static_cast<uint16_t>(packetSize);
    
    buf.write(&packet, sizeof(packet));
    
    auto& MissionList = isDaily ? m_iBattlePassDailyMissions : m_iBattlePassWeeklyMissions;
    
    std::vector<TPacketBattlePassMission> missionVec;
    missionVec.reserve(missionCount);
    
    for (int i = 0; i < missionCount; i++) 
    {
        TPacketBattlePassMission mission;
        mission.iType   = MissionList[i][BATTLEPASS_MISSION_TYPE];
        mission.iCount  = MissionList[i][BATTLEPASS_MISSION_COUNT];
        mission.iRemain = MissionList[i][BATTLEPASS_MISSION_REMINING];
        mission.iExp    = MissionList[i][BATTLEPASS_MISSION_EXP];
        mission.bDaily  = isDaily;
        
        missionVec.push_back(mission);
    }
    
    if (!missionVec.empty())
        buf.write(missionVec.data(), sizeof(TPacketBattlePassMission) * missionVec.size());
    
    GetDesc()->Packet(buf.read_peek(), buf.size());
}

void CHARACTER::SetBattlePassProgress(uint8_t iType, uint32_t iValue) 
{
	// ? Direct access
	if (m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL] >= MAX_BATTLEPASS_LEVEL)
		return;
	
	auto dailySocket = -1, weeklySocket = -1;

	for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) 
	{
		const auto count  = m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_COUNT];
		const auto remain = m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_REMINING];
		if (count != remain)
		{
			if (m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_TYPE] == iType)
				dailySocket = i;
			if (!MULTI_MISSION_PROGRESS)
				break;
		}
	}

	for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) 
	{
		const auto count  = m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_COUNT];
		const auto remain = m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_REMINING];
		if (count != remain)
		{
			if (m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_TYPE] == iType)
				weeklySocket = i;
			if (!MULTI_MISSION_PROGRESS)
				break;
		}
	}

	if (dailySocket == -1 && weeklySocket == -1)
		return;

	uint16_t iGivenExp = 0;

	if (dailySocket != -1) 
	{
		const uint32_t count  = m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_COUNT] + iValue;
		const uint32_t remain = m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_REMINING];
#if defined(ENABLE_NOTIFICATIONS_SYSTEM)
		if (m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_COUNT] < remain && count >= remain)
			SendNotification(MSG_ITEM_BATTLEPASS, m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_TYPE]);
#endif
		m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_COUNT] = static_cast<int>(std::min(count, remain));
		if (count >= remain)
			iGivenExp += m_iBattlePassDailyMissions[dailySocket][BATTLEPASS_MISSION_EXP];

		ChatPacket(CHAT_TYPE_COMMAND, "battlepass_daily_progress %d %d %d", dailySocket, std::min(count, remain), remain);

		uint8_t completedMission = 0;
		for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) {
			if (m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_COUNT] == m_iBattlePassDailyMissions[i][BATTLEPASS_MISSION_REMINING])
				completedMission++;
		}
		if (completedMission == BATTLEPASS_MAX_MISSION_COUNT)
			ResetMission(true, true);
	}

	if (weeklySocket != -1) 
	{
		const uint32_t count  = m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_COUNT] + iValue;
		const uint32_t remain = m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_REMINING];
#if defined(ENABLE_NOTIFICATIONS_SYSTEM)
		if (m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_COUNT] < remain && count >= remain)
			SendNotification(MSG_ITEM_BATTLEPASS, m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_TYPE]);
#endif
		m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_COUNT] = static_cast<int>(std::min(count, remain));
		if (count >= remain)
			iGivenExp += m_iBattlePassWeeklyMissions[weeklySocket][BATTLEPASS_MISSION_EXP];

		ChatPacket(CHAT_TYPE_COMMAND, "battlepass_weekly_progress %d %d %d", weeklySocket, std::min(count, remain), remain);

		uint8_t completedMission = 0;
		for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) {
			if (m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_COUNT] == m_iBattlePassWeeklyMissions[i][BATTLEPASS_MISSION_REMINING])
				completedMission++;
		}
		if (completedMission == BATTLEPASS_MAX_MISSION_COUNT)
			ResetMission(false, true);
	}

	SetBattlePassExp(iGivenExp);
}

void CHARACTER::SetBattlePassExp(uint16_t iExp)
{
	if (iExp <= 0)
		return;
	
	// ? Direct access
	auto& playerLevel = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL];
	if (playerLevel >= MAX_BATTLEPASS_LEVEL)
		return;
	
	auto& playerExp = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_EXP];
	const auto maxExp = BATTLEPASS_MAX_EXP;
	auto remainExp = playerExp + iExp;
	
	if (remainExp >= maxExp)
	{
		remainExp -= maxExp;
		playerLevel++;
	}
	
	playerExp = (playerLevel >= MAX_BATTLEPASS_LEVEL) ? 0 : remainExp;
	
	SendBattlePassPlayerData();
}

void CHARACTER::GetBattlePassReward(bool Primium)
{
	// ? Direct access
	const uint8_t playerLevel   = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL];
	const uint8_t CurrentMonth  = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_MONTH];

	if (Primium)
	{
		const bool    isPrimium  = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_IS_PRIMIUM];
		const uint8_t curRecived = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_PRIMIUM_REWARD];

		if (!isPrimium)
			return;

		for (int i = 1; i <= MAX_BATTLEPASS_LEVEL; i++) 
		{
			if (playerLevel < i)   break;
			if (curRecived >= i)   continue;

			const auto reward = SINGLE_REWARDS_TABLE ? PrimiumRewards[0][i - 1][0] : PrimiumRewards[CurrentMonth][i - 1][0];
			const auto count  = SINGLE_REWARDS_TABLE ? PrimiumRewards[0][i - 1][1] : PrimiumRewards[CurrentMonth][i - 1][1];

			if (AutoGiveItem(reward, count))
			{
				m_iBattlePassPlayerData[BATTLEPASS_PLAYER_PRIMIUM_REWARD] = i;
				SendBattlePassPlayerData();
			}
			break;
		}
	}
	else
	{
		const uint8_t curRecived = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_NORMAL_REWARD];

		for (int i = 1; i <= MAX_BATTLEPASS_LEVEL; i++) 
		{
			if (playerLevel < i)   break;
			if (curRecived >= i)   continue;

			const auto reward = SINGLE_REWARDS_TABLE ? NormalRewards[0][i - 1][0] : NormalRewards[CurrentMonth][i - 1][0];
			const auto count  = SINGLE_REWARDS_TABLE ? NormalRewards[0][i - 1][1] : NormalRewards[CurrentMonth][i - 1][1];

			if (AutoGiveItem(reward, count))
			{
				m_iBattlePassPlayerData[BATTLEPASS_PLAYER_NORMAL_REWARD] = i;
				SendBattlePassPlayerData();
			}
			break;
		}
	}
}

void CHARACTER::SetPrimiumUpgrade()
{
	// ? Direct access
	if (m_iBattlePassPlayerData[BATTLEPASS_PLAYER_IS_PRIMIUM]) { 
		ChatPacket(CHAT_TYPE_INFO, "·ﬁœ ﬁ„  » —ﬁÌ… «·»« · »«” «·Œ«’ »ﬂ ≈·Ï «·»—Ì„ÌÊ„ »«·›⁄·.");
		return;
	}
	
	if (CountSpecifyItem(39210) < 1) {
		ChatPacket(CHAT_TYPE_INFO, "·Ì” ·œÌﬂ «·»‰œ «·„ÿ·Ê» ·  „ﬂ‰ „‰ ›⁄· –·ﬂ.");
		return;
	}
	
	RemoveSpecifyItem(39210, 1);
	
	m_iBattlePassPlayerData[BATTLEPASS_PLAYER_IS_PRIMIUM] = true;
	SendBattlePassPlayerData();
}

void CHARACTER::SetBattlePassLevelUp()
{
	// ? Direct access
	auto& playerLevel = m_iBattlePassPlayerData[BATTLEPASS_PLAYER_LEVEL];
	if (playerLevel >= MAX_BATTLEPASS_LEVEL)
		return;
	
	if (CountSpecifyItem(39211) < 1) {
		ChatPacket(CHAT_TYPE_INFO, "·Ì” ·œÌﬂ «·»‰œ «·„ÿ·Ê» ·  „ﬂ‰ „‰ ›⁄· –·ﬂ.");
		return;
	}
	
	RemoveSpecifyItem(39211, 1);
	
	playerLevel++;
	if (playerLevel >= MAX_BATTLEPASS_LEVEL)
		m_iBattlePassPlayerData[BATTLEPASS_PLAYER_EXP] = 0;
	
	SendBattlePassPlayerData();
}

void CHARACTER::ResetBattlepassMission(uint8_t iSlot, bool isDaily)
{
	if (iSlot >= BATTLEPASS_MAX_MISSION_COUNT)
		return;

	if (CountSpecifyItem(39212) < 1) {
		ChatPacket(CHAT_TYPE_INFO, "·Ì” ·œÌﬂ «·»‰œ «·„ÿ·Ê» ·  „ﬂ‰ „‰ ›⁄· –·ﬂ.");
		return;
	}

	// ? Direct access
	auto& MissionList = isDaily ? m_iBattlePassDailyMissions : m_iBattlePassWeeklyMissions;
	auto& MissionsData = isDaily ? dailyMissionsData : weeklyMissionsData;
	auto& ExpTable     = isDaily ? dailyExpTable : weeklyExpTable;

	const uint32_t count  = MissionList[iSlot][BATTLEPASS_MISSION_COUNT];
	const uint32_t remain = MissionList[iSlot][BATTLEPASS_MISSION_REMINING];

	if (count == remain)
		return;

	RemoveSpecifyItem(39212, 1);

	std::vector<std::vector<int>> availableMissions = MissionsData;
	// ? Static RNG
	std::shuffle(availableMissions.begin(), availableMissions.end(), GetRNG());

	robin_hood::unordered_flat_set<int> existingMissionTypes;
	for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; ++i) {
		if (i != iSlot)
			existingMissionTypes.insert(MissionList[i][BATTLEPASS_MISSION_TYPE]);
	}

	const uint8_t randomized = number(0, 2);
	for (const auto& m : availableMissions) {
		if (existingMissionTypes.find(m[0]) == existingMissionTypes.end()) {
			MissionList[iSlot][BATTLEPASS_MISSION_TYPE]    = m[0];
			MissionList[iSlot][BATTLEPASS_MISSION_COUNT]   = 0;
			MissionList[iSlot][BATTLEPASS_MISSION_REMINING] = m[1 + randomized];
			MissionList[iSlot][BATTLEPASS_MISSION_EXP]     = ExpTable[randomized];
			break;
		}
	}

	SendBattlePassMissions(isDaily);
}

void CHARACTER::BattlepassMissionSkip(bool isDaily) 
{
	// ? Direct access
	auto& MissionList = isDaily ? m_iBattlePassDailyMissions : m_iBattlePassWeeklyMissions;

	for (int i = 0; i < BATTLEPASS_MAX_MISSION_COUNT; i++) {
		const auto iType  = MissionList[i][BATTLEPASS_MISSION_TYPE];
		const auto count  = MissionList[i][BATTLEPASS_MISSION_COUNT];
		const auto remain = MissionList[i][BATTLEPASS_MISSION_REMINING];
		if (count != remain) {
			SetBattlePassProgress(iType, remain - count);
			break;
		}
	}
}

int* CHARACTER::GetBattlePassDailyMissions()
{ 
	return &m_iBattlePassDailyMissions[0][0]; 
}

int* CHARACTER::GetBattlePassWeeklyMissions()
{ 
	return m_iBattlePassWeeklyMissions[0]; 
}

int* CHARACTER::GetBattlePassPlayerData()
{ 
	return m_iBattlePassPlayerData;
}
#endif