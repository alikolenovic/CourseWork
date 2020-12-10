-module(server).

-export([start_server/0]).

-include_lib("./defs.hrl").

-spec start_server() -> _.
-spec loop(_State) -> _.
-spec do_join(_ChatName, _ClientPID, _Ref, _State) -> _.
-spec do_leave(_ChatName, _ClientPID, _Ref, _State) -> _.
-spec do_new_nick(_State, _Ref, _ClientPID, _NewNick) -> _.
-spec do_client_quit(_State, _Ref, _ClientPID) -> _NewState.

start_server() ->
    catch(unregister(server)),
    register(server, self()),
    case whereis(testsuite) of
	undefined -> ok;
	TestSuitePID -> TestSuitePID!{server_up, self()}
    end,
    loop(
      #serv_st{
	 nicks = maps:new(), %% nickname map. client_pid => "nickname"
	 registrations = maps:new(), %% registration map. "chat_name" => [client_pids]
	 chatrooms = maps:new() %% chatroom map. "chat_name" => chat_pid
	}
     ).

loop(State) ->
    receive 
	%% initial connection
	{ClientPID, connect, ClientNick} ->
	    NewState =
		#serv_st{
		   nicks = maps:put(ClientPID, ClientNick, State#serv_st.nicks),
		   registrations = State#serv_st.registrations,
		   chatrooms = State#serv_st.chatrooms
		  },
	    loop(NewState);
	%% client requests to join a chat
	{ClientPID, Ref, join, ChatName} ->
	    NewState = do_join(ChatName, ClientPID, Ref, State),
	    loop(NewState);
	%% client requests to join a chat
	{ClientPID, Ref, leave, ChatName} ->
	    NewState = do_leave(ChatName, ClientPID, Ref, State),
	    loop(NewState);
	%% client requests to register a new nickname
	{ClientPID, Ref, nick, NewNick} ->
	    NewState = do_new_nick(State, Ref, ClientPID, NewNick),
	    loop(NewState);
	%% client requests to quit
	{ClientPID, Ref, quit} ->
	    NewState = do_client_quit(State, Ref, ClientPID),
	    loop(NewState);
	{TEST_PID, get_state} ->
	    TEST_PID!{get_state, State},
	    loop(State)
    end.

%% executes join protocol from server perspective
do_join(ChatName, ClientPID, Ref, State) ->
	ClientNick = maps:get(ClientPID, State#serv_st.nicks),
    case maps:find(ChatName, State#serv_st.chatrooms) of
    	{ok, ChatPID} -> ChatPID!{self(), Ref, register, ClientPID, ClientNick},
    					 OldReg = maps:get(ChatName, State#serv_st.registrations),
    					 Updated = State#serv_st{registrations = maps:put(ChatName, OldReg ++ [ClientPID], State#serv_st.registrations)},
    					 Updated;
    	error -> ChatPID = spawn(chatroom, start_chatroom, [ChatName]), 
    			 maps:put(ChatName, ChatPID, State#serv_st.chatrooms),
    			 ChatPID!{self(), Ref, register, ClientPID, ClientNick},
    			 Updated = State#serv_st{registrations = maps:put(ChatName, [ClientPID], State#serv_st.registrations), chatrooms = maps:put(ChatName, ChatPID, State#serv_st.chatrooms) },
    			 Updated
	end.

%% executes leave protocol from server perspective
do_leave(ChatName, ClientPID, Ref, State) ->
    ChatPID = maps:get(ChatName, State#serv_st.chatrooms),
    Updated = State#serv_st{registrations = maps:put(ChatName, lists:delete([ClientPID], maps:get(ChatName, State#serv_st.registrations)), State#serv_st.registrations)},
    ChatPID!{self(), Ref, unregister, ClientPID},
    ClientPID!{self(), Ref, ack_leave},
    Updated.

%% executes new nickname protocol from server perspective
do_new_nick(State, Ref, ClientPID, NewNick) ->
	case lists:member(NewNick, maps:values(State#serv_st.nicks)) of
		true -> ClientPID!{self(), Ref, err_nick_used},
				State;
		false -> Updated = State#serv_st{nicks = maps:put(ClientPID, NewNick, State#serv_st.nicks)},
				 Fun = fun(ChatName, Pids, AccIn) -> case lists:member(ClientPID, Pids) of true -> AccIn ++ [ChatName]; false -> AccIn end end,
				 Chatrooms = maps:fold(Fun, [], State#serv_st.registrations),
				 lists:foreach(fun(ChatName) -> maps:get(ChatName, State#serv_st.chatrooms)!{self(), Ref, update_nick, ClientPID, NewNick} end, Chatrooms),
				 ClientPID!{self(), Ref, ok_nick},
				 Updated
	end.


clean_map(State, ClientPID) ->
    maps:map(
        fun(Chat, LstPIDS) ->
            case lists:member(ClientPID, LstPIDS) of
                true -> lists:delete(ClientPID, LstPIDS);
                false -> LstPIDS
            end
        end, State#serv_st.registrations).

%% executes client quit protocol from server perspective
do_client_quit(State, Ref, ClientPID) ->
    Fun = fun(ChatName, Pids, AccIn) -> case lists:member(ClientPID, Pids) of true -> AccIn ++ [ChatName]; false -> AccIn end end,
	Chatrooms = maps:fold(Fun, [], State#serv_st.registrations),
	lists:foreach(fun(ChatName) -> maps:get(ChatName, State#serv_st.chatrooms)!{self(), Ref, unregister, ClientPID} end, Chatrooms),
	Updated = State#serv_st{registrations=clean_map(State, ClientPID), nicks=maps:remove(ClientPID, State#serv_st.nicks)},
	ClientPID!{self(), Ref, ack_quit},
	Updated.
	
