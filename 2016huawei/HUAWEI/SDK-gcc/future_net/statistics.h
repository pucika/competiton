#ifndef __TYPES_H__
#define __TYPES_H__
#include <vector>
#include "types.h"
using std::vector;

extern vector<vector<edge_t> > graph_gl;	//graph info
extern std::vector<int>  demand_gl;	//global demand
extern int start_gl = 0;			//global start
extern int end_gl = 0;			//global end

#endif
