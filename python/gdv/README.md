# GDV

## Requirements

* [Python 2.7][python_2_7]
* [Python Construct >= 2.8][python_construct]

## gdv_parser.py

Extract audio and video from **G**remlin **D**igital **V**ideo file format.

| Decoder        | Status |
|----------------|--------|
| 0              | TODO   |
| 1              | TODO   |
| 3              | TODO   |
| 6              | TODO   |
| 8              | DONE   |

### Usage

    usage: gdv_parser.py [-h] [-o output_file] [-d] [-i] [-a] [-f] [-p] gdv_file

    gdv extract launch options

    positional arguments:
    gdv_file        gdv file to extract

    optional arguments:
    -h, --help      show this help message and exit
    -o output_file  Output WAV file
    -d              Enable debugging output
    -i              Print file information
    -a              Extract audio
    -f              Extract frames
    -p              Prefix PNG frame name

#### Extract audio

    gdv_parser.py -a -o out.wav HAWK02B.GDV

#### Extract all frames

All frames will be extracted one by one to `DUMP_FRAME_<FILENAME>_XXXX.PNG`

    gdv_parser.py -f HAWK02B.GDV

## Files

| Filename       | MD5                              | SIZE ID | NB FRAMES | FRAMERATE | PLAYBACK FREQUENCY | FRAME SIZE | WIDTH | HEIGHT |
| -------------- | -------------------------------- | ------- | --------- | --------- | ------------------ | ---------- | ----- | ------ |
| ABADON1A.GDV   | 875aaa7bfca53c1446112cf7fd01017c | 0       | 240       | 12        | 22050              | 25190      | 320   | 280    |
| ABADON1B.GDV   | d24c1f5b27801235bd8728d709f23770 | 0       | 132       | 12        | 21168              | 20194      | 320   | 280    |
| ABADON1C.GDV   | 4e35006def9dd053738cc13acb15cbad | 0       | 199       | 12        | 22050              | 20326      | 320   | 280    |
| ABADON1D.GDV   | 8a35c55c5da228c35512bd2882c978b7 | 0       | 130       | 12        | 22050              | 20870      | 320   | 280    |
| ABADON1E.GDV   | 45722eddec4f3ffadd054ae6dd5b5524 | 0       | 139       | 12        | 22050              | 20788      | 320   | 280    |
| ABADON1F.GDV   | 9a3aca815015424e8022eaa50d570bde | 0       | 460       | 12        | 21168              | 20501      | 320   | 280    |
| ABADON1G.GDV   | 31b2dd2b8f1e0fe464030a236f0735e4 | 0       | 354       | 12        | 21168              | 25326      | 320   | 280    |
| ABADON1H.GDV   | cc65983ce4aed5792ea74ad547cf9ceb | 0       | 198       | 12        | 21168              | 19590      | 320   | 280    |
| ABADON2A.GDV   | bd1e376c103475f3e683661490108050 | 0       | 498       | 12        | 21200              | 18938      | 320   | 280    |
| ABADON2B.GDV   | d2e1c549251414133bdcd18df854e88e | 0       | 151       | 12        | 21200              | 18636      | 320   | 280    |
| ABADON2C.GDV   | 7a60e9442ba746c3fd772feb104e3ff9 | 0       | 175       | 12        | 21200              | 24967      | 320   | 280    |
| ABADON2D.GDV   | de254f0e379d99a057ab910d3dcb9bc9 | 0       | 237       | 12        | 21200              | 24785      | 320   | 280    |
| ABADON2E.GDV   | 74f92a8243a75804452e7afef15d7730 | 0       | 319       | 12        | 21200              | 18548      | 320   | 280    |
| ABADON2F.GDV   | 5e9ffb2563e37dedc35fa2600c88e71d | 0       | 338       | 12        | 21200              | 24764      | 320   | 280    |
| ABADON2G.GDV   | 5e603755d9db2d39a7c3cc5cc3e53540 | 0       | 352       | 12        | 21200              | 26112      | 320   | 280    |
| ABADON2H.GDV   | 50bfe19b3362260dd3c0190d132a662c | 0       | 123       | 12        | 21200              | 25274      | 320   | 280    |
| ABADON2I.GDV   | 03eaa41aea9234e8c2de7888b9718cdd | 0       | 530       | 12        | 21200              | 25310      | 320   | 280    |
| ALEF01.GDV     | 729724083ca9bae214d28d01edefa284 | 0       | 2115      | 12        | 22050              | 19009      | 320   | 280    |
| ALEF02.GDV     | eae5f4e10eb155294db5a90d09c49d07 | 0       | 1216      | 12        | 22050              | 19014      | 320   | 280    |
| ALEF03A.GDV    | 9fcb12f156e3cccdd54612c057676b4e | 0       | 238       | 12        | 21400              | 19008      | 320   | 280    |
| ALEF03B.GDV    | 91fa9e052f3bc0e3e80bb582ab810089 | 0       | 525       | 12        | 22050              | 26156      | 320   | 280    |
| ALEF03C.GDV    | c05cd355a5cc736d36121029ce85de35 | 0       | 667       | 12        | 22050              | 21369      | 320   | 280    |
| ALEF03D.GDV    | 3bda98527ce8113bc46a903a1affaead | 0       | 424       | 12        | 21168              | 26310      | 320   | 280    |
| ALEF04.GDV     | a125c262df84409987274fe4b882bf30 | 0       | 2037      | 12        | 21200              | 19013      | 320   | 280    |
| BEAST.GDV      | 390864b0022375df3d6ec81a16731049 | 0       | 735       | 12        | 21200              | 18607      | 320   | 280    |
| BELEXTRA.GDV   | 8a046f2013373be648e53138e72286ad | 0       | 85        | 12        | 21168              | 3446       | 320   | 280    |
| BELIAL1A.GDV   | db3d0dbc8770be4f3213081395282bf4 | 0       | 1210      | 12        | 21168              | 19008      | 320   | 280    |
| BELIAL1B.GDV   | bddf517a87f1cd5fdf776124cc90acc8 | 0       | 125       | 12        | 21168              | 19007      | 320   | 280    |
| BELIAL1C.GDV   | db7ce3020cafc379556e36d11b8a1775 | 0       | 103       | 12        | 21168              | 19008      | 320   | 280    |
| BELIAL1E.GDV   | d82c7f65e5383fbbca666f979bc4d183 | 0       | 403       | 12        | 21300              | 26392      | 320   | 280    |
| BELIAL1F.GDV   | 249554085619cbc8caf17e4fddf64ede | 0       | 547       | 12        | 21168              | 31407      | 320   | 280    |
| BELSB1.GDV     | 3816707c1621a31e01b8799852d344c9 | 0       | 916       | 12        | 21168              | 18619      | 320   | 280    |
| BELSB3.GDV     | 908429e6eea3090c0e8c1fa4b7bd4a29 | 0       | 354       | 12        | 21168              | 23444      | 320   | 280    |
| BELSB4.GDV     | f2614e7ec40d93bd7a456da09a08f10b | 0       | 868       | 12        | 21168              | 29355      | 320   | 280    |
| BELSB5.GDV     | 4bedf46a3fbf079f8bb71423edfafeb8 | 0       | 1197      | 12        | 21168              | 19007      | 320   | 280    |
| BELSB6.GDV     | 787d823d73b2f1d072a98bb24ec7f89f | 0       | 467       | 12        | 21200              | 19014      | 320   | 280    |
| BENDGMA.GDV    | a3f224130d8c919f877ff60c6d0a270f | 0       | 285       | 12        | 21168              | 19011      | 320   | 280    |
| BENDGMB.GDV    | 6f866fe69757f75b190ad9ee04bca2bf | 0       | 1060      | 12        | 21200              | 27838      | 320   | 280    |
| BETRAYAL.GDV   | 5f64ddeee7ef7057335cb9073831bd44 | 0       | 1710      | 12        | 21168              | 19013      | 320   | 280    |
| BRANDED.GDV    | a9004e3528ad00db36f51dc9f1570660 | 0       | 1405      | 12        | 22050              | 19016      | 320   | 280    |
| CHPTR1.GDV     | 672fc19a89bbd5744eea21865f57a34e | 0       | 85        | 12        | 21168              | 4292       | 320   | 280    |
| CHPTR10.GDV    | 9254fe881894fa75d6c8ffd4bc244896 | 0       | 85        | 12        | 21168              | 5336       | 320   | 280    |
| CHPTR11.GDV    | d293040aa7a0439ab6788d39631c7aaa | 0       | 85        | 12        | 21168              | 5482       | 320   | 280    |
| CHPTR12.GDV    | 7196f8f2c2b9f7baea7b01cd6064cbfc | 0       | 85        | 12        | 21168              | 5644       | 320   | 280    |
| CHPTR13.GDV    | f922d21ddd11d1e351b631baf165f7ac | 0       | 85        | 12        | 21168              | 6570       | 320   | 280    |
| CHPTR14.GDV    | cb03ee1d5ab644e4cf45aaba9f3aa10e | 0       | 85        | 12        | 21168              | 6134       | 320   | 280    |
| CHPTR15.GDV    | 232e05a22c14db00f22033d86d00bc10 | 0       | 85        | 12        | 21168              | 6136       | 320   | 280    |
| CHPTR16.GDV    | 1014b61d1a6d60db4f2f1ac11c42a3a3 | 0       | 85        | 12        | 21168              | 5366       | 320   | 280    |
| CHPTR17.GDV    | d925b78468ae9264855cf68b6db0c059 | 0       | 85        | 12        | 21168              | 6113       | 320   | 280    |
| CHPTR18.GDV    | 74028b3914f45a39e116395c569dede2 | 0       | 85        | 12        | 21168              | 5876       | 320   | 280    |
| CHPTR19.GDV    | 55c3341995cb250f9530faafdb28e11d | 0       | 85        | 12        | 21168              | 6033       | 320   | 280    |
| CHPTR2.GDV     | 52eb2f44469827cddf284a31acf104c1 | 0       | 85        | 12        | 21168              | 5576       | 320   | 280    |
| CHPTR20.GDV    | 1c1579b0948a9d847ccfea3b1c376031 | 0       | 85        | 12        | 21168              | 7190       | 320   | 280    |
| CHPTR3.GDV     | 0c23ac243547d857f4bb419e34873091 | 0       | 85        | 12        | 21168              | 5448       | 320   | 280    |
| CHPTR4.GDV     | 242874dc909a0d77e77220dbec218b14 | 0       | 85        | 12        | 21168              | 5972       | 320   | 280    |
| CHPTR5.GDV     | 3c29e96f7aa0866b65c0084838eeb2b0 | 0       | 85        | 12        | 21168              | 5101       | 320   | 280    |
| CHPTR6.GDV     | cbf82a83bfdc9c087c70fc1c0d6a555b | 0       | 85        | 12        | 21168              | 5434       | 320   | 280    |
| CHPTR7.GDV     | 6861827ea71b552a03b524238c34bdb2 | 0       | 85        | 12        | 21168              | 5925       | 320   | 280    |
| CHPTR8.GDV     | 16622a8c4f47a145767c20c513560db9 | 0       | 85        | 12        | 21168              | 6757       | 320   | 280    |
| CHPTR9.GDV     | e37cfe2dbd52934852abc774d16ff53c | 0       | 85        | 12        | 21168              | 6454       | 320   | 280    |
| DODGERA.GDV    | e3aa122d551b18cb2c5b9d1765ff8e8a | 0       | 556       | 12        | 21168              | 22470      | 320   | 280    |
| DOPPLE.GDV     | 9e19bbdb187cf61b9148175ebf05788c | 0       | 513       | 12        | 21168              | 19010      | 320   | 280    |
| ECREDITS.GDV   | 66df7243cc5994df451ae189b515ac8a | 0       | 1286      | 12        | 22050              | 16383      | 320   | 280    |
| EFFIGYA1.GDV   | 1567dc85751a5f18bc20638643862964 | 0       | 537       | 12        | 22150              | 18640      | 320   | 280    |
| EFFIGYA2.GDV   | 0edd09e532b5cce6c34af4152bef43f0 | 0       | 383       | 12        | 22050              | 25457      | 320   | 280    |
| EFFIGYA3.GDV   | 846d3c69025027ffd0f486df94c376bf | 0       | 80        | 12        | 22050              | 24931      | 320   | 280    |
| EFFIGYB.GDV    | 475b7568d9fd044d1fd7c9406bab47ff | 0       | 323       | 12        | 22050              | 32178      | 320   | 280    |
| EFFIGYC.GDV    | a663e9ad15aa68fa3926b8d2ab5d3df7 | 0       | 238       | 12        | 22050              | 31290      | 320   | 280    |
| ENCHANT.GDV    | 40994a4dc49624e3f2b1b4cd78becf42 | 0       | 855       | 12        | 21168              | 19011      | 320   | 280    |
| EPILOGUE.GDV   | 48d6b7436da7a9979516f8609b0fa26f | 0       | 1101      | 12        | 21168              | 19012      | 320   | 280    |
| FALSHIRE.GDV   | 04bcafafa36f3c90496b4dab0ed823c3 | 0       | 1662      | 12        | 22050              | 19018      | 320   | 280    |
| FLOTRAP1.GDV   | 9ea90ea37a012e7e8de4e0a50692275c | 0       | 465       | 12        | 22050              | 17511      | 320   | 280    |
| FLOTRAP2.GDV   | e76071aeae4ce6484a6b683e892095fb | 0       | 224       | 12        | 22050              | 18926      | 320   | 280    |
| FLOTRAP3.GDV   | 7c8a56fe81199eed0aa6ed52593916f2 | 0       | 183       | 12        | 22050              | 27034      | 320   | 280    |
| FLOTRAP4.GDV   | 7e9a893debd3a7384e819f4b0423f969 | 0       | 282       | 12        | 22050              | 22847      | 320   | 280    |
| FLOTRAP5.GDV   | dc4f8d9fde0c3465074e8056e34ec50a | 0       | 184       | 12        | 22050              | 27362      | 320   | 280    |
| FLOTRAP6.GDV   | aa9c4a86a478c7ca4b7e0be8d33746c2 | 0       | 835       | 12        | 22050              | 21888      | 320   | 280    |
| FULLKEEP.GDV   | 00a9a18389dd1eb9ded3bcf82df86899 | 0       | 5988      | 12        | 21168              | 19016      | 320   | 280    |
| GARDENS.GDV    | 4c3c82dd8002932c098bd505427bb005 | 0       | 818       | 12        | 21168              | 19006      | 320   | 280    |
| GATE01A.GDV    | 84a4f0c4cf9a9e7859362ade746625ae | 0       | 400       | 12        | 22050              | 18425      | 320   | 280    |
| GATE01B.GDV    | 1612aed2e6be65225223ffa60b95608a | 0       | 400       | 12        | 22050              | 18391      | 320   | 280    |
| GAUL01.GDV     | bbd391860f071617c9c70300576d182b | 0       | 998       | 12        | 21168              | 19012      | 320   | 280    |
| GAUL02.GDV     | 89450060c4866c779d1ac9b647847a44 | 0       | 729       | 12        | 22050              | 19007      | 320   | 280    |
| GLASSWIN.GDV   | 1bb9b8c4ef95e67162c38c6f74f90cb7 | 0       | 1028      | 12        | 21200              | 19015      | 320   | 280    |
| GNARLA.GDV     | 28cadf8aaa893304dad49a8556f90024 | 0       | 1981      | 12        | 22050              | 19009      | 320   | 280    |
| GNARLB.GDV     | 4525f188f5825977ca4a19b0b9e641c6 | 0       | 206       | 12        | 22050              | 21144      | 320   | 280    |
| GNARLC.GDV     | a67dd5242a85958b6f9344d5e8d74ead | 0       | 182       | 12        | 22050              | 21057      | 320   | 280    |
| GNARLD.GDV     | b92d5d141bb634bddd1fcdf81ba06d6c | 0       | 176       | 12        | 22050              | 21080      | 320   | 280    |
| GNARLE.GDV     | eaa0bdddbaf52934d90a370a1be4fb26 | 0       | 77        | 12        | 21100              | 21214      | 320   | 280    |
| GNARLF.GDV     | f3131702247865c34b82506c61e6d377 | 0       | 155       | 12        | 22050              | 21552      | 320   | 280    |
| GNARLG.GDV     | 5647a8f75b68007145ad35e8ef1d2019 | 0       | 169       | 12        | 22050              | 19004      | 320   | 280    |
| GNARLH.GDV     | bdb97568b914f5b82fcb0a158cca2b3c | 0       | 340       | 12        | 22050              | 27831      | 320   | 280    |
| GNARLI.GDV     | 315ccd97bc69364edd17c344b3776dd2 | 0       | 144       | 12        | 22050              | 28172      | 320   | 280    |
| GREMLOGO.GDV   | 15ccc918aaedb72e5a4cd7f1efdf8ca5 | 0       | 170       | 12        | 21168              | 18717      | 320   | 280    |
| HAWK01.GDV     | 645dcda9b38bce2f9917c2bf63916b63 | 0       | 1368      | 12        | 21168              | 19006      | 320   | 280    |
| HAWK02A.GDV    | 6cc31e20b51ac233064544fd3db34b31 | 0       | 514       | 12        | 21168              | 17850      | 320   | 280    |
| HAWK02B.GDV    | 1e66a0bf9bd33f79d8ed2c744b2ffbb8 | 0       | 78        | 12        | 21168              | 26596      | 320   | 280    |
| HAWK02C.GDV    | 26df75c923098b55eda03e1556543388 | 0       | 150       | 12        | 21168              | 28248      | 320   | 280    |
| HAWK02D.GDV    | 4091ac3ebe3dee9498376d3349f581fb | 0       | 496       | 12        | 21168              | 27794      | 320   | 280    |
| HAWK03A.GDV    | 4f433f7304adca05ac564f19c4293b3a | 0       | 1657      | 12        | 21168              | 52587      | 320   | 280    |
| HAWK03B.GDV    | 2452b0e4043fd712ac827954f0ec7e0b | 0       | 738       | 12        | 21200              | 19366      | 320   | 280    |
| HAWK03C.GDV    | 7b2333f700d757d16f58cd0736862f8b | 0       | 538       | 12        | 21200              | 19460      | 320   | 280    |
| HAWK03D.GDV    | ba87faa563c90e5dc9b77730d38ba225 | 0       | 328       | 12        | 21200              | 19097      | 320   | 280    |
| HAWK03E.GDV    | 52bc6c585c0211aa8fa94fdbf3be79b3 | 0       | 605       | 12        | 21168              | 19495      | 320   | 280    |
| HAWK03F.GDV    | 654bd4bd8fc5657276871204843d0b22 | 0       | 615       | 12        | 21168              | 19403      | 320   | 280    |
| HAWK03G.GDV    | 28e4c8f5a76308fffd96b311e9214539 | 0       | 294       | 12        | 21168              | 20834      | 320   | 280    |
| HAWK03H.GDV    | 9e0614ea2951b149f8c6419e587deeb7 | 0       | 259       | 12        | 21168              | 19904      | 320   | 280    |
| HAWK03I.GDV    | 112acd6ae8830f11226db0c00af7c197 | 0       | 235       | 12        | 21168              | 20044      | 320   | 280    |
| HAWK03J.GDV    | cbee5641d2426396de93769861e19ca3 | 0       | 290       | 12        | 21168              | 19882      | 320   | 280    |
| HAWK03K.GDV    | 578d5b518654a635f6f711f8fc87ed32 | 0       | 319       | 12        | 21168              | 21117      | 320   | 280    |
| HAWK03L.GDV    | da5c030029fda7d7e87d0c902144b5ed | 0       | 134       | 12        | 21168              | 21230      | 320   | 280    |
| HAWK03M.GDV    | 9fc354ce13ab27db6b8cf489bddfab41 | 0       | 426       | 12        | 21168              | 20930      | 320   | 280    |
| HAWK03N.GDV    | 7514b8a54219630abbe0afdf2b2a313c | 0       | 511       | 12        | 21168              | 21012      | 320   | 280    |
| HAWK03O.GDV    | 1858fce83c84c906395edb621a60c434 | 0       | 271       | 12        | 21168              | 25578      | 320   | 280    |
| HAWK03P.GDV    | 541a57fde1579bab2b1db81e0c2b634f | 0       | 1725      | 12        | 21168              | 27790      | 320   | 280    |
| HAWK04.GDV     | 1bec787204a3097d99354cdb779af824 | 0       | 1428      | 12        | 21168              | 19010      | 320   | 280    |
| INSTRA.GDV     | e91cad809509993f47f4fed50a9b4b11 | 0       | 199       | 12        | 21168              | 19008      | 320   | 280    |
| INSTRB.GDV     | b1690d999853bf4bfad0f02dcf7864f1 | 0       | 160       | 12        | 21168              | 28908      | 320   | 280    |
| INSTRC.GDV     | dea9065398ac8479e14cc35ca54dae39 | 0       | 251       | 12        | 21168              | 29641      | 320   | 280    |
| INSTRD.GDV     | c1b34a5f117e84ab36cb242b3007a495 | 0       | 145       | 12        | 21168              | 28729      | 320   | 280    |
| INSTRE.GDV     | 9a3c607cb7c15b53aa63c7eda0f8aca1 | 0       | 135       | 12        | 21200              | 29197      | 320   | 280    |
| INSTRF.GDV     | 111100aa7cdf3aac593154da8c8b9a64 | 0       | 231       | 12        | 21200              | 27411      | 320   | 280    |
| INSTRG.GDV     | 460953cf67c706bbe918b62409e550d6 | 0       | 197       | 12        | 21200              | 28586      | 320   | 280    |
| INSTRH.GDV     | 1fdbbb019c774521bd14da0b75ec1307 | 0       | 299       | 12        | 21200              | 19572      | 320   | 280    |
| INSTRI.GDV     | ad03008cf6748f79b6bb45137e2946df | 0       | 268       | 12        | 21200              | 27272      | 320   | 280    |
| INTRO.GDV      | a83311895526e0ec1a4e829f424936ca | 0       | 6096      | 12        | 21100              | 29012      | 320   | 280    |
| MOVIE.GDV      | 4bc7be9c6d275ad853b2c134f633bfa1 | 0       | 4446      | 12        | 21168              | 53860      | 320   | 400    |
| RANDALL.GDV    | 02d9067ac806695c9505534d4cb88fac | 0       | 2914      | 12        | 21200              | 19004      | 320   | 280    |
| RAPHAEL.GDV    | 8840e6eb2fd07870efc46ad408e84198 | 0       | 2570      | 12        | 21168              | 19013      | 320   | 280    |
| RAPHAELH.GDV   | c117cf84221096ce2b5db3519ba1add3 | 0       | 246       | 12        | 21168              | 27729      | 320   | 280    |
| RAPHAELI.GDV   | f2073bc3b53810670d1cbdc6ecf9c5a1 | 0       | 524       | 12        | 22050              | 19011      | 320   | 280    |
| RAPHAELJ.GDV   | 8a9ab31edb96c1dc339142402d54b3a8 | 0       | 250       | 12        | 22050              | 17693      | 320   | 280    |
| RAPHAELK.GDV   | d0facd591f5021f2c7e9f685982f8468 | 0       | 149       | 12        | 22050              | 18610      | 320   | 280    |
| RAPHAELL.GDV   | 9512ed59729f2a0d5a7c4ef57df6c0e8 | 0       | 108       | 12        | 22050              | 28740      | 320   | 280    |
| RAPHAELM.GDV   | 361297e2cc7819611d2cef8f49fb9121 | 0       | 289       | 12        | 22050              | 28958      | 320   | 280    |
| RAPHAELN.GDV   | 3006311f3f46151e7d904884b3ca1b50 | 0       | 139       | 12        | 22050              | 28721      | 320   | 280    |
| RAPHAELO.GDV   | caae9f764110d77b77a389e55e2123f2 | 0       | 307       | 12        | 22050              | 28286      | 320   | 280    |
| RATPFA.GDV     | 3599f60e941faeb9c65c8ac5bb734322 | 0       | 951       | 12        | 21168              | 21375      | 320   | 280    |
| RATPFB.GDV     | 5462b0c55fae0de44ea22c9983cfc7d8 | 0       | 368       | 12        | 21168              | 19004      | 320   | 280    |
| RAYSEL1A.GDV   | dd7e93e0514d2de40ff9a5f4db477bd5 | 0       | 409       | 12        | 21168              | 19008      | 320   | 280    |
| RAYSEL1B.GDV   | b8061c6fc3c2fcf21ab5bf47f83a5cd7 | 0       | 238       | 12        | 21168              | 25591      | 320   | 280    |
| RAYSEL1C.GDV   | 00228ab5978641363e75958cf99329ef | 0       | 302       | 12        | 21168              | 25686      | 320   | 280    |
| RAYSEL1D.GDV   | 9a13da8f6f15335fe55ae01365ea52ed | 0       | 229       | 12        | 21168              | 25580      | 320   | 280    |
| RAYSEL1E.GDV   | 7fe81f2406b0182718138b2354114d49 | 0       | 451       | 12        | 21168              | 23307      | 320   | 280    |
| RAYSEL1F.GDV   | 0869018790a2c760abf6c9ac188cecb6 | 0       | 63        | 12        | 21168              | 24538      | 320   | 280    |
| RAYSEL1G.GDV   | 66257a4898e6874f26fa42749d21dedf | 0       | 238       | 12        | 21200              | 25816      | 320   | 280    |
| REBECCA.GDV    | 2d1be567fad8344117a78774a0ea9991 | 0       | 2068      | 12        | 22050              | 19017      | 320   | 280    |
| REFLECTA.GDV   | 2ce5af633a46e594764ecbe81ef58548 | 0       | 194       | 12        | 21300              | 19005      | 320   | 280    |
| REFLECTB.GDV   | 42d524b5457453761e14f1b8149213eb | 0       | 151       | 12        | 21300              | 20620      | 320   | 280    |
| REFLECTC.GDV   | 6880d727dc07088be07ade81484306a7 | 0       | 1111      | 12        | 21200              | 29161      | 320   | 280    |
| RITUAL.GDV     | d109ad65f3d8949e69efb3f78631ba5d | 0       | 1082      | 12        | 21168              | 19016      | 320   | 280    |
| SHRIVEA.GDV    | 6a439308029985ff61e7a0a1c34fbb2c | 0       | 564       | 12        | 21168              | 19007      | 320   | 280    |
| SHRIVEB.GDV    | 020e664f0dba7bcab496d3a8070a4416 | 0       | 361       | 12        | 21168              | 20078      | 320   | 280    |
| SHRIVEC.GDV    | e53aa09129692f8cc9e0ca94f30d52fa | 0       | 956       | 12        | 21168              | 19007      | 320   | 280    |
| SHRIVED.GDV    | 888ab5cc02ed74434c8b33f451330339 | 0       | 178       | 12        | 21168              | 20171      | 320   | 280    |
| TALEWELA.GDV   | a31a56078c1a20ee015d654e8f37e33b | 0       | 1593      | 12        | 21168              | 18728      | 320   | 280    |
| TALEWELB.GDV   | 6ed62f75370dfe07e49e4a50d6a0b883 | 0       | 590       | 12        | 21168              | 26109      | 320   | 280    |
| TALEWELC.GDV   | d3b0ea25f9dd383dc9f4253fbc07eb09 | 0       | 393       | 12        | 21168              | 30221      | 320   | 280    |
| TUNNWARP.GDV   | 28ac2c20475d62c3c317d60feb01b426 | 0       | 88        | 12        | 22050              | 18470      | 320   | 280    |
| VERSE.GDV      | 3d799d2feedec79dda19170b980aeef4 | 0       | 390       | 12        | 21000              | 17730      | 320   | 280    |
| WALKWAY1.GDV   | 3d753d31c409e79a5488be7f7f6a4444 | 0       | 1004      | 12        | 22050              | 19006      | 320   | 280    |
| WALKWAY2.GDV   | eb32b94861dca6ecc4e19127d09cdf98 | 0       | 165       | 12        | 22050              | 21465      | 320   | 280    |
| WALKWAY3.GDV   | 2bc5b4ef929abb5007799d4d1df09f7a | 0       | 181       | 12        | 22050              | 20842      | 320   | 280    |
| WALKWY1A.GDV   | 00bfbd5caf042f1b824257e4081f03d4 | 0       | 735       | 12        | 22050              | 18327      | 320   | 280    |

[python_2_7]: http://www.python.org/getit/
[python_construct]: https://pypi.python.org/pypi/construct