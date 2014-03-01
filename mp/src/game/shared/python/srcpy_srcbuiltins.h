//====== Copyright © Sandern Corporation, All rights reserved. ===========//
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
#include "srcpy_boostpython.h"

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

//-----------------------------------------------------------------------------
// Purpose:
//-----------------------------------------------------------------------------
inline void PyCOM_TimestampedLog( const char *msg ) { COM_TimestampedLog( "%s", msg ); }

//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void RegisterTickMethod( boost::python::object method, float ticksignal, bool looped = true, bool userealtime = false );
void UnregisterTickMethod( boost::python::object method );
boost::python::list GetRegisteredTickMethods();
bool IsTickMethodRegistered( boost::python::object method );

void RegisterPerFrameMethod( boost::python::object method );
void UnregisterPerFrameMethod( boost::python::object method );
boost::python::list GetRegisteredPerFrameMethods();
bool IsPerFrameMethodRegistered( boost::python::object method );

#endif // SRCPY_SRCBUILTINS_H