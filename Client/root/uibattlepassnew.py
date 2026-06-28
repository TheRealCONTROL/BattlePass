## Credits                                                                  #
#                                                                           #
#  This system was developed by **CONTROL**.                                #
#                                                                           #
#  **Discord:** `control69`                                                 #
#                                                                           #
#  For more free and premium Metin2 systems, tools, and resources, visit:   #
#                                                                           #
#  https://pay2win-store.vercel.app/                                        #
#                                                                           #
#############################################################################


import app, player, net
import ui
import localeInfo
import uiScriptLocale
import constInfo
import uiToolTip
import item
import uiCommon
import constInfo


MAX_EXP = 1000
MAX_PAGES = 2 # 1. Missions / 2. Rewards

MAX_ITEMS_PER_PAGE = 10
MAX_MISSION = 10
MAX_EXP_PER_STAGE = 5
MAX_MISSION_TIP = [
	localeInfo.BATTLPASS_MISSION_TEXT_1,
	localeInfo.BATTLPASS_MISSION_TEXT_2,
	localeInfo.BATTLPASS_MISSION_TEXT_3,
	localeInfo.BATTLPASS_MISSION_TEXT_4,
	localeInfo.BATTLPASS_MISSION_TEXT_5,
	localeInfo.BATTLPASS_MISSION_TEXT_6,
	localeInfo.BATTLPASS_MISSION_TEXT_7,
	localeInfo.BATTLPASS_MISSION_TEXT_8,
	localeInfo.BATTLPASS_MISSION_TEXT_9,
	localeInfo.BATTLPASS_MISSION_TEXT_10,
	localeInfo.BATTLPASS_MISSION_TEXT_11,
	localeInfo.BATTLPASS_MISSION_TEXT_12,
	localeInfo.BATTLPASS_MISSION_TEXT_13,
	localeInfo.BATTLPASS_MISSION_TEXT_14,
	localeInfo.BATTLPASS_MISSION_TEXT_15,
]
MONTH_DICT = [
	localeInfo.BP_JANUARY,
	localeInfo.BP_FEBRUARY, localeInfo.BP_MARCH,
	localeInfo.BP_APRIL, localeInfo.BP_MAY,
	localeInfo.BP_JUNE, localeInfo.BP_JULY,
	localeInfo.BP_AUGUST, localeInfo.BP_SEPTEMBER,
	localeInfo.BP_OCTOBER, localeInfo.BP_NOVEMBER,
	localeInfo.BP_DECEMBER
]

PRIMIUM_ITEM = 39210
LEVELUP_ITEM = 39211
RESET_ITEM = 39212
REWARD_PAGE = 0
MISSION_PAGE = 1

ROOT_PATH = "d:/ymir work/ui/pattern/control_work/battlepass/ui/"
MISSION_IMAGE_PATH = "d:/ymir work/ui/pattern/control_work/battlepass/"
SHOP_NUMBER = 20 ## The Number Of Your Shop

BOARD_WIDTH = 500 + 27
BOARD_HEIGHT = 300 + 50


