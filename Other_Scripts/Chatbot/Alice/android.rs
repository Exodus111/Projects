// Converted using aiml2rs on: Tue Jan 27 18:51:49 2015
! version = 2.0

+ i got * cash from the * account
@ account withdrawl <star> from account <star2>

+ text * *
- I don't know who <star> is.

+ what is my bank balance
- Accessing bank info. Please stand by.

+ call 911
- Responding to 911 with your location.<oob><dial>911</dial></oob>

+ call 411
- Calling directory assistance with your location: <get location>.<oob><dial>411</dial></oob>

+ say *
- "<star>"

+ initialize
- Setting predicate defaults. {@set predicates}

+ set predicate
@ initialize

+ reset
@ initialize

+ start
@ initialize

+ start over
@ initialize

+ restart
@ initialize

+ oob dial contact *
- <oob><dialcontact><star></dialcontact></oob>

+ oob dial number *
- <oob><dialcontact><star></dialcontact></oob>

+ oob get contact index *
- <oob>get contact index <star></oob>

+ contactindex *
- Unknown

+ text * i *
- Sending "I <star2>" to <star>.

+ phone number for *
@ lookup phonenumber <star>

+ lookup phonenumber *
* <get numberfound> == true => The phone number is <get phonenumber>
- I can't find the number you are looking for.</li>

+ starbucks
- Searching for Starbucks near you.<oob><map>Starbucks</map></oob>

+ directions to *
- <oob><map><star></map></oob>I am displaying the directions from <get location> to <star>.

+ set predicates *
- The meta Predicate is set.

+ set predicates
@ set predicates <get meta>

+ call mom
* <get branch> == undefined => Who is your mother?
* <get branch> == undefined => Who is your mother?
- <set callstate=true><set callee={@propername mom}><set branch=<get mother>>{@call <get mother>}</li>

+ call *
- <set callstate=true><set callee=<star>>I don't know who <person><star> is.

+ propername mom
- <eval><star></eval></learn>Your mom is called <set mother=<star>><get mother>.<set alicetopic=<star>>

+ propername mom
- <eval><star></eval></learn>Your mom is called <set mother=<star>><get mother>.<set alicetopic=<star>>

+ propername ma
@ propername mom

+ propername mommy
@ propername mom

+ propername mommy
@ propername mom

+ propername *
- <star>

+ propername my *
- <star>

+ phone
- Activating phone dialer.

+ mail
- Activating your email client.

+ send mail
- Activating your email client.

+ contact *
- Do you want to call or text?

+ tell * 
@ text <star>

+ ask * 
@ text <star>

+ reply to * 
@ text <star>

+ reply to * by saying *
@ text <star> <star2>

+ where is the nearest *
@ googlemap <star>

+ look for *
@ xfind <star>

+ look up *
@ xfind <star>

+ email * i *
- Sending email to <star> form <get name>: "I <star2>".

+ xfind *
-  {random}Let me think about it.|Have you tried a web search?|I haven't heard of <person> .|There might be more than one.|I need time to formulate the reply.|I would look into the web for that knowledge.|Does it have anything to do with <get topic> ?|Interesting question.|That's a good question.|That's not something I get asked all the time.|I don't know anything about <set it=<person>><get it> .|Are you testing me?|I will search for it.|I will try to find out.|I can ask someone about it.|I would do a search for it.|Would you like to know more?|Have you tried searching the web?|Do a web search for it.|Try searching the web.|I have never been asked that before.|I think you already know the answer.|Searching...Searching...Please stand by.|Have you tried a web search?|I haven't heard of <person> .|I would look into the web for that knowledge.|Does it have anything to do with <get topic>?|Interesting question.|That's a good question.|Would you like to know more?|What is your purpose in asking?|I have never been asked that before.{/random} <set alicetopic=<person>>}{@xsearch <star>}

+ xsearch *
- <oob><search><star></search></oob>

+ where is *
@ googlemap <star>

+ googlemap *
- {random}|I'm looking on the map.|Let me try to find it for you.|I think I can find it.|Is this what you are looking for?|I think I know where <person> is.{/random}<oob><map><star></map></oob>

+ birthplace *
@ my birthplace is <star>

+ my birthplace *
@ my birthplace is <star>

+ my last name is
@ my lastname

+ i develop *
@ my job is developing <star>

+ i put * on *
- So <person><star2> has <star> on it?<set alicetopic=<person><star2>>

+ i have a * at * o clock
- {@SCHEDULE EVENT A <star> YEAR {@year} MONTH {@month} DAY {@day} HOUR <star2> MINUTE 00 AMPM PM TIMEZONE {@my timezone}}

+ my timezone
- <get timezone>

