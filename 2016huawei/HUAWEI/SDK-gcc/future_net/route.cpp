
#include "route.h"
#include "lib_record.h"
#include "types.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cstring>
#include <string>
#include "methods.h"
#include "statistics.h"

using std::cin;
using std::cout;
using std::endl;
vector<vector<edge_t> > graph_gl(500,vector<edge_t>(500));
std::vector<int>  demand_gl;
//你要完成的功能总入口
void search_route(char *topo[5000], int edge_num, char *demand)
{
	//record_result(result[i]);

	/****************init_graph****************/

	{
		int edge_index = 0, start = 0, end = 0, weight  = 0;
		for (int i =0; i!=edge_num; i++)
		{
			sscanf(topo[i],"%d,%d,%d,%d",&edge_index,&start,&end,&weight);
			if (weight < graph_gl[start][end].weight)		//reduce edge info
			{
				graph_gl[start][end].weight = weight;
				graph_gl[start][end].index = edge_index;
			}
		}
		for (int i  = 0 ; i != 10; i++)
			for(int j = 0; j != 10; j++)
				cout << graph_gl[i][j].weight << " ";
			cout << endl;
	}

	/****************init_demand**************/

	{
		char de_ptr[50]; 
		sscanf(demand,"%d,%d,%s",&start_gl,&end_gl,de_ptr);
		char* de_buf = de_ptr;
		char* temp;
		while((temp = strsep(&de_buf, "|")) != NULL)
		{
			demand_gl.push_back(atoi(temp));
		}
	}

	/****************main method****************/
		//waht the fuck!!!
		ant_colony(); 

}
