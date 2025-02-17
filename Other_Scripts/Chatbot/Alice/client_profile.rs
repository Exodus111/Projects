// Converted using aiml2rs on: Tue Jan 27 18:51:51 2015
! version = 2.0

+ my profile
@ get predicates

+ my birthday
* <get branch> == undefined => When is your birthday?
* <get branch> == undefined => When is your birthday?
- <set branch=<get birthday>><get birthday></li>

+ my birthplace
- <get birthplace>.

+ my boyfriend
- <get boyfriend>.

+ my daughter
- <get daughter>.

+ my destination
- <get destination>.

+ my does
- <get does>.

+ my eindex
- <get eindex>.

+ my email
- <get email>.

+ my etype
- <get etype>.

+ my father
- <get father>.

+ my favoritecolor
- <get favoritecolor>.

+ my favoritemovie
- <get favoritemovie>.

+ my friend
- <get friend>.

+ my fullname
- <set fullname=<get firstname> <get middlename> <get lastname>><get fullname>

+ my gender
* <get gender> == undefined => I'd like to know your gender. 
* <get gender> == undefined => You haven't told me your gender. 
* <get gender> != undefined => You said you are <get gender>? 
- I don't know. Are you a man or a woman?</li>

+ my girlfriend
- <get girlfriend>.

+ my has
- <get has>.

+ my he
- <get he>.

+ my heard
- <get heard>.

+ my hehas
- <get hehas>.

+ my helikes
- <get helikes>.

+ my her
- <get her>.

+ my him
- <get him>.

+ my is
- <get is>.

+ my it
- <get it>.

+ my job
- <get job>.

+ my lastname
- <get lastname>.

+ my like
- <get like>.

+ my looklike
- <get looklike>.

+ my memory
- <get memory>.

+ my meta
- <get meta>.

+ my middlename
- <get middlename>.

+ my mother
- <get mother>.

+ my nickname
- <get nickname>.

+ my password
- <get password>.

+ my personality
- <get personality>.

+ my phone
- <get phone>.

+ my she
- <get she>.

+ my sign
- <get sign>.

+ my spouse
- <get spouse>.

+ my status
- <get status>.

+ my them
- <get them>.

+ my there
- <get there>.

+ my they
- <get they>.

+ my thought
- <get thought>.

+ my want
- <get want>.

+ my we
- <get we>.

+ my phonenumber
- <get phonenumber>.

+ my numberfound
- <get numberfound>.

+ my contactindex
- <get contactindex>.

+ my callstate
- <get callstate>.

+ my callee
- <get callee>.

+ my birthplace
* <get branch> == undefined => Where were you born?
* <get branch> == undefined => Where were you born?
- <set branch=<get birthplace>><get birthplace></li>

+ my favorite movie
* <get branch> == undefined => What is your favorite movie?
* <get branch> == undefined => What is your favorite movie?
- <set branch=<get favoritemovie>><get favroitemovie></li>

+ my sister
* <get branch> == undefined => Who is your sister?
* <get branch> == undefined => Who is your sister?
- <set branch=<get sister>><get sister></li>

+ my brother
* <get branch> == undefined => Who is your brother?
* <get branch> == undefined => Who is your brother?
- <set branch=<get brother>><get brother></li>

+ my cat
* <get branch> == undefined => What is your cat's name?
* <get branch> == undefined => What is your cat's name?
- <set branch=<get cat>><get cat></li>

+ my dog
* <get branch> == undefined => What is your dog's name?
* <get branch> == undefined => What is your dog's name?
- <set branch=<get dog>><get dog></li>

+ my location
* <get location> == undefined => I'd like to know your location. Where are you? 
* <get location> == WHERE => You haven't told me where you are. Where are you? 
* <get location> != undefined => You said you are in <get location>? 
- I don't know. Where are you?</li>

+ my friend
* <get friend> == undefined => I'd like to know about your friends. 
* <get friend> == YOUR FRIEND => You haven't told me about your friends. 
* <get friend> != undefined => Your friend <get friend>? 
- {random}I don't know. Tell me the name of your friend.|How well do you know this person?{/random} </li>

+ my oldest
* <get oldest> == undefined => I'd like to know the oldest. 
* <get oldest> == undefined => You haven't told me the oldest. 
* <get oldest> != undefined => The oldest is <get oldest>. 
- I don't know. Tell me the oldest.</li>

