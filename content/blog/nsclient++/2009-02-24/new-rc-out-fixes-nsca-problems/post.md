Title: New RC out! (fixes NSCA problems)
Author: mickem
Status: published

The latest RC out in a bit will fix the issues with missing encryptions
on NSCA connections. A good way to verify this is too run:

     NSClient++ /about 

Which yields the following:

     ... l NSClient++.cpp(339) * NSCAAgent (w/ encryption) (NSCAAgent.dll) l NSClient++.cpp(342) Passive check support (needs NSCA on nagios server). l NSClient++.cpp(342) Avalible crypto are: {0=No Encryption (not safe), 1=XOR (not safe), 2=DES, 3=DES-EDE3, 4=CAST-128, 6=XTEA, 8=Blowfish, 9=Twofish, 11=RC2, 14=AES, 20=Serpent, 23=GOST} ... 

where it lists available encryption algorithms. After this I shall
investigate the process check issue and after then I shall (if nothing
else pops up) release the new version. // Michael Medin
