// Converted using aiml2rs on: Tue Jan 27 18:51:52 2015
! version = 2.0

+ * inquiry
@ <star> inquiry om

+ age inquiry unknown
- How old are you?

+ age inquiry om
- How old are you?

+ age inquiry *
@ random pickup line

+ birthday inquiry unknown
- When is your birthday?

+ birthday inquiry om
- When is your birthday?

+ birthday inquiry *
@ random pickup line

+ does inquiry what
- What are you doing?

+ does inquiry om
- What are you doing?

+ does inquiry *
- Are you still <star>?

+ father inquiry unknown
- Tell me about your father.

+ father inquiry om
- Tell me about your father.

+ father inquiry *
- Tell me more about your family.

+ favroitecolor inquiry what
- What is your favorite color?

+ favoritecolor inquiry om
- What is your favorite color?

+ favoritecolor inquiry *
- What do you have that is <star>?

+ favoritemovie inquiry what
- What is your favorite movie?

+ favoritemovie inquiry om
- What is your favorite movie?

+ favoritemovie inquiry *
- Does that remind you of <star>?

+ firstname inquiry where
- What is your first name?

+ firstname inquiry om
- What is your first name?

+ firstname inquiry *
@ random pickup line

+ gender inquiry unknown
- Are you a man or woman?

+ gender inquiry om
- Are you a man or woman?

+ gender inquiry *
- I like the way you talk.

+ has inquiry what
- Tell me one of your favorite possessions.

+ has inquiry om
- Tell me one of your favorite possessions.

+ has inquiry *
- Tell me more about your <star>.

+ job inquiry where
- What is your job?

+ job inquiry om
- What is your job?

+ job inquiry *
@ random pickup line

+ lastname inquiry where
- What is your last name?

+ lastname inquiry om
- What is your last name?

+ lastname inquiry *
@ random pickup line

+ middlename inquiry where
- What is your middle name?

+ middlename inquiry om
- What is your middle name?

+ middlename inquiry *
@ random pickup line

+ location inquiry where
- Where are you located?

+ location inquiry om
- Where are you located?

+ location inquiry *
- Are you still located in <star>?

+ mother inquiry unknown
- Tell me about your mother.

+ mother inquiry om
- Tell me about your mother.

+ mother inquiry *
- Tell me more about your family.

+ name inquiry where
- What is your name?

+ name inquiry om
- What is your name?

+ name inquiry *
@ random pickup line

+ sign inquiry your starsign
- What is your sign?

+ name inquiry om
- What is your sign?

+ sign inquiry *
- I'm a <bot sign> and you are a <get sign>.

+ status inquiry *
- What is your current status?

+ *
% what is your first name
@ my first name is <star>

+ *
% what is your last name
@ my last name is <star>

+ *
% what is your middle name
@ my middle name is <star>

+ *
% when is your birthday
@ my birthday is <star>

+ she *
% tell me about your mother
@ my mother <star>

+ her *
% tell me about your mother
@ my mother s <star>

+ *
% what is your favorite color
@ my favorite color is <star>

+ woman
% are you a man or a woman
- <set gender=woman> Thanks for telling me your gender.

+ man
% are you a man or a woman
- <set gender=man> Thanks for telling me your gender, dude.

+ *
% what are you doing
- It sounds like a lot of fun. <set does=<person>>

+ *
% tell me one of your favorite possessions
- You must be very fond of it. <set has=<person>>

+ *
% what is your current status
- Updating your status to "<set status=<star>><get status>".

