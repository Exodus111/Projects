// Converted using aiml2rs on: Tue Jan 27 18:52:00 2015
! version = 2.0

+ aimlequal * equal *
- {@learnequal <star>}{@<star> testequal <star2>}

+ successor 0
- 1

+ successor 1
- 2

+ successor 2
- 3

+ successor 3
- 4

+ successor 4
- 5

+ successor 5
- 6

+ successor 6
- 7

+ successor 7
- 8

+ successor 8
- 9

+ successor 9
- 1 0

+ successor * 9
- {@successor <star>} 0

+ successor * *
- <star> {@successor <star2>}

+ successor * 9 9
- {@successor <star>} 0 0

+ successor * * *
- <star> {@successor <star2> <star3>}

+ successor * 9 9 9
- {@successor <star>} 0 0 0

+ successor * * * *
- <star> {@successor <star2> <star3> <star4>}

+ successor *
- 0

+ successor
- 0

+ successor * * * * *
- 0

+ add 0 plus *
- <star>

+ add 1 plus *
@ successor <star>

+ add * plus *
- {@ADD 1 PLUS {@ADD {@predecessor <star>} PLUS<star2>}}

