// Converted using aiml2rs on: Tue Jan 27 18:52:06 2015
! version = 2.0

+ show stack
- top=" <get top> " second=" <get second> " third=" <get third> " fourth=" <get fourth> " fifth=" <get fifth> " sixth=" <get sixth> " seventh=" <get seventh> " last=" <get last> "

+ pop
@ popom <get top>

+ popom om
- <set top={@random topic} ><get top>

+ popom *
- <get top> <set top=<get second> ><set second=<get third> ><set third=<get fourth> ><set fourth=<get fifth> ><set fifth=<get sixth> ><set sixth=<get seventh> ><set seventh=<get last> ><set last={@random topic} >

+ push *
- <set last=<get seventh> ><set seventh=<get sixth> ><set sixth=<get fifth> ><set fifth=<get fourth> ><set fourth=<get third> ><set third=<get second> ><set second=<get top> ><set top=<star> ><star>

