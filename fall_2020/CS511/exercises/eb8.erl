-module(eb8).
-compile(export_all).

start(N) -> 
	C = spawn(?MODULE, counter_server, [0]),
	[spawn(?MODULE, turnstile, [C, 50]) || _ <- lists:seq(1, N)],
	C.

counter_server(State) ->
	receive
		{bump} ->
			counter_server(State + 1);
		{read, From} ->
			From!{State}
	end.

turnstile(C, N) ->
	case N of
		0 -> ok;
		_ -> C!{bump},
			 turnstile(C, N - 1)
	end.
