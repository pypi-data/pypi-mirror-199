class examples:
    ECHO = {
        "optimizer": "ECHO",
        "msg": [[1, 2], [1, 1], [1, 2]]
    }
    VRPTW = {
        "optimizer": "VRPTW",
        "vehicles":
            # vehicle number, vehicle capacity
            [25, 80],
        "nodes":
            # node	x-coord	y-coord	demand 	ready_time	due_date service_time
            [[0, 40, 50, 0, 0, 1236, 0],
            [1, 45, 68, 10, 912, 967, 90],
            [2, 45, 70, 30, 825, 870, 90],
            [3, 42, 66, 10, 65, 146, 90],
            [4, 42, 68, 10, 727, 782, 90],
            [5, 42, 65, 10, 15, 67, 90],
            [6, 40, 69, 20, 621, 702, 90],
            [7, 40, 66, 20, 170, 225, 90],
            [8, 38, 68, 20, 255, 324, 90],
            [9, 38, 70, 10, 534, 605, 90],
            [10, 35, 66, 10, 357, 410, 90]],
        "distance":
            #[[round(math.sqrt((data["Nodes"][i][1] - data["Nodes"][j][1])**2 + (data["Nodes"][i][2] - data["Nodes"][j][2])**2),5)  for j in range(10)] for i in range(10)]
            [[0.0, 18.68154, 20.61553, 16.12452, 18.11077, 15.13275, 19.0, 16.0, 18.11077, 20.09975, 16.76305],
            [18.68154, 0.0, 2.0, 3.60555, 3.0, 4.24264, 5.09902, 5.38516, 7.0, 7.28011, 10.19804],
            [20.61553, 2.0, 0.0, 5.0, 3.60555, 5.83095, 5.09902, 6.40312, 7.28011, 7.0, 10.77033],
            [16.12452, 3.60555, 5.0, 0.0, 2.0, 1.0, 3.60555, 2.0, 4.47214, 5.65685, 7.0],
            [18.11077, 3.0, 3.60555, 2.0, 0.0, 3.0, 2.23607, 2.82843, 4.0, 4.47214, 7.28011],
            [15.13275, 4.24264, 5.83095, 1.0, 3.0, 0.0, 4.47214, 2.23607, 5.0, 6.40312, 7.07107],
            [19.0, 5.09902, 5.09902, 3.60555, 2.23607, 4.47214, 0.0, 3.0, 2.23607, 2.23607, 5.83095],
            [16.0, 5.38516, 6.40312, 2.0, 2.82843, 2.23607, 3.0, 0.0, 2.82843, 4.47214, 5.0],
            [18.11077, 7.0, 7.28011, 4.47214, 4.0, 5.0, 2.23607, 2.82843, 0.0, 2.0, 3.60555],
            [20.09975, 7.28011, 7.0, 5.65685, 4.47214, 6.40312, 2.23607, 4.47214, 2.0, 0.0, 5.0],
            [16.76305, 10.19804, 10.77033, 7.0, 7.28011, 7.07107, 5.83095, 5.0, 3.60555, 5.0, 0.0]]

    }
    CLSP = {
        "optimizer": "CLSP",
        "Products":
        # setup_cost holding_cost variable_time setup_time
            [[748.0, 1.0, 1, 0], [1053.0, 1.0, 1, 0]],
        "Capacity": [1247, 1247, 1247, 1247, 1247, 1247, 1247],
        "Demand":
            [[0, 96, 117, 174, 137, 145, 117],
            [91, 79, 99, 0, 108, 0, 100]]
    }

    ###### to be inlcuded ########
    MCND = {
        "optimizer": "CND",  # multicommodity capacitated network design
        "Nodes":  # Commodity DEMAND
            [[0, 10],
            [1, -10]],
        "Arcs":  # ORIGIN DESTINATION	CAPCITY VAR_COST FIXED_COST
            [[0, 40, 50, 10.2, 1000],
            [1, 45, 68, 10.2, 1000],
            [2, 45, 70, 10.2, 1000],
            [3, 42, 66, 10.2, 1000]]
    }
    CND = {
        "optimizer": "CND",  # capacitated network design
        "Nodes":  # ID  DEMAND
            [[0, 10],
            [1, -10]],
        "Arcs":  # ORIGIN DESTINATION	CAPCITY VAR_COST FIXED_COST
            [[0, 40, 50, 10.2, 1000],
            [1, 45, 68, 10.2, 1000],
            [2, 45, 70, 10.2, 1000],
            [3, 42, 66, 10.2, 1000]]
    }
    MCF = {
        "optimizer": "MCF",  # minimum cost flows
        "Nodes":  # ID  DEMAND
            [[0, 10],
            [1, -10]],
        "Arcs":  # ORIGIN DESTINATION	CAPCITY
            [[0, 40, 50],
            [1, 45, 68],
            [2, 45, 70],
            [3, 42, 66]]
    }
    HCVRPTW = {
        "optimizer": "HCVRPTW",
        "Vehicles":  # VEHICLE_NUMBER	TYPE
            [25, "LDV"],
        "Nodes":  # NODE	XCOORD	YCOORD	ELEVATION	DEMAND 	READY_TIME	DUE_DATE	SERVICE_TIME
            [[0, 40, 50, 313, 0, 0, 1236, 0],
            [1, 45, 68, 37, 10, 912, 967, 90],
            [2, 45, 70, 781, 30, 825, 870, 90],
            [3, 42, 66, 974, 10, 65, 146, 90]]
    }
    HVRP = {
        "optimizer": "HVRP",
        "Vehicles":  # VEHICLE_NUMBER CAPACITY
            [[25, 2000], [25, 2000]],
        "Nodes":  # NODE	XCOORD	YCOORD	DEMAND
            [[0, 40, 50, 0],
            [1, 45, 68, 10],
            [2, 45, 70, 30],
            [3, 42, 66, 10]]
    }
    CVRP = {
        "optimizer": "CVRP",
        "Vehicles":  # VEHICLE_NUMBER CAPACITY
            [25, 2000],
        "Nodes":  # NODE	XCOORD	YCOORD	DEMAND
            [[0, 40, 50, 0],
            [1, 45, 68, 10],
            [2, 45, 70, 30],
            [3, 42, 66, 10]]
    }

    TSP = {
        "optimizer": "TSP",
        "Nodes":  # NODE	XCOORD	YCOORD
            [[0, 40, 50],
            [1, 45, 68],
            [2, 45, 70],
            [3, 42, 66]]
    }
