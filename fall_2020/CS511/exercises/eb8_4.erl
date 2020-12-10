-module(eb8_4).
-compile(export_all).

start(T, N) ->
	L = [spawn(?MODULE, client, []) || _ <- lists:seq(1, N)],
	C = spawn(?MODULE, timer, [T, L]),
	C.

% T is tick rate, PIDs is list of PIDs which receive
timer(T, PIDs) ->
	timer:sleep(T),
	[ Pid!{tick} || Pid <- PIDs],
	timer(T, PIDs).

client() ->
	receive
		{tick} ->
			io:format("received tick."),
			client()
	end.