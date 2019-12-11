from a_star import *
def alt_path(prev_path, graf, param):
	if param == 1:
		for edge_id in prev_path:
			#print(graf.edge[edge_id].length)
			graf.edge[edge_id].alt_velocity = graf.edge[edge_id].velocity / 1.1
			#print(graf.edge[edge_id].alt_velocity, graf.edge[edge_id].velocity)
			graf.edge[edge_id].count_actual_time_of_travel(graf.edge[edge_id].alt_velocity)
	else:
		for edge_id in prev_path:
			graf.edge[edge_id].alt_length = graf.edge[edge_id].length * 1.05
			graf.edge[edge_id].cur_length = graf.edge[edge_id].alt_length
	path, i, path_edge = A_star(graf, graf.node['464430.25,572320.14'], graf.node['481488.72,574638.42'], param)
	return path, i, path_edge