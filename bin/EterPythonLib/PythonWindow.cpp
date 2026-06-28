
	void CAniImageBox::OnUpdate()
	{
	#if defined(ENABLE_CLIP_MASK)
		if (m_bEnableMask && m_pMaskWindow)
			m_rMaskRect = m_pMaskWindow->GetRect();
	#endif

		if (++m_bycurDelay < m_byDelay)
			return;

		m_bycurDelay = 0;

		if (m_ImageVector.size() <= 1)
			return;

		if (++m_bycurIndex >= m_ImageVector.size())
		{
			m_bycurIndex = 0;
			OnEndFrame(); // -> Add This Line
		}
	}


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
	
	
	// Under
	void CAniImageBox::OnChangePosition()
	{
		for (auto& img : m_ImageVector)
		{
			img->SetPosition(m_rect.left, m_rect.top);
		}
	}

	// Add This Func
	void CAniImageBox::OnEndFrame()
	{
		PyCallClassMemberFunc(m_poHandler, "OnEndFrame", BuildEmptyTuple());
	}