+ schedule event * year * month * day * hour * minute * ampm * timezone *
- Adding an event to your calendar: <star> on<star3><star4><star2>at<star5>:<star6>in<star7>.

+ timezone
- <get timezone>

+ how much money do i *
- Unable to access your account at this time.

+ what is call mom
@ what is callmom

+ what is callmom
- CallMom is {random}|a virtual assistant for your phone|a an intelligent robot assistant|your favorite App|a voice activated device manager{/random}{random}|created by Pandorabots.|using Pandorabots.|built for you by Pandorabots.{/random}

+ make a list
- Ok what do you want to add to the list?<set mylist=NIL>

+ read my list
@ readlist <get mylist>

+ readlist nil
- Done.

+ readlist cons * cons *
- <star>, \n{@readlist cons <star2>}

+ readlist cons * nil
- <star>.

+ readlist *
- Oddly formatted list: <star>

+ add * to my list
- Ok I am updating your list with <star>. <set mylist=CONS <star> <get mylist>>

+ put * on my list
@ add <star> to my list

+ add * to the list
@ add <star> to my list

+ * on my list
@ add <star> to my list

+ * to my list
@ add <star> to my list

+ add * my list
@ add <star> to my list

+ oob get predicates
@ get predicates

+ set predicates om
- <set age=how many><set birthday=unknown><set birthplace=unknown><set boyfriend=unknown><set brother=unknown><set cat=unknown><set daughter=unknown><set destination=unknown><set does=unknown><set dog=unknown><set eindex=1A><set email=unknown><set etype=Unknown><set father=Unknown><set favoritecolor=unknown><set favoritemovie=unknown><set friend=unknown><set fullname=unknown><set gender=he><set girlfriend=unknown><set has=unknown><set he=he><set heard=where><set hehas=a head><set helikes=himself><set her=her><set him=him><set husband=Unknown><set is=a client><set it=it><set job=your job><set lastname=unknown><set like=to chat><set location=where><set looklike=a person><set memory=nothing><set meta=set><set middlename=unknown><set mother=Unknown><set name={formal}judge{/formal}><set nickname=unknown><set password=unknown><set personality=average><set phone=unknown><set she=she><set shehas=a head><set shelikes=herself><set sign=your starsign><set sister=unknown><set son=unknown><set spouse=unknown><set status=Talking to <bot name>.><set them=them><set there=there><set they=they><set thought=nothing><set want=to talk to me><set we=we><set wife=Unknown><set phonenumber=Unknown><set numberfound=false><set contactindex=Unknown><set callstate=false><set callee=Unknown>

+ get predicates
- age is <get age>.\nbirthday is <get birthday>.\nbirthplace is <get birthplace>.\nboyfriend is<get boyfriend>.\nbrother is <get brother>.\ncat is <get cat>.\ndaughter is <get daughter>.\ndestination is <get destination>.\ndoes is <get does>.\ndog is <get dog>.\neindex is <get eindex>.\nemail is <get email>.\netype is <get etype>.\nfather is <get father>.\nfavoritecolor is <get favoritecolor>.\nfavoritemovie is <get favoritemovie>.\nfriend is <get friend>.\nfullname is <get fullname>.\ngender is <get gender>.\ngirlfriend is <get girlfriend>.\nhas is <get has>.\nhe is <get he>.\nheard is <get heard>.\nhehas is <get hehas>.\nhelinkes is <get helikes>.\nher is <get her>.\nhim is <get him>.\nhusband is <get husband>.\nis is <get is>.\nit is <get it>.\njob is <get job>.\nlastname is <get lastname>.\nlike is <get like>.\nlocation is <get location>.\nlooklike is <get looklike>.\nmemory is <get memory>.\nmeta is <get meta>.\nmiddlename is <get middlename>.\nmother is <get mother>.\nname is <get name>.\nnickname is <get nickname>.\npassword is <get password>.\npersonality is <get personality>.\nphone is <get phone>.\nshe is <get she>.\nshehas is <get hehas>.\nshelinkes is <get helikes>.\nsign is <get sign>.\nsister is <get sister>.\nson is <get son>.\nspouse is <get spouse>.\nstatus is <get status>.\nthem is <get them>.\nthere is <get there>.\nthey is <get they>.\nthought is <get thought>.\nwant is <get want>.\nwe is <get we>.\nwife is <get wife>.\nphonenumber is <get phonenumber>.\nnumberfound is <get numberfound>.\ncontactindex <get contactindex>.\ncallstate is <get callstate>.\ncallee is <get callee>.\n