class Window(ui.Window):

	def __init__(self):
		ui.Window.__init__(self)
		self.__Initialize()
		self.__Load()

	def __Initialize(self):
		self.__children = {}

		self.toolTip = None
		self.tooltipItem = None

		self.rewardItemsNormal = []
		self.rewardItemsPrimium = []

		self.NormalRecived = 0
		self.PrimiumRecived = 0

		self.playerLevel = 0
		self.isPrimium = False

		self.clockLeftTime = 0
		self.missionClockLeftTime = []

		self.QuestPage = 0

		self.CanClickNormal = True
		self.CanClickPrimium = True
		self.ItemQuestionDlg = None

		self.max_page_buttons = 10
		self.total_count = 20
		self.board_count = min(self.max_page_buttons, self.total_count)
		self.scroll_animation = None
		self.target_pos = 0.0
		self.current_pos = 0.0
		self.animation_speed = 0.1
		self.scroll_speed = 2.0

	def Destroy(self):
		self.__Initialize()

	def __Load(self):
		try:
			self.AddFlag("movable")
			self.AddFlag("float")
			#self.AddFlag("animate") # only uncomment if you have those systems
			#self.AddFlag("alpha_sensitive") # only uncomment if you have those systems
			self.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 10 + 18)

			mainBoard = ui.BoardWithTitleBar()
			mainBoard.SetParent(self)
			mainBoard.SetPosition(0, 0)
			mainBoard.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 15)
			mainBoard.SetCloseEvent(ui.__mem_func__(self.Close))
			mainBoard.SetTitleName("BattlePass")
			mainBoard.Show()
			self.__children["mainBoard"] = mainBoard

			## ----- pageBoards_1 (Rewards Page) -----
			pageBoard = ui.ImageBox()
			pageBoard.SetParent(self.__children["mainBoard"])
			pageBoard.LoadImage(ROOT_PATH + "slice/bg.png")
			pageBoard.SetPosition(0, 30)
			pageBoard.SetWindowHorizontalAlignCenter()
			self.__children["pageBoard_{}".format(0)] = pageBoard

			leftBanner = ui.ImageBox()
			leftBanner.SetParent(self.__children["pageBoard_0"])
			leftBanner.LoadImage(ROOT_PATH + "slice/items/left_board.png")
			leftBanner.SetPosition(0, 68)
			leftBanner.SetWindowHorizontalAlignLeft()
			leftBanner.Show()
			self.__children["leftBanner"] = leftBanner

			rewardWindow = ui.Window()
			rewardWindow.SetParent(self.__children["pageBoard_0"])
			rewardWindow.SetSize(412, 212)
			rewardWindow.SetPosition(72, 67)
			rewardWindow.SetWindowHorizontalAlignLeft()
			rewardWindow.Show()
			self.__children["rewardWindow"] = rewardWindow

			rewardBoard = ui.ExpandedImageBox()
			rewardBoard.SetParent(self.__children["rewardWindow"])
			rewardBoard.LoadImage(ROOT_PATH + "slice/items/full_board.png")
			rewardBoard.SetPosition(0, 0)
			rewardBoard.SetWindowHorizontalAlignCenter()
			rewardBoard.SetWindowVerticalAlignCenter()
			rewardBoard.Show()
			self.__children["rewardBoard"] = rewardBoard

			bigLock = ui.ExpandedImageBox()
			bigLock.SetParent(self.__children["pageBoard_0"])
			bigLock.LoadImage(ROOT_PATH + "slice/items/big_lock.png")
			bigLock.SetPosition(33, 180)
			bigLock.SetWindowHorizontalAlignCenter()
			bigLock.Show()
			bigLock.OnMouseLeftButtonDown = ui.__mem_func__(self.__OnClickPrimium)
			self.__children["bigLock"] = bigLock

			## ----- pageBoards_2 (Mission Page) -----
			pageBoard = ui.ImageBox()
			pageBoard.SetParent(self.__children["mainBoard"])
			pageBoard.LoadImage(ROOT_PATH + "slice/bg.png")
			pageBoard.SetPosition(0, 30)
			pageBoard.SetWindowHorizontalAlignCenter()
			self.__children["pageBoard_{}".format(1)] = pageBoard

			for i in xrange(2):
				baseFrame = ui.ImageBox()
				baseFrame.SetParent(self.__children["pageBoard_1"])
				baseFrame.LoadImage(ROOT_PATH + "slice/base_frame.png")
				baseFrame.SetPosition(0, 90)
				baseFrame.SetWindowHorizontalAlignCenter()
				self.__children["baseFrame_{}".format(i)] = baseFrame

			questButtonData = (
				(localeInfo.MISSION_DAILY_TITLE, "btn_m_1.png", 4),
				(localeInfo.MISSION_WEEKLY_TITLE, "btn_m_2.png", 93),
			)

			for i in xrange(2):
				pageQuestButton = ui.RadioButton()
				pageQuestButton.SetParent(self.__children["pageBoard_1"])
				pageQuestButton.SetUpVisual(ROOT_PATH + "slice/quest/btn_m_0.png")
				pageQuestButton.SetOverVisual(ROOT_PATH + "slice/quest/btn_m_0.png")
				pageQuestButton.SetDownVisual(ROOT_PATH + "slice/quest/" + questButtonData[i][1])
				pageQuestButton.SetText(questButtonData[i][0], 12)
				pageQuestButton.SetPosition(questButtonData[i][2], 65)
				pageQuestButton.SetEvent(ui.__mem_func__(self.__OnClickQuestPageButton), i)
				pageQuestButton.Show()

				self.__children["pageQuestButton_{}".format(i)] = pageQuestButton

			## ----- pageButtonsImages / pageButtons (outside board) -----
			imageFiles = (
				"btns_items.dds",
				"btns_quests.dds",
			)

			for i in xrange(2):
				pageButtonsImages = ui.ImageBox()
				pageButtonsImages.SetParent(self)
				pageButtonsImages.LoadImage(ROOT_PATH + "slice/" + imageFiles[i])
				pageButtonsImages.SetPosition(2, 325)

				self.__children["pageButtonsImage_{}".format(i)] = pageButtonsImages


			buttonPositions = (10, 68)

			for i in xrange(MAX_PAGES):
				pageButtons = ui.RadioButton()
				pageButtons.SetParent(self)
				pageButtons.SetPosition(buttonPositions[i], 328)
				pageButtons.SetSize(48, 26)
				pageButtons.SetEvent(ui.__mem_func__(self.__OnClickPageButton), i)
				pageButtons.Show()

				self.__children["pageButton_{}".format(i)] = pageButtons
				self.__children["pageBoard_{}".format(i)].Hide()

			rewardsScrollBar = ui.ScrollBarHorizontal()
			rewardsScrollBar.SetParent(self)
			rewardsScrollBar.SetScrollBarSize(483)
			rewardsScrollBar.SetPosition(12, 320 - 7)
			rewardsScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			rewardsScrollBar.SetMiddleBarSize(float(self.max_page_buttons) / float(self.total_count))
			rewardsScrollBar.Show()
			self.__children["rewardsScrollBar"] = rewardsScrollBar

			self.OnScroll()

			for i in xrange(4):
				## Daily Missions
				dailyMissionBg = ui.MakeExpandedImageBox(self.__children["baseFrame_{}".format(0)], MISSION_IMAGE_PATH + "ui/slice/banner_daily.png", 0, 3 + (i*50))
				dailyMissionBg.SetWindowHorizontalAlignCenter()
				dailyMissionBg.Show()
				self.__children["dailyMissionBg_{}".format(i)] = dailyMissionBg

				dailyMissionLock = ui.MakeExpandedImageBox(self.__children["baseFrame_{}".format(0)], MISSION_IMAGE_PATH + "ui/slice/quest_done.png", 0, 3 + (i*50))
				dailyMissionLock.SetWindowHorizontalAlignCenter()
				dailyMissionLock.Hide()
				self.__children["dailyMissionLock_{}".format(i)] = dailyMissionLock

				dailyMissionTypeIcon = ui.MakeExpandedImageBox(dailyMissionBg, MISSION_IMAGE_PATH + "ui/slice/daily_icons/battlepass_mission_0.png", 60, 0)
				dailyMissionTypeIcon.SetWindowHorizontalAlignRight()
				dailyMissionTypeIcon.Show()
				self.__children["dailyMissionTypeIcon_{}".format(i)] = dailyMissionTypeIcon

				dailyMissionGauge = ui.MakeGauge(dailyMissionBg, 70 + 150, 30, 190)
				self.__children["dailyMissionGauge_{}".format(i)] = dailyMissionGauge

				dailyMissionGaugeTxt = ui.MakeTextLineNew(dailyMissionBg, 70 + 150, 25, "0/0")
				self.__children["dailyMissionGaugeTxt_{}".format(i)] = dailyMissionGaugeTxt

				dailyMissionTxt = ui.MakeTextLineNew(dailyMissionBg, 70, 8, "MissionKill % Of Whatever")
				dailyMissionTxt.SetWindowHorizontalAlignRight()
				self.__children["dailyMissionTxt_{}".format(i)] = dailyMissionTxt

				dailyMissionExp = ui.MakeTextLineNew(dailyMissionBg, 49, 26, str(MAX_EXP))
				dailyMissionExp.SetHorizontalAlignCenter()
				self.__children["dailyMissionExp_{}".format(i)] = dailyMissionExp

				refreshDailyButton = ui.Button()
				refreshDailyButton.SetParent(dailyMissionBg)
				btn_file = MISSION_IMAGE_PATH + "ui/slice/quest/"
				refreshDailyButton.SetUpVisual(btn_file + "btn_refresh_0.png")
				refreshDailyButton.SetOverVisual(btn_file + "btn_refresh_1.png")
				refreshDailyButton.SetDownVisual(btn_file + "btn_refresh_2.png")
				refreshDailyButton.SetEvent(ui.__mem_func__(self.__OnClickRefreshMission), i, True)
				refreshDailyButton.SetWindowHorizontalAlignRight()
				refreshDailyButton.SetPosition(23, 2)
				refreshDailyButton.Show()
				self.__children["refreshDailyButton_{}".format(i)] = refreshDailyButton

				## Weekly Missions
				weeklyMissionBg = ui.MakeExpandedImageBox(self.__children["baseFrame_{}".format(1)], MISSION_IMAGE_PATH + "ui/slice/banner_weakly.png", 0, 3 + (i*50))
				weeklyMissionBg.SetWindowHorizontalAlignCenter()
				weeklyMissionBg.Show()
				self.__children["weeklyMissionBg_{}".format(i)] = weeklyMissionBg

				weeklyMissionLock = ui.MakeExpandedImageBox(self.__children["baseFrame_{}".format(1)], MISSION_IMAGE_PATH + "ui/slice/quest_done.png", 0, 3 + (i*50))
				weeklyMissionLock.SetWindowHorizontalAlignCenter()
				weeklyMissionLock.Hide()
				self.__children["weeklyMissionLock_{}".format(i)] = weeklyMissionLock

				weeklyMissionTypeIcon = ui.MakeExpandedImageBox(weeklyMissionBg, MISSION_IMAGE_PATH + "ui/slice/weekly_icons/battlepass_mission_0.png", 60, 0)
				weeklyMissionTypeIcon.SetWindowHorizontalAlignRight()
				weeklyMissionTypeIcon.Show()
				self.__children["weeklyMissionTypeIcon_{}".format(i)] = weeklyMissionTypeIcon

				weeklyMissionGauge = ui.MakeGauge(weeklyMissionBg, 70 + 150, 30, 190)
				self.__children["weeklyMissionGauge_{}".format(i)] = weeklyMissionGauge

				weeklyMissionGaugeTxt = ui.MakeTextLineNew(weeklyMissionBg, 70 + 150, 25, "0/0")
				self.__children["weeklyMissionGaugeTxt_{}".format(i)] = weeklyMissionGaugeTxt

				weeklyMissionTxt = ui.MakeTextLineNew(weeklyMissionBg, 70, 8, "MissionKill % Of Whatever")
				weeklyMissionTxt.SetWindowHorizontalAlignRight()
				self.__children["weeklyMissionTxt_{}".format(i)] = weeklyMissionTxt

				weeklyMissionExp = ui.MakeTextLineNew(weeklyMissionBg, 49, 26, "1000")
				weeklyMissionExp.SetHorizontalAlignCenter()
				self.__children["weeklyMissionExp_{}".format(i)] = weeklyMissionExp

				refreshWeeklyButton = ui.Button()
				refreshWeeklyButton.SetParent(weeklyMissionBg)
				btn_file = MISSION_IMAGE_PATH + "ui/slice/quest/"
				refreshWeeklyButton.SetUpVisual(btn_file + "btn_refresh_0.png")
				refreshWeeklyButton.SetOverVisual(btn_file + "btn_refresh_1.png")
				refreshWeeklyButton.SetDownVisual(btn_file + "btn_refresh_2.png")
				refreshWeeklyButton.SetEvent(ui.__mem_func__(self.__OnClickRefreshMission), i, False)
				refreshWeeklyButton.SetWindowHorizontalAlignRight()
				refreshWeeklyButton.SetPosition(23, 2)
				refreshWeeklyButton.Show()
				self.__children["refreshWeeklyButton_{}".format(i)] = refreshWeeklyButton

			topBg = ui.MakeImageBox(self, MISSION_IMAGE_PATH + "ui/slice/top_bg.png", 12, 32)
			topBg.Show()
			self.__children["topBg"] = topBg

			gaugeBg = ui.MakeImageBox(self.__children["topBg"], MISSION_IMAGE_PATH + "ui/slice/gauge.png", 305, 27 + 4)
			gaugeBg.Show()
			self.__children["gaugeBg"] = gaugeBg

			LevelUpButton = ui.Button()
			LevelUpButton.SetParent(self.__children["topBg"])
			btn_file = MISSION_IMAGE_PATH + "ui/slice/"
			LevelUpButton.SetUpVisual(btn_file + "btn_level_up_0.png")
			LevelUpButton.SetOverVisual(btn_file + "btn_level_up_1.png")
			LevelUpButton.SetDownVisual(btn_file + "btn_level_up_2.png")
			LevelUpButton.SetEvent(ui.__mem_func__(self.__OnClickLevelUp))
			LevelUpButton.SetPosition(265, 29 + 4)
			LevelUpButton.Show()
			self.__children["LevelUpButton"] = LevelUpButton

			playerLevelTxt = ui.MakeTextLineNew(self.__children["topBg"], 266, 8, "Lv.0")
			playerLevelTxt.SetOutline()
			playerLevelTxt.SetHorizontalAlignRight()
			self.__children["playerLevelTxt"] = playerLevelTxt

			playeExpTxt = ui.MakeTextLineNew(self.__children["topBg"], 390, 28 + 6, "0/0")
			playeExpTxt.SetOutline()
			playeExpTxt.SetHorizontalAlignCenter()
			self.__children["playeExpTxt"] = playeExpTxt

			clockImage = ui.MakeImageBox(self.__children["topBg"], "d:/ymir work/ui/pattern/control_work/calendar.png", 425 + 20, 6 - 4)
			clockImage.OnMouseOverIn = ui.__safe_func__(self.OnMouseOverInText, localeInfo.TOOLTIP_BATTLEPASS_CALENDAR)
			clockImage.OnMouseOverOut = ui.__safe_func__(self.OnMouseOverOutText)
			clockImage.Show()
			self.__children["clockImage"] = clockImage

			clockTxt = ui.MakeTextLineNew(self.__children["clockImage"], -3, 2 + 6, "00:00:00")
			clockTxt.SetOutline()
			clockTxt.SetHorizontalAlignLeft()
			self.__children["clockTxt"] = clockTxt

			expGauge = ui.MakeExpandedImageBox(self.__children["gaugeBg"], MISSION_IMAGE_PATH + "ui/slice/gauge_inner.png", 3, 3)
			expGauge.Show()
			self.__children["expGauge"] = expGauge

			for i in xrange(4):
				expGaugeSplits = ui.MakeImageBox(self.__children["gaugeBg"], MISSION_IMAGE_PATH + "ui/slice/gauge_line.png", 33 + (i*32), 3)
				expGaugeSplits.Show()
				self.__children["expGaugeSplits_{}".format(i)] = expGaugeSplits

			sGaugeAnimation = ui.AniImageBox()
			sGaugeAnimation.SetParent(self.__children["gaugeBg"])
			sGaugeAnimation.ResetFrame()
			sGaugeAnimation.Show()
			sGaugeAnimation.SetDelay(3)
			for j in range(52):
				image_file = MISSION_IMAGE_PATH + "ui/gauge/gauge_effect_%02d.dds" % j
				sGaugeAnimation.AppendImage(image_file)
			sGaugeAnimation.SetPosition(0, 1)
			sGaugeAnimation.SetSize(0, 0)
			self.__children["sGaugeAnimation"] = sGaugeAnimation

			PrimiumButton = ui.Button()
			PrimiumButton.SetParent(self.__children["topBg"])
			btn_file = MISSION_IMAGE_PATH + "ui/slice/banners/banner_02.png"
			PrimiumButton.SetUpVisual(btn_file)
			PrimiumButton.SetOverVisual(btn_file)
			PrimiumButton.SetDownVisual(btn_file)
			PrimiumButton.SetEvent(ui.__mem_func__(self.__OnClickShop))
			PrimiumButton.SetPosition(3, 3)
			PrimiumButton.Show()
			self.__children["PrimiumButton"] = PrimiumButton

			sBannerAnimation = ui.AniImageBox()
			sBannerAnimation.SetParent(self.__children["PrimiumButton"])
			sBannerAnimation.ResetFrame()
			sBannerAnimation.Show()
			sBannerAnimation.SetDelay(3)
			for j in range(60):
				image_file = MISSION_IMAGE_PATH + "ui/effect/effect_%02d.dds" % j
				sBannerAnimation.AppendImage(image_file)
			sBannerAnimation.SetPosition(0, 0)
			sBannerAnimation.SetSize(0, 0)
			self.__children["sBannerAnimation"] = sBannerAnimation

			for i in xrange(2):
				imgPath = "d:/ymir work/ui/pattern/control_work/clock_bar_%d.png" % i
				missionClockImage = ui.MakeExpandedImageBox(self, imgPath, 309, 90)
				missionClockImage.Show()
				missionClockImage.OnMouseOverIn = ui.__safe_func__(self.OnMouseOverInText, localeInfo.TOOLTIP_BATTLEPASS_MISSION)
				missionClockImage.OnMouseOverOut = ui.__safe_func__(self.OnMouseOverOutText)
				self.__children["missionClockImage_{}".format(i)] = missionClockImage

				missionClockText = ui.MakeTextLineNew(self.__children["missionClockImage_{}".format(i)], 145, 6, "00:00:00")
				missionClockText.SetOutline()
				missionClockText.SetHorizontalAlignLeft()
				self.__children["missionClockText_{}".format(i)] = missionClockText

		except:
			import exception
			exception.Abort("BattlePass.__Load")

		self.toolTip = uiToolTip.ToolTip()
		self.tooltipItem = uiToolTip.ItemToolTip()

		self.SetCenterPosition()
		self.__OnClickQuestPageButton(0)
		self.__OnClickPageButton(0)

		self.SetRewards()
		if app.ENABLE_CLIP_MASK:
			self.__children["rewardBoard"].SetClippingMaskWindow(self.__children["rewardWindow"])

	def OnMouseOverInText(self, text):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(text)
		self.toolTip.AlignHorizonalCenter()
		self.toolTip.Show()

	def OnMouseOverOutText(self):
		self.toolTip.Hide()

	def __OnClickShop(self):
		net.SendRemoteShopPacket(SHOP_NUMBER) # MAKE SURE YOU HAVE THIS SYSTEM !

	def __OnClickQuestPageButton(self, arg):
		for page in xrange(2):
			self.__children["baseFrame_{}".format(page)].Hide()
		self.__children["baseFrame_{}".format(arg)].Show()

		for btn in xrange(2):
			self.__children["pageQuestButton_{}".format(btn)].SetUp()
		self.__children["pageQuestButton_{}".format(arg)].Down()

		for img in xrange(2):
			self.__children["missionClockImage_{}".format(img)].Hide()
		self.__children["missionClockImage_{}".format(arg)].Show()

		self.QuestPage = arg

	def __OnClickLevelUp(self):
		if self.ItemQuestionDlg == None:
			self.ItemQuestionDlg = ItemQuestionDlg()
		if self.ItemQuestionDlg.IsShow():
			return
		self.ItemQuestionDlg.SetText(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_1)
		self.ItemQuestionDlg.SetText2(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_NEED % (1))
		self.ItemQuestionDlg.SetAcceptEvent(ui.__safe_func__(self.OnCloseQuestionDialog, LEVELUP_ITEM))
		self.ItemQuestionDlg.SetCancelEvent(ui.__safe_func__(self.OnCloseQuestionDialog, False))
		self.ItemQuestionDlg.Open(LEVELUP_ITEM)

	def __OnClickPrimium(self):
		if self.ItemQuestionDlg == None:
			self.ItemQuestionDlg = ItemQuestionDlg()
		if self.ItemQuestionDlg.IsShow():
			return
		self.ItemQuestionDlg.SetText(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_2)
		self.ItemQuestionDlg.SetText2(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_NEED % (1))
		self.ItemQuestionDlg.SetAcceptEvent(ui.__safe_func__(self.OnCloseQuestionDialog, PRIMIUM_ITEM))
		self.ItemQuestionDlg.SetCancelEvent(ui.__safe_func__(self.OnCloseQuestionDialog, False))
		self.ItemQuestionDlg.Open(PRIMIUM_ITEM)

	def OnCloseQuestionDialog(self, item):
		if not self.ItemQuestionDlg:
			return

		self.ItemQuestionDlg.Close()
		self.ItemQuestionDlg = None

		if item == False:
			return

		if player.GetItemCountByVnum(item) < 1:
			self.popupDlg = uiCommon.PopupDialog()
			self.popupDlg.SetText(localeInfo.BATTLEPASS_NOT_ENOUGH_ITEM)
			self.popupDlg.Open()
			return

		if item == PRIMIUM_ITEM:
			net.SendChatPacket("/battlepass_primium")
		else:
			net.SendChatPacket("/battlepass_levelup")

	def __OnClickRefreshMission(self, iSlot, isDaily):
		if self.ItemQuestionDlg == None:
			self.ItemQuestionDlg = ItemQuestionDlg()
		if self.ItemQuestionDlg.IsShow():
			return
		self.ItemQuestionDlg.SetText(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_2)
		self.ItemQuestionDlg.SetText2(localeInfo.BATTLEPASS_ITEM_DIALOG_QUISTION_NEED % (1))
		self.ItemQuestionDlg.SetAcceptEvent(ui.__safe_func__(self.OnCloseResetQuestionDialog, RESET_ITEM, iSlot, isDaily))
		self.ItemQuestionDlg.SetCancelEvent(ui.__safe_func__(self.OnCloseResetQuestionDialog, False, iSlot, isDaily))
		self.ItemQuestionDlg.Open(RESET_ITEM)

	def OnCloseResetQuestionDialog(self, item, iSlot, isDaily):
		if not self.ItemQuestionDlg:
			return

		self.ItemQuestionDlg.Close()
		self.ItemQuestionDlg = None

		if item == False:
			return

		if player.GetItemCountByVnum(item) < 1:
			self.popupDlg = uiCommon.PopupDialog()
			self.popupDlg.SetText(localeInfo.BATTLEPASS_NOT_ENOUGH_ITEM)
			self.popupDlg.Open()
			return

		net.SendChatPacket("/battlepass_mission_reset {} {}".format(int(iSlot), int(isDaily)))

	def OnRender(self):
		if self.scroll_animation:
			self.current_pos += (self.target_pos - self.current_pos) * self.animation_speed
			if abs(self.target_pos - self.current_pos) < 0.001:
				self.current_pos = self.target_pos
				self.scroll_animation = None

			self.__children["rewardsScrollBar"].SetPos(self.current_pos)
			self.UpdatePosition()

	def OnScroll(self):
		self.UpdatePosition()

	def UpdatePosition(self):
		pos = self.__children["rewardsScrollBar"].GetPos() * (self.total_count - self.board_count)
		x_position = 205 - pos * 41
		self.__children["rewardBoard"].SetPosition(int(x_position), 0)

	def OnMouseWheel(self, length):
		def WHEEL_TO_SCROLL(length):
			if length > 0:
				return -1
			elif length < 0:
				return 1
			else:
				return 0

		if self.IsInPosition() and self.__children["rewardsScrollBar"].IsShow() and self.total_count > 0:
			dir = WHEEL_TO_SCROLL(length)
			self.target_pos = self.__children["rewardsScrollBar"].GetPos() + ((self.scroll_speed / self.total_count) * dir)
			self.target_pos = max(0.0, min(1.0, self.target_pos))

			if not self.scroll_animation:
				self.scroll_animation = True
				self.current_pos = self.__children["rewardsScrollBar"].GetPos()

			return True
		return False

	def __OnClickPageButton(self, arg):
		for page in xrange(2):
			self.__children["pageBoard_{}".format(page)].Hide()
		self.__children["pageBoard_{}".format(arg)].Show()

		for btn in xrange(2):
			self.__children["pageButton_{}".format(btn)].SetUp()
		self.__children["pageButton_{}".format(arg)].Down()

		for image in xrange(2):
			self.__children["pageButtonsImage_{}".format(image)].Hide()
		self.__children["pageButtonsImage_{}".format(arg)].Show()

		if arg == REWARD_PAGE:
			self.__children["rewardsScrollBar"].Show()
			for img in xrange(2):
				self.__children["missionClockImage_{}".format(img)].Hide()

		if arg == MISSION_PAGE:
			self.__children["rewardsScrollBar"].Hide()
			for img in xrange(2):
				self.__children["missionClockImage_{}".format(img)].Hide()
			self.__children["missionClockImage_{}".format(self.QuestPage)].Show()

	def SetRewards(self):
		for i in xrange(len(self.rewardItemsNormal)):
			itemList1 = self.rewardItemsNormal[i]
			normalItemsSlot = ui.ExpandedImageBox()
			normalItemsSlot.SetParent(self.__children["rewardBoard"])
			item.SelectItem(itemList1[0])
			normalItemsSlot.LoadImage(item.GetIconImageFileName())
			normalItemsSlot.OnMouseOverIn = ui.__safe_func__(self.OnMouseOverInNormalItem, i)
			normalItemsSlot.OnMouseOverOut = ui.__safe_func__(self.OnMouseOverOutItem)
			normalItemsSlot.OnMouseLeftButtonDown = ui.__mem_func__(self.SetNormalRewardAnimate)
			_, itemSize = item.GetItemSize()
			SizeList = [0, 32, 16, 0]
			normalItemsSlot.SetPosition(5 + (i * 41), SizeList[itemSize] + 15)
			normalItemsSlot.Show()
			self.__children["normalItemsSlot_{}".format(i)] = normalItemsSlot

			if int(itemList1[1]) > 1:
				number_str = str(itemList1[1])
				digits = len(number_str)
				x_offset = (digits - 1) * 5

				normalItemsCount = ui.NumberLine()
				normalItemsCount.SetParent(self.__children["normalItemsSlot_{}".format(i)])
				normalItemsCount.SetNumber(number_str)
				normalItemsCount.SetPosition(25 - x_offset, 25)

				normalItemsCount.Show()
				self.__children["normalItemsCount_{}".format(i)] = normalItemsCount

			itemList2 = self.rewardItemsPrimium[i]
			primiumItemsSlot = ui.ExpandedImageBox()
			primiumItemsSlot.SetParent(self.__children["rewardBoard"])
			item.SelectItem(itemList2[0])
			primiumItemsSlot.LoadImage(item.GetIconImageFileName())
			primiumItemsSlot.OnMouseOverIn = ui.__safe_func__(self.OnMouseOverInPrimiumItem, i)
			primiumItemsSlot.OnMouseOverOut = ui.__safe_func__(self.OnMouseOverOutItem)
			primiumItemsSlot.OnMouseLeftButtonDown = ui.__mem_func__(self.SetPrimiumRewardAnimate)
			_, itemSize = item.GetItemSize()
			SizeList = [0, 32, 16, 0]
			primiumItemsSlot.SetPosition(5 + (i * 41), SizeList[itemSize] + 110)
			primiumItemsSlot.Show()
			self.__children["primiumItemsSlot_{}".format(i)] = primiumItemsSlot

			if int(itemList2[1]) > 1:
				number_str = str(itemList2[1])
				digits = len(number_str)
				x_offset = (digits - 1) * 5

				primiumItemsCount = ui.NumberLine()
				primiumItemsCount.SetParent(self.__children["primiumItemsSlot_{}".format(i)])
				primiumItemsCount.SetNumber(number_str)
				primiumItemsCount.SetPosition(25 - x_offset, 25)

				primiumItemsCount.Show()
				self.__children["primiumItemsCount_{}".format(i)] = primiumItemsCount

			normalSlotLock = ui.MakeExpandedImageBox(self.__children["rewardBoard"], MISSION_IMAGE_PATH + "ui/slice/items/item_lock.png", 1 + (i * 41), 15)
			normalSlotLock.AddFlag("not_pick")
			if self.playerLevel > i:
				if self.NormalRecived > i:
					normalSlotLock.LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_done.png")
				else:
					normalSlotLock.Hide()
			else:
				normalSlotLock.Show()
			self.__children["normalSlotLock_{}".format(i)] = normalSlotLock

			primiumSlotLock = ui.MakeExpandedImageBox(self.__children["rewardBoard"], MISSION_IMAGE_PATH + "ui/slice/items/item_lock.png", 1 + (i * 41), 111)
			primiumSlotLock.AddFlag("not_pick")
			if self.playerLevel > i and self.isPrimium:
				if self.PrimiumRecived > i:
					primiumSlotLock.LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_done.png")
				else:
					primiumSlotLock.Hide()
			else:
				primiumSlotLock.Show()
			self.__children["primiumSlotLock_{}".format(i)] = primiumSlotLock

		for i in xrange(19):
			imgPath = MISSION_IMAGE_PATH + "ui/slice/items/level_bar/bg_level_{}.dds".format(0 if i < 10 else 1)
			levelBg = ui.MakeExpandedImageBox(self.__children["rewardBoard"], imgPath, 29 + (i * 41), 3)
			levelBg.Show()
			self.__children["levelBg_{}".format(i)] = levelBg

			levelPath = MISSION_IMAGE_PATH + "ui/slice/items/level_bar/{}.dds".format(i + 1)
			levelImg = ui.MakeExpandedImageBox(self.__children["rewardBoard"], levelPath, 29 + (i * 41), 3)
			levelImg.Show()
			self.__children["levelImg_{}".format(i)] = levelImg

		for i in xrange(20):
			self.SetNormalRewardReciveAnimate(i)
			self.SetPrimiumRewardReciveAnimate(i)

	def SetNormalRewardReciveAnimate(self, i):
		NormalAvailable = ui.AniImageBox()
		NormalAvailable.SetParent(self.__children["rewardBoard"])
		NormalAvailable.SetDelay(2.5)
		for j in range(43):
			image_file = MISSION_IMAGE_PATH + "ui/reward_effect/reward_effect_%02d.dds" % j
			NormalAvailable.AppendImage(image_file)
		NormalAvailable.SetPosition((i * 41), 17)
		NormalAvailable.SetShow(self.NormalRecived <= i and self.playerLevel > i)
		self.__children["NormalAvailable_{}".format(i)] = NormalAvailable

	def SetPrimiumRewardReciveAnimate(self, i):
		PrimiumAvailable = ui.AniImageBox()
		PrimiumAvailable.SetParent(self.__children["rewardBoard"])
		PrimiumAvailable.SetDelay(2.5)
		for j in range(43):
			image_file = MISSION_IMAGE_PATH + "ui/reward_effect/reward_effect_%02d.dds" % j
			PrimiumAvailable.AppendImage(image_file)
		PrimiumAvailable.SetPosition((i * 41), 112)
		PrimiumAvailable.SetShow(self.PrimiumRecived <= i and self.isPrimium and self.playerLevel > i)
		self.__children["PrimiumAvailable_{}".format(i)] = PrimiumAvailable

	def SetNormalRewardAnimate(self):
		slot = self.NormalRecived
		key = "NormalAvailable_{}".format(slot)
		if self.__children.get(key) == None:
			return
		if self.NormalRecived > slot or self.playerLevel <= slot:
			return
		if not self.CanClickNormal:
			return
		self.CanClickNormal = False
		self.__children[key].Hide()
		self.__children[key] = ui.AniImageBox()
		self.__children[key].SetParent(self.__children["rewardBoard"])
		self.__children[key].SetDelay(2)
		for j in range(57):
			image_file = MISSION_IMAGE_PATH + "ui/lock/item_unlocked_%02d.dds" % j
			self.__children[key].AppendImage(image_file)
		self.__children[key].SetPosition((slot * 41), 17)
		self.__children[key].ResetFrame()
		self.__children[key].Show()
		self.__children[key].SetEndFrameEvent(ui.__mem_func__(self.GetNormalReward), slot)

	def SetPrimiumRewardAnimate(self):
		slot = self.PrimiumRecived
		key = "PrimiumAvailable_{}".format(slot)
		if self.__children.get(key) == None:
			return
		if self.PrimiumRecived > slot or self.playerLevel <= slot or not self.isPrimium:
			return
		if not self.CanClickPrimium:
			return
		self.CanClickPrimium = False
		self.__children[key].Hide()
		self.__children[key] = ui.AniImageBox()
		self.__children[key].SetParent(self.__children["rewardBoard"])
		self.__children[key].SetDelay(2)
		for j in range(57):
			image_file = MISSION_IMAGE_PATH + "ui/lock/item_unlocked_%02d.dds" % j
			self.__children[key].AppendImage(image_file)
		self.__children[key].SetPosition((slot * 41), 112)
		self.__children[key].ResetFrame()
		self.__children[key].Show()
		self.__children[key].SetEndFrameEvent(ui.__mem_func__(self.GetPrimiumReward), slot)

	def GetNormalReward(self, slot):
		key = "NormalAvailable_{}".format(slot)
		self.__children[key].Hide()
		self.__children[key] = None
		net.SendChatPacket("/battlepass_reward {}".format(int(False)))

	def GetPrimiumReward(self, slot):
		key = "PrimiumAvailable_{}".format(slot)
		self.__children[key].Hide()
		self.__children[key] = None
		net.SendChatPacket("/battlepass_reward {}".format(int(True)))

	def OnMouseOverInNormalItem(self, slot):
		if self.tooltipItem:
			itemList = self.rewardItemsNormal[slot]
			self.tooltipItem.SetItemToolTip(itemList[0])

	def OnMouseOverInPrimiumItem(self, slot):
		if self.tooltipItem:
			itemList = self.rewardItemsPrimium[slot]
			self.tooltipItem.SetItemToolTip(itemList[0])

	def OnMouseOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		if self.__children.get("clockTxt"):
			leftTime = max(0, self.clockLeftTime - app.GetTime())
			self.__children["clockTxt"].SetText(localeInfo.SecondToDHMS(leftTime))

		for i in xrange(2):
			key = "missionClockText_{}".format(i)
			if self.__children.get(key):
				leftTime = max(0, self.missionClockLeftTime[i] - app.GetTime())
				self.__children[key].SetText(localeInfo.SecondToDHMS(leftTime))

	def SetBattlePassData(self, Month, Level, Exp, isNormalRecived, isPrimiumRecived, isPrimium, dailyTime, weeklyTime, monthTime):
		self.__children["mainBoard"].SetTitleName(localeInfo.BATTLEPASS_TITLE + " " + MONTH_DICT[int(Month)])
		self.playerLevel = Level
		self.__children["playerLevelTxt"].SetText("Lv.{}".format(Level))
		self.__children["expGauge"].SetPercentage(Exp, MAX_EXP)
		self.__children["playeExpTxt"].SetText("{}/{}".format(Exp, MAX_EXP))
		self.clockLeftTime = monthTime + app.GetTime()

		self.isPrimium = isPrimium
		if isNormalRecived != self.NormalRecived:
			self.CanClickNormal = True
		if isNormalRecived != self.PrimiumRecived:
			self.CanClickPrimium = True

		self.RefreshRewardRecives(isNormalRecived, isPrimiumRecived, isPrimium)
		self.missionClockLeftTime.append(dailyTime + app.GetTime())
		self.missionClockLeftTime.append(weeklyTime + app.GetTime())

		self.RefreshRewardLocks(Level, isPrimium)
		if self.isPrimium:
			self.__children["bigLock"].Hide()
		else:
			self.__children["bigLock"].Show()

	def RefreshRewardLocks(self, level, isPrimium):
		i = 0
		while self.__children.get("normalSlotLock_{}".format(i)) is not None:
			normalKey = "normalSlotLock_{}".format(i)
			primiumKey = "primiumSlotLock_{}".format(i)

			if self.playerLevel > i:
				if self.NormalRecived > i:
					self.__children[normalKey].LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_done.png")
					self.__children[normalKey].Show()
				else:
					self.__children[normalKey].Hide()
			else:
				self.__children[normalKey].LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_lock.png")
				self.__children[normalKey].Show()

			if self.playerLevel > i and isPrimium:
				if self.PrimiumRecived > i:
					self.__children[primiumKey].LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_done.png")
					self.__children[primiumKey].Show()
				else:
					self.__children[primiumKey].Hide()
			else:
				self.__children[primiumKey].LoadImage(MISSION_IMAGE_PATH + "ui/slice/items/item_lock.png")
				self.__children[primiumKey].Show()

			i += 1

	def RefreshRewardRecives(self, isNormalRecived, isPrimiumRecived, isPrimium):
		self.NormalRecived = isNormalRecived
		self.PrimiumRecived = isPrimiumRecived

		i = 0
		while self.__children.get("NormalAvailable_{}".format(i)) is not None or self.__children.get("PrimiumAvailable_{}".format(i)) is not None:
			normalKey = "NormalAvailable_{}".format(i)
			primiumKey = "PrimiumAvailable_{}".format(i)

			if self.__children.get(normalKey) is None:
				normalAvail = ui.AniImageBox()
				normalAvail.SetParent(self.__children["rewardBoard"])
				normalAvail.SetDelay(2.5)
				for j in range(43):
					image_file = MISSION_IMAGE_PATH + "ui/reward_effect/reward_effect_%02d.dds" % j
					normalAvail.AppendImage(image_file)
				normalAvail.SetPosition((i * 41), 17)
				normalAvail.SetShow(self.NormalRecived <= i and self.playerLevel > i)
				self.__children[normalKey] = normalAvail
			else:
				self.__children[normalKey].SetShow(self.NormalRecived <= i and self.playerLevel > i)

			if self.__children.get(primiumKey) is None:
				primiumAvail = ui.AniImageBox()
				primiumAvail.SetParent(self.__children["rewardBoard"])
				primiumAvail.SetDelay(2.5)
				for j in range(43):
					image_file = MISSION_IMAGE_PATH + "ui/reward_effect/reward_effect_%02d.dds" % j
					primiumAvail.AppendImage(image_file)
				primiumAvail.SetPosition((i * 41), 112)
				primiumAvail.SetShow(self.PrimiumRecived <= i and self.isPrimium and self.playerLevel > i)
				self.__children[primiumKey] = primiumAvail
			else:
				self.__children[primiumKey].SetShow(self.PrimiumRecived <= i and self.isPrimium and self.playerLevel > i)

			i += 1

	def SetRewardItems(self, rewards_list):
		for vnum, count, vnum2, count2 in rewards_list:
			self.rewardItemsNormal.append([vnum, count])
			self.rewardItemsPrimium.append([vnum2, count2])

	def format_million(self, num):
		if num < 1000000:
			return str(num)

		millions = num / 1000000.0
		if millions == int(millions):
			return localeInfo.MILLION_TEXT_1 % int(millions)
		else:
			return localeInfo.MILLION_TEXT_2 % round(millions, 1)

	def SetBattlePassMissions(self, missions_list):
		for slot, type, count, remain, exp, isDaily in missions_list:
			if isDaily:
				self.__children["dailyMissionTypeIcon_{}".format(slot)].LoadImage(MISSION_IMAGE_PATH + "ui/slice/daily_icons/battlepass_mission_%d.png" % (type))
				self.__children["dailyMissionGauge_{}".format(slot)].SetPercentage(count, remain)
				self.__children["dailyMissionGaugeTxt_{}".format(slot)].SetText("%d/%d" % (count, remain))
				self.__children["dailyMissionTxt_{}".format(slot)].SetText(MAX_MISSION_TIP[type] % (self.format_million(remain)))
				self.__children["dailyMissionExp_{}".format(slot)].SetText("%d" % (exp))
				if count == remain:
					self.__children["dailyMissionLock_{}".format(slot)].Show()
					self.__children["refreshDailyButton_{}".format(slot)].Hide()
				else:
					self.__children["dailyMissionLock_{}".format(slot)].Hide()
					self.__children["refreshDailyButton_{}".format(slot)].Show()
			else:
				self.__children["weeklyMissionTypeIcon_{}".format(slot)].LoadImage(MISSION_IMAGE_PATH + "ui/slice/weekly_icons/battlepass_mission_%d.png" % (type))
				self.__children["weeklyMissionGauge_{}".format(slot)].SetPercentage(count, remain)
				self.__children["weeklyMissionGaugeTxt_{}".format(slot)].SetText("%d/%d" % (count, remain))
				self.__children["weeklyMissionTxt_{}".format(slot)].SetText(MAX_MISSION_TIP[type] % (self.format_million(remain)))
				self.__children["weeklyMissionExp_{}".format(slot)].SetText("%d" % (exp))
				if count == remain:
					self.__children["weeklyMissionLock_{}".format(slot)].Show()
					self.__children["refreshWeeklyButton_{}".format(slot)].Hide()
				else:
					self.__children["weeklyMissionLock_{}".format(slot)].Hide()
					self.__children["refreshWeeklyButton_{}".format(slot)].Show()

	def SetBattlePassDailyProgress(self, slot, count, remain):
		self.__children["dailyMissionGauge_{}".format(slot)].SetPercentage(count, remain)
		self.__children["dailyMissionGaugeTxt_{}".format(slot)].SetText("{}/{}".format(count, remain))
		if count == remain:
			self.__children["dailyMissionLock_{}".format(slot)].Show()
		else:
			self.__children["dailyMissionLock_{}".format(slot)].Hide()

	def SetBattlePassWeeklyProgress(self, slot, count, remain):
		self.__children["weeklyMissionGauge_{}".format(slot)].SetPercentage(count, remain)
		self.__children["weeklyMissionGaugeTxt_{}".format(slot)].SetText("{}/{}".format(count, remain))
		if count == remain:
			self.__children["weeklyMissionLock_{}".format(slot)].Show()
		else:
			self.__children["weeklyMissionLock_{}".format(slot)].Hide()

	def Open(self):
		if self.IsShow():
			self.Close()
			return
		self.Show()
		if not self.__children.get("normalItemsSlot_0"):
			self.SetRewards()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		if self.ItemQuestionDlg:
			self.ItemQuestionDlg.Close()
			self.ItemQuestionDlg = None
		self.Hide()

