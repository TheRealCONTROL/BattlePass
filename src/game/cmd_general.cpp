#ifdef ENABLE_BATTLEPASS_SYSTEM
ACMD(do_battlepass_primium)
{
	ch->SetPrimiumUpgrade();
}
ACMD(do_battlepass_levelup)
{
	ch->SetBattlePassLevelUp();
}
ACMD(do_battlepass_reward)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1 || !isnhdigit(*arg1))
		return;
	
	ch->GetBattlePassReward(atoi(arg1));
}
ACMD(do_battlepass_mission_reset)
{
	char	arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	if (!*arg1 || !*arg2 || !isnhdigit(*arg1) || !isnhdigit(*arg2))
		return;
	
	ch->ResetBattlepassMission(atoi(arg1), atoi(arg2));
}
ACMD(do_battlepass_reset)
{
	ch->ResetPlayerMonth(true);
}
ACMD(do_battlepass_mission_skip)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1 || !isnhdigit(*arg1))
		return;
	
	ch->BattlepassMissionSkip(atoi(arg1));
}
#endif