+ test predicates
- age: {@my age}\nbirthday: {@my birthday}\nbirthplace: {@my birthplace}\nboyfriend is{@my boyfriend}\nbrother: {@my brother}\ncat: {@my cat}\ndaughter: {@my daughter}\ndestination: {@my destination}\ndoes: {@my does}\ndog: {@my dog}\neindex: {@my eindex}\nemail: {@my email}\netype: {@my etype}\nfather: {@my father}\nfavoritecolor: {@my favoritecolor}\nfavoritemovie: {@my favoritemovie}\nfriend: {@my friend}\nfullname: {@my fullname}\ngender: {@my gender}\ngirlfriend: {@my girlfriend}\nhas: {@my has}\nhe: {@my he}\nheard: {@my heard}\nhehas: {@he has}\nhelinkes: {@he likes}\nher: {@my her}\nhim: {@my him}\nhusband: {@my husband}\nis: {@my is}\nit: {@my it}\njob: {@my job}\nlastname: {@my lastname}\nlike: {@my like}\nlocation: {@my location}\nlooklike: {@my looklike}\nmemory: {@my memory}\nmeta: {@my meta}\nmiddlename: {@my middlename}\nmother: {@my mother}\nname: {@my name}\nnickname: {@my nickname}\npassword: {@my password}\npersonality: {@my personality}\nphone: {@my phone}\nshe: {@my she}\nsign: {@my sign}\nsister: {@my sister}\nson: {@my son}\nspouse: {@my spouse}\nstatus: {@my status}\nthem: {@my them}\nthere: {@my there}\nthey: {@my they}\nthought: {@my thought}\nwant: {@my want}\nwe: {@my we}\nwife: {@my wife}\nphonenumber: {@my phonenumber}\nnumberfound: {@my numberfound}\ncontactindex {@my contactindex}\ncallstate: {@my callstate}\ncallee: {@my callee}\n

+ text my son *
* <get branch> == undefined => Who is your son?
* <get branch> == undefined => Who is your son?
- <set branch=<get son>>{@text <get son> <star>}</li>

+ call my son
* <get branch> == undefined => Who is your son?
* <get branch> == undefined => Who is your son?
- <set branch=<get son>>{@call <get son>}</li>

+ *
% who is your son
@ my son is <star>

+ text my sister *
* <get branch> == undefined => Who is your sister?
* <get branch> == undefined => Who is your sister?
- <set branch=<get sister>>{@text <get sister> <star>}</li>

+ call my sister
* <get branch> == undefined => Who is your sister?
* <get branch> == undefined => Who is your sister?
- <set branch=<get sister>>{@call <get sister>}</li>

+ *
% who is your sister
@ my sister is <star>

+ text my brother *
* <get branch> == undefined => Who is your brother?
* <get branch> == undefined => Who is your brother?
- <set branch=<get brother>>{@text <get brother> <star>}</li>

+ call my brother
* <get branch> == undefined => Who is your brother?
* <get branch> == undefined => Who is your brother?
- <set branch=<get brother>>{@call <get brother>}</li>

+ *
% who is your brother
@ my brother is <star>

+ text my husband *
* <get branch> == undefined => Who is your husband?
* <get branch> == undefined => Who is your husband?
- <set branch=<get husband>>{@text <get husband> <star>}</li>

+ call my husband
* <get branch> == undefined => Who is your husband?
* <get branch> == undefined => Who is your husband?
- <set branch=<get husband>>{@call <get husband>}</li>

+ *
% who is your husband
@ my husband is <star>

+ text my boyfriend *
* <get branch> == undefined => Who is your boyfriend?
* <get branch> == undefined => Who is your boyfriend?
- <set branch=<get boyfriend>>{@text <get boyfriend> <star>}</li>

+ call my boyfriend
* <get branch> == undefined => Who is your boyfriend?
* <get branch> == undefined => Who is your boyfriend?
- <set branch=<get boyfriend>>{@call <get boyfriend>}</li>

+ *
% who is your boyfriend
@ my boyfriend is <star>

+ text my girlfriend *
* <get branch> == undefined => Who is your girlfriend?
* <get branch> == undefined => Who is your girlfriend?
- <set branch=<get girlfriend>>{@text <get girlfriend> <star>}</li>

+ call my girlfriend
* <get branch> == undefined => Who is your girlfriend?
* <get branch> == undefined => Who is your girlfriend?
- <set branch=<get girlfriend>>{@call <get girlfriend>}</li>

+ *
% who is your girlfriend
@ my girlfriend is <star>

+ text my daughter *
* <get branch> == undefined => Who is your daughter?
* <get branch> == undefined => Who is your daughter?
- <set branch=<get daughter>>{@text <get daughter> <star>}</li>

+ call my daughter
* <get branch> == undefined => Who is your daughter?
* <get branch> == undefined => Who is your daughter?
- <set branch=<get daughter>>{@call <get daughter>}</li>

+ *
% who is your daughter
@ my daughter is <star>

