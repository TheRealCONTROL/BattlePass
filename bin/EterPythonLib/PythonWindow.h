	class CAniImageBox : public CWindow
	{
		[...]
		[...]
		
		protected:
			void OnUpdate();
			void OnRender();
			void OnChangePosition();
			virtual void OnEndFrame(); // <- Add This Line

			bool OnIsType(DWORD dwType);

		protected:
			BYTE m_bycurDelay;
			BYTE m_byDelay;
			BYTE m_bycurIndex;
			std::vector<std::unique_ptr<CGraphicExpandedImageInstance>> m_ImageVector;
	};