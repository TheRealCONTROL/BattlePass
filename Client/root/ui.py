
# add this class if you don't have it !

class __safe_func__(object):
	__slots__ = ("call", "saved_args")

	def __init__(self, mfunc, *saved_args):
		self.saved_args = tuple(saved_args)

		im_func = getattr(mfunc, "im_func", None)
		im_self = getattr(mfunc, "im_self", None)

		# Bound method
		if im_func and im_self:
			self._wrap_bound(im_func, im_self)
			return

		# Plain function / builtin / cython
		self._wrap_plain(mfunc)

	def _wrap_bound(self, func, obj):
		obj_ref = weakref.ref(obj)
		argc = func.func_code.co_argcount
		flags = func.func_code.co_flags
		sa = self.saved_args

		if flags & CO_VARARGS or argc > 1:
			def wrapper(*args):
				o = obj_ref()
				if o is None:
					return None
				return func(o, *(sa + args) if sa else args)
			self.call = wrapper
		elif sa:
			def wrapper(*args):
				o = obj_ref()
				if o is None:
					return None
				return func(o, *(args or sa))
			self.call = wrapper
		else:
			def wrapper(*args):
				o = obj_ref()
				if o is None:
					return None
				return func(o)
			self.call = wrapper

	def _wrap_plain(self, func):
		sa = self.saved_args
		if sa:
			def wrapper(*args):
				return func(*(sa + args))
			self.call = wrapper
		else:
			self.call = func

	def __call__(self, *args):
		return self.call(*args)

	def __nonzero__(self):  # Python 2
		return bool(self.call)
		




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


	def Lock(self):
		wndMgr.Lock(self.hWnd)

	def Unlock(self):
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	if app.ENABLE_BATTLEPASS_SYSTEM:
		def SetShow(self, isShow):
			if isShow:
				wndMgr.Show(self.hWnd)
			else:
				wndMgr.Hide(self.hWnd)


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


class AniImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		if app.ENABLE_BATTLEPASS_SYSTEM:
			self.eventEndFrame = None
			self.endFrameArgs = None
			self.keyFrameEvent = None


	[...]
	[...]
	[...]
	
	if app.ENABLE_BATTLEPASS_SYSTEM:
		def SetOnEndFrame(self, event):
			self.eventEndFrame = event

		def SetEndFrameEvent(self, event, *args):
			self.eventEndFrame = event
			self.endFrameArgs = args

		def OnEndFrame(self):
			if self.endFrameArgs == None:
				if self.eventEndFrame:
					apply(self.eventEndFrame)
			else:
				if self.eventEndFrame:
					apply(self.eventEndFrame, self.endFrameArgs)
					
		def SetKeyFrameEvent(self, event):
			self.keyFrameEvent = event
	else:
		def OnEndFrame(self):
			pass


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