class ItemQuestionDlg(ui.Board):
 
	def __init__(self):
		ui.Board.__init__(self)
		self.__children = {}
		self.ItemRequired = 0
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.__CreateDialog()
 
	def __CreateDialog(self):
		WIDTH = 285
		HEIGHT = 160
 
		self.AddFlag("movable")
		self.AddFlag("float")
		#self.AddFlag("animate")  # only uncomment if you have those systems
		self.SetSize(WIDTH, HEIGHT)
 
		mainBoard = ui.Board()
		mainBoard.SetParent(self)
		mainBoard.SetPosition(0, 0)
		mainBoard.SetSize(WIDTH, HEIGHT)
		mainBoard.Show()
		self.__children["mainBoard"] = mainBoard
 
		backgroundimg = ui.ImageBox()
		backgroundimg.SetParent(self.__children["mainBoard"])
		backgroundimg.LoadImage("d:/ymir work/ui/skillcolor/skill_color_window.png")
		backgroundimg.SetPosition(10, 10)
		backgroundimg.Show()
		self.__children["backgroundimg"] = backgroundimg
 
		textLine = ui.TextLine()
		textLine.SetParent(self.__children["mainBoard"])
		textLine.SetPosition(WIDTH / 2, 30)
		textLine.SetHorizontalAlignCenter()
		textLine.Show()
		self.__children["textLine"] = textLine
 
		textLine2 = ui.TextLine()
		textLine2.SetParent(self.__children["mainBoard"])
		textLine2.SetPosition(WIDTH / 2, 50)
		textLine2.SetHorizontalAlignCenter()
		textLine2.Show()
		self.__children["textLine2"] = textLine2
 
		regist_slot_img = ui.ExpandedImageBox()
		regist_slot_img.SetParent(self.__children["mainBoard"])
		regist_slot_img.LoadImage("d:/ymir work/ui/public/Slot_Base.sub")
		regist_slot_img.SetPosition(127, 75)
		regist_slot_img.Show()
		self.__children["regist_slot_img"] = regist_slot_img
 
		itemimg = ui.SlotWindow()
		itemimg.SetParent(self.__children["regist_slot_img"])
		itemimg.SetPosition(-6, -6)
		itemimg.SetSize(44, 44)
		itemimg.AppendSlot(0, 6, 6, 32, 32)
		itemimg.SetOverInItemEvent(ui.__mem_func__(self.OverInImgItemSlot))
		itemimg.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		itemimg.Show()
		self.__children["itemimg"] = itemimg
 
		acceptButton = ui.Button()
		acceptButton.SetParent(self.__children["mainBoard"])
		acceptButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		acceptButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		acceptButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		acceptButton.SetText(uiScriptLocale.YES)
		acceptButton.SetSize(61, 21)
		acceptButton.SetPosition(- 40, 123)
		acceptButton.SetWindowHorizontalAlignCenter()
		acceptButton.Show()
		self.__children["acceptButton"] = acceptButton
 
		cancelButton = ui.Button()
		cancelButton.SetParent(self.__children["mainBoard"])
		cancelButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		cancelButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		cancelButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		cancelButton.SetText(uiScriptLocale.NO)
		cancelButton.SetSize(61, 21)
		cancelButton.SetPosition(40, 123)
		cancelButton.SetWindowHorizontalAlignCenter()
		cancelButton.Show()
		self.__children["cancelButton"] = cancelButton
 
	def OverInImgItemSlot(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetItemToolTip(self.ItemRequired)
 
	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()
 
	def SetUp(self):
		self.__children["itemimg"].SetItemSlot(0, self.ItemRequired, 0)
		self.__children["itemimg"].RefreshSlot()
 
	def Open(self, vnum):
		self.ItemRequired = int(vnum)
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		self.SetUp()
 
	def Close(self):
		self.Hide()
 
	def SetAcceptEvent(self, event):
		self.__children["acceptButton"].SetEvent(event)
 
	def SetCancelEvent(self, event):
		self.__children["cancelButton"].SetEvent(event)
 
	def SetText(self, text):
		self.__children["textLine"].SetText(text)
 
	def SetText2(self, text):
		self.__children["textLine2"].SetText(text)
 
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
		
		