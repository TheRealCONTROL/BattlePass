
if (pinfo->type == CHAT_TYPE_SHOUT)
	{
		// const int SHOUT_LIMIT_LEVEL = 15;

		if (ch->GetLevel() < g_iShoutLimitLevel)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, "يجب أن تصل للمستوى %d لتتمكن من فعل ذلك.", g_iShoutLimitLevel);
			return (iExtraLen);
		}

		// if (thecore_heart->pulse - (int) ch->GetLastShoutPulse() < passes_per_sec * g_iShoutLimitTime)
		if (thecore_heart->pulse - (int) ch->GetLastShoutPulse() < passes_per_sec * 3)
			return (iExtraLen);

		ch->SetLastShoutPulse(thecore_heart->pulse);
#ifdef ENABLE_BATTLEPASS_SYSTEM
		ch->SetBattlePassProgress(BATTLEPASS_SHOUT);
#endif
		TPacketGGShout p;
		