if app.ENABLE_BATTLEPASS_SYSTEM:
	class BattlePassGauge(Window):

		SLOT_WIDTH = 16
		SLOT_HEIGHT = 7

		GAUGE_TEMPORARY_PLACE = 12
		GAUGE_WIDTH = 16

		def __init__(self):
			Window.__init__(self)
			self.width = 0

		def MakeGauge(self, width, color):

			self.width = max(48, width)

			imgSlotLeft = ImageBox()
			imgSlotLeft.SetParent(self)
			imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/gauge_small/gauge_slot_left.tga")
			imgSlotLeft.Show()

			imgSlotRight = ImageBox()
			imgSlotRight.SetParent(self)
			imgSlotRight.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/gauge_small/gauge_slot_right.tga")
			imgSlotRight.Show()
			imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

			imgSlotCenter = ExpandedImageBox()
			imgSlotCenter.SetParent(self)
			imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/gauge_small/gauge_slot_center.tga")
			imgSlotCenter.Show()
			imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
			imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

			imgGauge = ExpandedImageBox()
			imgGauge.SetParent(self)
			imgGauge.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/gauge_small/gauge_" + color + ".tga")
			imgGauge.Show()
			imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

			imgSlotLeft.AddFlag("attach")
			imgSlotCenter.AddFlag("attach")
			imgSlotRight.AddFlag("attach")

			self.imgLeft = imgSlotLeft
			self.imgCenter = imgSlotCenter
			self.imgRight = imgSlotRight
			self.imgGauge = imgGauge
			self.curValue = 100
			self.maxValue = 100
			self.currentGaugeColor = color

			self.SetSize(width, self.SLOT_HEIGHT)
			
		def SetColor(self, color):
			if (self.currentGaugeColor == color):
				return
				
			self.currentGaugeColor = color
			self.imgGauge.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/gauge_small/gauge_" + color + ".tga")
			self.SetPercentage(self.curValue, self.maxValue)

		def SetPercentage(self, curValue, maxValue):
			if maxValue > 0.0:
				percentage = min(1.0, float(curValue)/float(maxValue))
			else:
				percentage = 0.0
				
			self.lastCurValue = curValue
			self.lastMaxValue = maxValue

			gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
			self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
			
	class ScrollBarHorizontal(Window):

		SCROLLBAR_HEIGHT = 13
		SCROLLBAR_MIDDLE_WIDTH = 1
		SCROLLBAR_BUTTON_HEIGHT = 17
		SCROLLBAR_BUTTON_WIDTH = 17
		SCROLL_BTN_XDIST = 2
		SCROLL_BTN_YDIST = 2

		class MiddleBar(DragButton):
			def __init__(self):
				DragButton.__init__(self)
				self.AddFlag("movable")
				self.SetWindowName("scrollbar_middlebar")

			def MakeImage(self):
				left = ExpandedImageBox()
				left.SetParent(self)
				left.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scrollbar.png")
				left.AddFlag("not_pick")
				left.Show()
				leftScale = ExpandedImageBox()
				leftScale.SetParent(self)
				leftScale.SetPosition(left.GetWidth(), 0)
				leftScale.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scroll_left.png")
				leftScale.AddFlag("not_pick")
				leftScale.Show()

				right = ExpandedImageBox()
				right.SetParent(self)
				right.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scrollbar.png")
				right.AddFlag("not_pick")
				right.Show()
				rightScale = ExpandedImageBox()
				rightScale.SetParent(self)
				rightScale.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scroll_right.png")
				rightScale.AddFlag("not_pick")
				rightScale.Show()

				middle = ExpandedImageBox()
				middle.SetParent(self)
				middle.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scrollbar.png")
				middle.AddFlag("not_pick")
				middle.Show()

				self.left = left
				self.leftScale = leftScale
				self.right = right
				self.rightScale = rightScale
				self.middle = middle

			def Resize(self, width):
				width = max(12, width)
				DragButton.SetSize(self, width, 10)
				self.right.SetPosition(width-4, 0)

				width -= 4*3
				self.middle.SetRenderingRect(0, 0, float(width)/4.0, 0)

			def SetSize(self, width):
				minWidth = self.left.GetWidth() + self.right.GetWidth() + self.middle.GetWidth()
				width = max(minWidth, width)
				DragButton.SetSize(self, width, 10)

				scale = (width - minWidth) / 2 
				extraScale = 0
				if (width - minWidth) % 2 == 1:
					extraScale = 1

				self.leftScale.SetRenderingRect(0, 0, scale - 1, 0)
				self.middle.SetPosition(self.left.GetWidth() + scale, 0)
				self.rightScale.SetPosition(self.middle.GetRight(), 0)
				self.rightScale.SetRenderingRect(0, 0, scale - 1 + extraScale, 0)
				self.right.SetPosition(width - self.right.GetWidth(), 0)

		def __init__(self):
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0
			self.eventScroll = None
			self.eventArgs = None
			self.lockFlag = False

			self.CreateScrollBar()
			self.SetScrollBarSize(0)

			self.scrollStep = 0.20
			self.SetWindowName("NONAME_ScrollBar")

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			leftImage = ExpandedImageBox()
			leftImage.SetParent(self)
			leftImage.AddFlag("not_pick")
			leftImage.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scroll_left.png")
			leftImage.Show()
			
			middleImage = ExpandedImageBox()
			middleImage.SetParent(self)
			middleImage.AddFlag("not_pick")
			middleImage.SetPosition(leftImage.GetWidth(), 0)
			middleImage.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scroll_center.png")
			middleImage.Show()
			
			rightImage = ExpandedImageBox()
			rightImage.SetParent(self)
			rightImage.AddFlag("not_pick")
			rightImage.LoadImage("d:/ymir work/ui/pattern/control_work/battlepass/ui/scrollbars/horizontal/scroll_right.png")
			rightImage.Show()
			
			self.leftImage = leftImage
			self.rightImage = rightImage
			self.middleImage = middleImage

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
			middleBar.Show()
			middleBar.MakeImage()
			middleBar.SetSize(0) # set min width
			self.middleBar = middleBar

		@WindowDestroy
		def Destroy(self):
			self.eventScroll = None
			self.eventArgs = None

		def SetScrollEvent(self, event, *args):
			self.eventScroll = event
			self.eventArgs = args

		def SetMiddleBarSize(self, pageScale):
			self.middleBar.Resize(int(pageScale * float(self.GetWidth() - self.SCROLL_BTN_XDIST*2)))
			realWidth = self.GetWidth() - self.SCROLL_BTN_XDIST*2 - self.middleBar.GetWidth()
			self.pageSize = realWidth

		def SetScrollBarSize(self, width):
			self.SetSize(width, self.SCROLLBAR_HEIGHT)

			self.pageSize = width - self.SCROLL_BTN_XDIST*2 - self.middleBar.GetWidth()

			middleImageScale = float((width-3 - self.SCROLL_BTN_XDIST*2) - self.middleImage.GetWidth()) / float(self.middleImage.GetWidth())
			self.middleImage.SetRenderingRect(0, 0, middleImageScale, 0)
			self.rightImage.SetPosition(width-6, 0)

			self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
				width - self.SCROLL_BTN_XDIST * 2, self.middleBar.GetHeight())
			self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
			
		def SetScrollStep(self, step):
			self.scrollStep = step
		
		def GetScrollStep(self):
			return self.scrollStep
			
		def GetPos(self):
			return self.curPos

		def OnLeft(self):
			self.SetPos(self.curPos-self.scrollStep)

		def OnRight(self):
			self.SetPos(self.curPos+self.scrollStep)

		def SetPos(self, pos, moveEvent = True):
			pos = max(0.0, pos)
			pos = min(1.0, pos)

			newPos = float(self.pageSize) * pos
			self.middleBar.SetPosition(int(newPos) + self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
			if moveEvent == True:
				self.OnMove()

		def OnMove(self):

			if self.lockFlag:
				return

			if 0 == self.pageSize:
				return

			(xLocal, yLocal) = self.middleBar.GetLocalPosition()
			self.curPos = float(xLocal - self.SCROLL_BTN_XDIST) / float(self.pageSize)

			if self.eventScroll:
				apply(self.eventScroll, self.eventArgs)

		def OnMouseLeftButtonDown(self):
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			newPos = float(xMouseLocalPosition) / float(self.GetWidth())
			self.SetPos(newPos)

		def LockScroll(self):
			self.lockFlag = True

		def UnlockScroll(self):
			self.lockFlag = False



\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



if app.ENABLE_BATTLEPASS_SYSTEM:
	def MakeGauge(parent, x, y, size):
		gauge_make = BattlePassGauge()
		gauge_make.SetParent(parent)
		gauge_make.MakeGauge(size, "bpass")
		gauge_make.SetPosition(x, y)
		gauge_make.Show()
		return gauge_make