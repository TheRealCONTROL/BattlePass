#ifdef ENABLE_BATTLEPASS_SYSTEM
ACMD(do_battlepass_primium);
ACMD(do_battlepass_levelup);
ACMD(do_battlepass_reward);
ACMD(do_battlepass_mission_reset);
ACMD(do_battlepass_reset);
ACMD(do_battlepass_mission_skip);
#endif

/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////

#ifdef ENABLE_BATTLEPASS_SYSTEM
	{ "battlepass_primium",		do_battlepass_primium,				0,			POS_DEAD,	GM_PLAYER },
	{ "battlepass_levelup",		do_battlepass_levelup,				0,			POS_DEAD,	GM_PLAYER },
	{ "battlepass_reward",		do_battlepass_reward,				0,			POS_DEAD,	GM_PLAYER },
	{ "battlepass_mission_reset",do_battlepass_mission_reset,		0,			POS_DEAD,	GM_PLAYER },
	{ "battlepass_reset",		do_battlepass_reset,				0,			POS_DEAD,	GM_IMPLEMENTOR },
	{ "battlepass_mission_skip",do_battlepass_mission_skip,			0,			POS_DEAD,	GM_IMPLEMENTOR },
#endif