
		if app.ENABLE_BATTLEPASS_SYSTEM:
			onPressKeyDict[app.DIK_F5]		= ui.__safe_func__(self.interface.wndBattlePass.Open()) # or change it to whatever you want

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

		if app.ENABLE_BATTLEPASS_SYSTEM:
			serverCommandList["battlepass_data"] = self.SetBattlePassData
			serverCommandList["battlepass_daily_progress"] = self.SetBattlePassDailyProgress
			serverCommandList["battlepass_weekly_progress"] = self.SetBattlePassWeeklyProgress
			
		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	if app.ENABLE_BATTLEPASS_SYSTEM:
		def OpenBattlePassBoard(self):
			self.interface.ToggleBattlePassBoard()
		def SetRewardItems(self, rewards_list):
			self.interface.wndBattlePass.SetRewardItems(rewards_list)
		def SetBattlePassData(self, Month, Level, Exp, isNormalRecived, isPrimiumRecived, isPrimium, dailyTime, weeklyTime, monthTime):
			self.interface.wndBattlePass.SetBattlePassData(int(Month), int(Level), int(Exp), int(isNormalRecived), int(isPrimiumRecived), int(isPrimium), int(dailyTime), int(weeklyTime), int(monthTime))
		def SetBattlePassMissions(self, missions_list):
			self.interface.wndBattlePass.SetBattlePassMissions(missions_list)
		def SetBattlePassDailyProgress(self, socket, count, remain):
			self.interface.wndBattlePass.SetBattlePassDailyProgress(int(socket), int(count), int(remain))
		def SetBattlePassWeeklyProgress(self, socket, count, remain):
			self.interface.wndBattlePass.SetBattlePassWeeklyProgress(int(socket), int(count), int(remain))