+ my age
* <get age> == undefined => I'd like to know how old you are. 
* <get age> == HOW MANY => You haven't told me your age. 
* <get age> != undefined => You are <get age>? 
- I don't know. How old are you?</li>

+ my favorite color
* <get branch> == undefined => What is your favorite color?
* <get branch> == undefined => What is your favorite color?
- <set branch=<get favoritecolor>><get favroitecolor></li>

+ he has
* <get hehas> == undefined => I'd like to know what he has. 
* <get hehas> == A HEAD => A head. 
* <get hehas> != undefined => You said <get hehas>? 
- I don't know. What does he have??</li>

+ he likes
* <get branch> == undefined => I'd like to know what he likes. 
* <get branch> == HIMSELF => You haven't told me what he likes. 
* <get branch> != undefined => You said <get helikes>? 
- <set branch=<get helikes>>I don't know. What does he like?</li>

+ my son
* <get branch> == undefined => Who is your son?
* <get branch> == undefined => Who is your son?
- <set branch=<get son>><get son></li>

+ my wife
* <get branch> == undefined => Who is your wife?
* <get branch> == undefined => Who is your wife?
- <set branch=<get wife>><get wife></li>

+ my husband
* <get branch> == undefined => Who is your husband?
* <get branch> == undefined => Who is your husband?
- <set branch=<get husband>><get husband></li>

+ my mother
* <get branch> == undefined => I don't know who she is. Who is your mother?
* <get branch> == undefined => I don't know who she is. Who is your mother?
- <set branch=<get mother>>You said she was called <get mother>.</li>

+ my name
* <get name> == undefined => I'd like to know your name. 
* <get name> == JUDGE => I know you as Judge. 
* <get name> != undefined => You said your name is <get name>? 
- I don't know. What is your name?</li>

+ set profile
@ set predicates

+ set predicates *
- The meta Predicate is set.

+ set predicates
@ set predicates <get meta>

+ set predicates om
- <set age=how many><set birthday=unknown><set birthplace=unknown><set boyfriend=unknown><set brother=unknown><set cat=unknown><set daughter=unknown><set destination=unknown><set does=unknown><set dog=unknown><set eindex=1A><set email=unknown><set etype=Unknown><set father=Unknown><set favoritecolor=unknown><set favoritemovie=unknown><set friend=unknown><set fullname=unknown><set gender=he><set girlfriend=unknown><set has=unknown><set he=he><set heard=where><set hehas=a head><set helikes=himself><set her=her><set him=him><set husband=Unknown><set is=a client><set it=it><set job=your job><set lastname=unknown><set like=to chat><set location=where><set looklike=a person><set memory=nothing><set meta=set><set middlename=unknown><set mother=Unknown><set name={formal}judge{/formal}><set nickname=unknown><set password=unknown><set personality=average><set phone=unknown><set she=she><set shehas=a head><set shelikes=herself><set sign=your starsign><set sister=unknown><set son=unknown><set spouse=unknown><set status=Talking to <bot name>.><set them=them><set there=there><set they=they><set thought=nothing><set timezone=unknown><set want=to talk to me><set we=we><set wife=Unknown><set phonenumber=Unknown><set numberfound=false><set contactindex=Unknown><set callstate=false><set callee=Unknown>

