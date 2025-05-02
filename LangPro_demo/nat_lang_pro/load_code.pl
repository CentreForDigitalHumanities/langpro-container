:- dynamic sen_id/5.  
:- multifile sen_id/5.  
:- discontiguous sen_id/5. 

:- op(601, xfx, (/)).  
:- op(601, xfx, (\)).  
:- multifile ccg/2, id/2.  
:- discontiguous ccg/2, id/2. 

main :-
    load_files(stdin, [stream(user_input)]),
    current_prolog_flag(argv, [Goal|_]),
    call(Goal),
    halt.

main :- halt(1).
