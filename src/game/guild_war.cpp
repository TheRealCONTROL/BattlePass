
void CGuild::EndWar(DWORD dwOppGID)
{
	if (dwOppGID == GetID())
		return;

	auto it = m_EnemyGuild.find(dwOppGID);
	if (it != m_EnemyGuild.end())
	{
		CWarMap * pMap = CWarMapManager::instance().Find(it->second.map_index);

		if (pMap)
			pMap->SetEnded();

		GuildWarPacket(dwOppGID, it->second.type, GUILD_WAR_END);
		m_EnemyGuild.erase(it);

		if (!UnderAnyWar())
		{
			for (const auto &it : m_memberOnline)
			{
				LPCHARACTER ch = it;
				ch->RemoveAffect(GUILD_SKILL_BLOOD);
				ch->RemoveAffect(GUILD_SKILL_BLESS);
				ch->RemoveAffect(GUILD_SKILL_SEONGHWI);
				ch->RemoveAffect(GUILD_SKILL_ACCEL);
				ch->RemoveAffect(GUILD_SKILL_BUNNO);
				ch->RemoveAffect(GUILD_SKILL_JUMUN);

				ch->RemoveBadAffect();
#ifdef ENABLE_BATTLEPASS_SYSTEM
				ch->SetBattlePassProgress(BATTLEPASS_GUILD_WAR);
#endif
			}
		}
	}
}