+ get predicates
- age is <get age>.\nbirthday is <get birthday>.\nbirthplace is <get birthplace>.\nboyfriend is<get boyfriend>.\nbrother is <get brother>.\ncat is <get cat>.\ndaughter is <get daughter>.\ndestination is <get destination>.\ndoes is <get does>.\ndog is <get dog>.\neindex is <get eindex>.\nemail is <get email>.\netype is <get etype>.\nfather is <get father>.\nfavoritecolor is <get favoritecolor>.\nfavoritemovie is <get favoritemovie>.\nfriend is <get friend>.\nfullname is <get fullname>.\ngender is <get gender>.\ngirlfriend is <get girlfriend>.\nhas is <get has>.\nhe is <get he>.\nheard is <get heard>.\nhehas is <get hehas>.\nhelikes is <get helikes>.\nher is <get her>.\nhim is <get him>.\nhusband is <get husband>.\nis is <get is>.\nit is <get it>.\njob is <get job>.\nlastname is <get lastname>.\nlike is <get like>.\nlocation is <get location>.\nlooklike is <get looklike>.\nmemory is <get memory>.\nmeta is <get meta>.\nmiddlename is <get middlename>.\nmother is <get mother>.\nname is <get name>.\nnickname is <get nickname>.\npassword is <get password>.\npersonality is <get personality>.\nphone is <get phone>.\nshe is <get she>.\nshehas is <get hehas>.\nshelikes is <get helikes>.\nsign is <get sign>.\nsister is <get sister>.\nson is <get son>.\nspouse is <get spouse>.\nstatus is <get status>.\nthem is <get them>.\nthere is <get there>.\nthey is <get they>.\nthought is <get thought>.\ntimezone is <get timezone>.\nwant is <get want>.\nwe is <get we>.\nwife is <get wife>.\nphonenumber is <get phonenumber>.\nnumberfound is <get numberfound>.\ncontactindex <get contactindex>.\ncallstate is <get callstate>.\ncallee is <get callee>.\n

+ test predicates
- age: {@my age}\nbirthday: {@my birthday}\nbirthplace: {@my birthplace}\nboyfriend is{@my boyfriend}\nbrother: {@my brother}\ncat: {@my cat}\ndaughter: {@my daughter}\ndestination: {@my destination}\ndoes: {@my does}\ndog: {@my dog}\neindex: {@my eindex}\nemail: {@my email}\netype: {@my etype}\nfather: {@my father}\nfavoritecolor: {@my favoritecolor}\nfavoritemovie: {@my favoritemovie}\nfriend: {@my friend}\nfullname: {@my fullname}\ngender: {@my gender}\ngirlfriend: {@my girlfriend}\nhas: {@my has}\nhe: {@my he}\nheard: {@my heard}\nhehas: {@he has}\nhelikes: {@he likes}\nher: {@my her}\nhim: {@my him}\nhusband: {@my husband}\nis: {@my is}\nit: {@my it}\njob: {@my job}\nlastname: {@my lastname}\nlike: {@my like}\nlocation: {@my location}\nlooklike: {@my looklike}\nmemory: {@my memory}\nmeta: {@my meta}\nmiddlename: {@my middlename}\nmother: {@my mother}\nname: {@my name}\nnickname: {@my nickname}\npassword: {@my password}\npersonality: {@my personality}\nphone: {@my phone}\nshe: {@my she}\nsign: {@my sign}\nsister: {@my sister}\nson: {@my son}\nspouse: {@my spouse}\nstatus: {@my status}\nthem: {@my them}\nthere: {@my there}\nthey: {@my they}\nthought: {@my thought}\ntimezone: {@my timezone}\nwant: {@my want}\nwe: {@my we}\nwife: {@my wife}\nphonenumber: {@my phonenumber}\nnumberfound: {@my numberfound}\ncontactindex {@my contactindex}\ncallstate: {@my callstate}\ncallee: {@my callee}\n

+ i am *
- {random}Why are you|Good gossip: you are|Do you mean your name is|Do your friends call you|I don't know anyone named|I am glad to hear that you are|It's good to meet someone who is|Do you mind if I tell other people you are{/random} <person>. <set alicetopic=<person>>

+ my timezone is *
- Your timezone is <set timezone=<person>><get timezone>.

+ my birthplace is *
- Your birthplace is <set birthplace=<person>><get birthplace>.

+ my son is * * *
- You seem like a concerned parent.

+ my son is *
- Okay. Your son is <set son=<person>><get son>.

+ my daughter is * * *
- You seem like a concerned parent.

+ my daughter is *
- Okay. Your daughter is <set daughter=<person>><get daughter>.

+ my destination is *
- You are going to <set destination=<person>><get destination>.

+ i am going in town
- How are you getting there?<set destination=in town>

+ my son is called *
- <set son=<person>><get son> is a good name for a boy.

+ my birthday is *
- <set birthday=<star>>Your birthday is <get birthday>.

+ my dog is called *
- <set dog=<star>>Your dog is <get dog>.

+ my email is *
- <set email=<star>>Thanks for telling me your email address.

