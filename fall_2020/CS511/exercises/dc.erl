-module(dc).

dryCleaner (Clean, Dirty) -> % % Clean , Dirty are counters
	receive 
		{dropOffOverall} ->
			dryCleaner(Clean, Dirty + 1);
		{From, dryCleanItem} when Dirty > 0 ->
			dryCleaner(Clean + 1, Dirty);
		{From, pickUpOverall} when Clean > 0 ->
			dryCleaner(Clean - 1, Dirty)
	end.

employee (DC) -> % drop off overall , then pick up a clean one ( if none
% is available , wait ) , and end
	DC!{dropOffOverall},
	receive
		{DC, ok} ->
			DC!{self(), pickUpOverall}
		end.
	
dryCleanMachine (DC) -> % dry clean item ( if none are available , wait ) ,
% then sleep for 1000 milliseconds and repeat
	DC!{self(), dryCleanItem},
	receive
		{DC, ok} -> 
			timer:sleep(1000), dryCleanMachine(DC)
	end.
	

	
start(E, M) ->
	DC =spawn(? MODULE , dryCleaner ,[0 ,0]) ,
	[ spawn(? MODULE , employee ,[DC]) || _ <- lists : seq (1 , E ) ],
	[ spawn(? MODULE , dryCleanMachine ,[DC]) || _ <- lists : seq (1 , M ) ].
