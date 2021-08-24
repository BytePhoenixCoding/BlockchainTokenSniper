# V1.1 of BSCTokenSniper is largely untested. Please try it out and let me know if there's any issues. Thanks!

BSCTokenSniper v1.1 has been released. Not much, just a few improvements.

Improvements:

- Added 'check for test' to ignore tokens which have 'test' in their name.

- Added 'try' and 'catch' clauses for buy token and listenForTokens function to avoid exiting with error

- Added function to detect WBNB pair in either pair 1 or pair 2 (currently only detects WBNB in pair 1 which potentially ignores alot of tokens)

- Created 'SpecifiedTokenSniper' script - this allows you to snipe a specific token at launch as soon as it gains liquidity, if you know the token address. 
If you're lucky (like the refinable bot) you could make huge amounts of money.

- You can now pick what liquidity pair address you would like. It is set to WBNB by default (recommended) but you can change to anything if you wish.

New config.json entries:

- "checkForTest": choose whether "test" is in the token's name. Only enable if checkSourceCode is enabled. Recommended.

- "liquidityPairAddress": Leave it unless you want to change the liquidity pair address.




