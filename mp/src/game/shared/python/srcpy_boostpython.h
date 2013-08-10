//====== Copyright © Sandern Corporation, All rights reserved. ===========//
//
// Purpose: 
//
// $NoKeywords: $
//=============================================================================//

#ifndef SRCPY_BOOSTPYTHON_H
#define SRCPY_BOOSTPYTHON_H
#ifdef _WIN32
#pragma once
#endif

#include "valve_minmax_off.h"
#include <boost/python.hpp>
#include "valve_minmax_on.h"

#ifdef _DEBUG
	// boost redefines _DEBUG
	#undef _DEBUG
	#define _DEBUG 1
#endif // _DEBUG

#endif // SRCPY_BOOSTPYTHON_H
