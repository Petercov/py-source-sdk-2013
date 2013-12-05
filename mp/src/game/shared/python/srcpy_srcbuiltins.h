//====== Copyright � Sandern Corporation, All rights reserved. ===========//
//
// Purpose: 
//
// $NoKeywords: $
//=============================================================================//

#ifndef SRCPY_SRCBUILTINS_H
#define SRCPY_SRCBUILTINS_H
#ifdef _WIN32
#pragma once
#endif

#include <tier0/dbg.h>

// These classes redirect input to Msg and Warning respectively
class SrcPyStdOut 
{
public:
	void write( const char *msg ) { Msg( "%s", msg ); }
	void flush() {}
};

class SrcPyStdErr 
{
public:
	void write( const char *msg ) { Warning( "%s", msg ); }
	void flush() {}
};

// Wrappers for Msg, Warning and DevMsg (Python does not use VarArgs)
inline void SrcPyMsg( const char *msg ) { Msg( "%s", msg ); }
inline void SrcPyWarning( const char *msg ) { Warning( "%s", msg ); }
inline void SrcPyDevMsg( int level, const char *msg ) { DevMsg( level, "%s", msg ); }

#endif // SRCPY_SRCBUILTINS_H