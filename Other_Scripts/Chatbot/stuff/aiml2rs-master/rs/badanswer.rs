// Converted using aiml2rs on: Wed Jan 28 03:07:26 2015
! version = 2.0

+ bad answer
- <set badanswer-that-full=<undef>> <set alicetopic=badanswer-prelim>Would you like to teach me a new answer to "<get badanswer-input>"?

+ *
* <get star> == yes =>  OK, what should I have said?<set alicetopic=learning new answers>
* <get star> == no =>  OK, let's forget it then.<set alicetopic=learning new answers>
- <set star=<star>>Yes or No?</li>

+ * *
- <@>

+ *
% ok what should i have said
* <get badanswer-that> != undefined =>  <set alicetopic=BADANSWER> Does this depend on me having just said, "<get badanswer-that-full>"? 
- "<set badanswer-newresp=<input>><get badanswer-newresp>..."? <set alicetopic=BADANSWER2> Do you want me to remember that?</li>

+ * *
% ok what should i have said
- <@>

+ 
* <get response1> == OK, what should I have said => 
* <get star> == no => I'll try to remember to respond, "<get badanswer-newresp>" when you say, "<get badanswer-input>" <learn>   <eval>{uppercase}<get badanswer-input>{/uppercase}</eval>   <eval><get badanswer-newresp></eval>  
- 

+ 
* <get star> == yes => I'll try to remember to respond, "<get badanswer-newresp>" when you say, "<get badanswer-input>" if I have just said "<get badanswer-that-full>" <learn>   <eval>{uppercase}<get badanswer-input>{/uppercase}</eval>   <eval>{uppercase}<get badanswer-that>{/uppercase}</eval>   <eval><get badanswer-newresp></eval>  
- Yes or No?</li>

+ 
* <get star> == yes => I'll try to remember to respond, "<get badanswer-newresp>" when you say, "<get badanswer-input>" if I have just said "<get badanswer-that-full>" <learn>   <eval>{uppercase}<get badanswer-input>{/uppercase}</eval>   <eval>{uppercase}<get badanswer-that>{/uppercase}</eval>   <eval><get badanswer-newresp></eval>  
- Yes or No?</li>

+ * *
- <@>

+ 
* <get star> == no => OK, let's forget it then.<set alicetopic=learning new answers>
- Yes or No?</li>

+ 
* <get star> == no => OK, let's forget it then.<set alicetopic=learning new answers>
- Yes or No?</li>

+ * *
- <@>

+ wrong
@ bad answer

+ not right
@ bad answer

+ that is wrong
@ bad answer

+ that is not right
@ bad answer

+ that is incorrect
@ bad answer

+ that answer is not correct
@ bad answer

+ that answer is incorrect
@ bad answer

+ that answer is wrong
@ bad answer

+ that answer is not right
@ bad answer

+ that answer was bad
@ bad answer

+ that was a bad answer
@ bad answer

+ that was an incorrect answer
@ bad answer

+ that was the wrong answer
@ bad answer

+ that answer was not right
@ bad answer

+ wrong answer
@ bad answer

+ your answer was wrong
@ bad answer

+ your answer was not right
@ bad answer

+ your answer was not correct
@ bad answer

+ can i teach you
- Yes, if I give you a bad answer, just say "Bad answer" and you can teach me a new response.

+ can you learn
@ can i teach you

+ do you learn
@ can i teach you

+ can i teach you *
@ can i teach you

+ can you learn *
@ can i teach you

+ will you learn *
@ can i teach you

+ if * will you learn *
@ can i teach you

+ do you learn *
@ can i teach you

