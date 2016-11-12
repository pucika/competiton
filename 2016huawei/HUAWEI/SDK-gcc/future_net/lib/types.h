#ifndef _types_h
#define _types_h
#include <climits>
struct edge_t
{
	int weight;
	int index;
	edge_t(): weight(INT_MAX),index(-1)
	{}
};

#endif