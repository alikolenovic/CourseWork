start() ->
	register (loading_machine , spawn (fun loadingMachine/0)),
	register (control_center , spawn (? MODULE , controlCenterLoop ,[1 ,1])) ,
	[spawn (? MODULE , passengerTrain ,[0]) || _ <- lists : seq (1 ,10)],
	[spawn (? MODULE , passengerTrain ,[1]) || _ <- lists : seq (1 ,10)],
	[spawn (? MODULE , freightTrain ,[0]) || _ <- lists : seq (1 ,5)],
	[spawn (? MODULE , freightTrain ,[1]) || _ <- lists : seq (1 ,5)].

passengerTrain(Direction) ->
	acquireTrack(Direction),
	timer:sleep(rand:uniform(1000)), % passengers get on/off
	releaseTrack(Direction).

freightTrain (_Direction) ->
	acquireTrack(0),
	acquireTrack(1),
	waitForLoadingMachine(), % machine loads / unloads
	releaseTrack(0),
	releaseTrack(1).

loadingMachine () ->
	receive
		{From, permToProcess} ->
			timer:sleep(rand:uniform (1000)) , % processing
			From!{doneProcessing},
			loadingMachine()
	end .

waitForLoadingMachine() -> %% TODO
	whereis(loading_machine)!{self(), permToProcess}
	receive
		{doneProcessing} ->
			ok

releaseTrack(N) ->
	whereis(control_center)!{self(), release, N}.

acquireTrack(N) -> %% TODO
	whereis(control_center)!{self(), acquire, N}.

%% used by acquireTrack and releaseTrack
%% S0 is 0 ( track 0 has been acquired ) or 1 ( track 0 is free )
%% S1 is 0 ( track 1 has been acquired ) or 1 ( track 1 is free )
%% understands two types of messages :
%% {From , acquire ,N} -- acquire track N
%% {From , release ,N} -- release track N
controlCenterLoop(S0, S1) -> %% TODO
    receive
        {_From, acquire, N} ->
            case N of
                1 when S1 > 1 ->
                    controlCenterLoop(S0, S1 - 1)
                0 when S0 > 1 ->
                    controlCenterLoop(S0 - 1, S1)
                end;
        {_From, release, N} ->
            case N of 
                1 ->
                    controlCenterLoop(S0, S1 + 1)
                0 ->
                    controlCenterLoop(S0 + 1, S1)
            end
        end.