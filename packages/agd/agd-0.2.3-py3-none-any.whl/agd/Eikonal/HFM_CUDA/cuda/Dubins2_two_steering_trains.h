#pragma once 

// Maximum of a family of four schemes
#define nmix_macro 4 
const bool mix_is_min = true; 

// The PDE is solved in three dimensional space
#define curvature_macro 1
#include "Geometry3.h"

// Choose between a forward only vehicle, and one that can move forward and backwards 
// (with no commutation cost here).
#if reversible_macro
const Int nsym=decompdim; 
const Int nfwd=0;
#else
const Int nsym=0; 
const Int nfwd=decompdim;
#endif

#include "Constants.h"
#include "Decomp_v_.h"

