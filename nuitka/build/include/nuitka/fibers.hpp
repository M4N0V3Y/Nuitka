//     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
//
//     Part of "Nuitka", an optimizing Python compiler that is compatible and
//     integrates with CPython, but also works on its own.
//
//     Licensed under the Apache License, Version 2.0 (the "License");
//     you may not use this file except in compliance with the License.
//     You may obtain a copy of the License at
//
//        http://www.apache.org/licenses/LICENSE-2.0
//
//     Unless required by applicable law or agreed to in writing, software
//     distributed under the License is distributed on an "AS IS" BASIS,
//     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//     See the License for the specific language governing permissions and
//     limitations under the License.
//
#ifndef __NUITKA_FIBERS_H__
#define __NUITKA_FIBERS_H__

#ifdef __WIN32__
#include <windows.h>
#else
#include <ucontext.h>
#endif

typedef struct _Fiber
{
#if defined __WIN32__
    void *ss_sp;
    size_t ss_size;

    CONTEXT f_context;
#else
    ucontext_t f_context;
#endif
} Fiber;

extern "C" void initFiber( Fiber *to );

extern "C" void swapFiber( Fiber *to, Fiber *from );

extern "C" void prepareFiber( Fiber *to, void *code, unsigned long arg );

extern "C" void releaseFiber( Fiber *to );

#endif
