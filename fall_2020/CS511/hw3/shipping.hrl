
%% Record Ship contains the fields ->
%% name: A string value
%% id: Unique integer value
%% container_cap: Max number of containers a ship can hold
-record(ship, {id, name, container_cap}).
%% Record Container contains the fields ->
%% id: Unique integer value
%% weight: Positive integer value of itself
-record(container, {id, weight}).
%% Record Port contains the fields ->
%% name: A string value
%% id: Unique integer value
%% docks: A list of docks for the port, where it can be represented by a
%% 		  unique integer or a character. Only has to be unique at a given port
%% container_cap: Max number of containers a ship can hold
-record(port, {id, name, docks = [], container_cap}).
%% Record Shipping State contains the fields ->
%% ships: List of ships currently in the system
%% containers: a list of containers currently in the system
%% ship_locations: a tuple consisting a port_id, dock_id, and ship_id
%% ship_inventory: a map that takes a ship id and maps it to thje list of
%%				   container ids on that ship
%% port_inventory: a map that takes a port id and maps it to the list of 
%%				   container ids on that port
-record(shipping_state, 
        {
          ships = [],
          containers = [],
          ports = [],
          ship_locations = [],
          ship_inventory = maps:new(),
          port_inventory = maps:new()
         }
       ).


