isComplete(T :: btree()) ->
	Q0 = queue:in(T, queue():new()).
	icHelper(Q0)

icHelper(Q) ->
	if (queue:out(Q) == btree:empty) ->
		if (is_empty(Q)) ->
			true
		true ->
			false
	true ->
		icHelper(out(Q))

icHelper(Q) ->
	{{value, T}, Q2} = queue:out(Q),
	case T of
		{empty} -> all_empty(Q2);
		{node, _D, LT, RT} ->
			icHelper(queue:in(RT, queue:in(LT, Q2)))
	end.

all_empty(Q) ->
	case queue:is_empty(Q) of
		true -> true
		_ -> case queue:out(Q) of
			{{value, {empty}}, Q2} ->
				all_empty(Q2);
			{{value, _}, Q2} -> false
	end.

