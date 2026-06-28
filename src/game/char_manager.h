

#ifdef ENABLE_BATTLEPASS_SYSTEM
	public:
		void ResetBattlePass();
#endif
};

template<class Func>
Func CHARACTER_MANAGER::for_each_pc(Func f)
{
	for (auto& pair : m_map_pkChrByPID)
		f(pair.second);

	return f;
}