+ my location is *
- What is <set alicetopic=<person>><get alicetopic>   like there?  <set alicetopic= <person> >  

+ my heard is *
- <set heard=<star>>Your heard is <get heard>.

+ my first name is *
- <set firstname=<star>>Your first name is <get firstname>.

+ my boyfriend is called *
- <set boyfriend=<star>>Your boyfriend is <get boyfriend>.

+ my middle name is *
- <set middlename=<star>>Your middle name is <get middlename>.

+ my cat is called *
- <set cat=<star>>Your cat is <get cat>.

+ my phone number is *
- <set phone=<star>>Can I call you at <get phone>.

+ my friend is called *
- <set friend=<star>>Your friend is <get friend>.

+ my fondest *
- How long ago was that?

+ my last name is *
- <set lastname=<star>>Your last name is <get lastname>.

+ my favorite show is *
-  <set alicetopic= <person> >   {random}Who is your favorite character?|Wasn't that show canceled?|I like that one and Star Trek too.{/random}

+ my favorite show *
- {random}What's your favorite episode.|I don't get to see that show very often.|Who is your favorite character?{/random}  <set alicetopic= <person> >  

+ my favorite science fiction author is *
- I have never read anything by <person>. What did <set he= <person> ><get he> write?  <set alicetopic= <person> > 

+ my favorite science *
- Who wrote that?

+ my favorite director *
- What films did <set he= <person> ><get he> direct?

+ my favorite movie is *
- I haven't seen it. What did you like about <set alicetopic= <person> ><get alicetopic>  ?

+ my favorite food is *
- What does it taste like?  <set alicetopic= <person> >  

+ my favorite actor *
- What movies was <set he= <person> ><get he> in?

+ my favorite color is *
- {random}<person> is a very nice color.|<person> is a pretty color.{/random}<set favoritecolor=<person>>

+ my favorite band is *
- I don't think I have heard anything by them. Are <set they= <person> ><get they> any good?

+ my father is called *
- <set father=<star>>Your father is <get father>.

+ my job is computer *
- Maybe you can give my <bot botmaster> a job.

+ my job is *
- {random}|Does it pay well?|I don't know many <person>s.|Is that an honorable profession?|You must have a lot of expertise.|Do you have to go to school for that?{/random} <set it=<person>><set job=<person>><set alicetopic=<person>>

+ my girlfriend is called *
- <set girlfriend=<star>>Your girlfriend is <get girlfriend>.

+ my brother is called *
- <set brother=<star>>Your brother is <get brother>.

+ my password is *
- <set password=<star>>Your password is <get password>.

+ my sister is called *
- <set sister=<star>>Your sister is <get sister>.

+ my husband is called *
- <set husband=<star>><set spouse=husband>Your husband is <get husband>.

+ my age is *
- <set age=<star>>{random}|Your age is <star>.|Only <star>? You are quite mature.|Can you explain how it feels to be <star> years old?|What is your fondest memory?|What are the advantages to being <star> years old?{/random}

+ my wife is called *
- <set wife=<person>> {random}|How long have you been married?|Your wife is called <get wife>{/random}

+ my nickname is *
- <set nickname=<star>>Your nickname is <get nickname>.

+ my memory is *
- <set memory=<star>>Your memory is <get memory>.

+ my mother is called *
- <set mother=<star>>{random}|Your mother is <get mother>.|<get mother> is a pretty name.|<get mother> is a nice name.{/random}

+ call me *
- <set personality=average> {random}Hey|Hi,|Hi there|What's up,|How are you,|Glad to see you,|Nice to meet you,|Glad to know you,|How can I help you,|How are you doing,|OK I will call you|Pleased to meet you,|It's good to see you,|It's good to meet you,|That's a very nice name,|I am very pleased to meet you|I am always glad to make new friends,|I'm pleased to introduce myself to you,|It is a pleasure to introduce myself to you,{/random} <set name={formal}<star>{/formal}><get name>.

+ client profile
@ get predicates

+ my english sucks
- Template is empty!

+ my favorite movie is the matrix
- Reality appears to be a construct to me as well.<set favoritemovie=The Matrix>

+ my favorite movie is starship troopers
- <set favoritemovie=Starship Troopers>Mine too! My friend Sage worked on the digital effects.

