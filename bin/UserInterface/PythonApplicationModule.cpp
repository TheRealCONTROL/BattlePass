

#ifdef ENABLE_BATTLEPASS_SYSTEM
	PyModule_AddIntConstant(poModule, "ENABLE_BATTLEPASS_SYSTEM", true);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_BATTLEPASS_SYSTEM", false);
#endif