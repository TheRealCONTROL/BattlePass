if app.ENABLE_BATTLEPASS_SYSTEM:
	import uibattlepassnew
	
	
	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		[...]
		[...]
		[...]
		if app.ENABLE_BATTLEPASS_SYSTEM:
			self.wndBattlePass = None
	
	
	
	def Close(self):
		[...]
		[...]
		[...]
		if app.ENABLE_BATTLEPASS_SYSTEM:
			if self.wndBattlePass:
				self.wndBattlePass.Hide()
				del self.wndBattlePass
	
	
	
	def __MakeWindows(self):
		[...]
		[...]
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		
		if app.ENABLE_BATTLEPASS_SYSTEM:
			self.wndBattlePass = uibattlepassnew.Window()