# Missing Ticker Coverage Analysis

This document lists all tickers with missing data periods for each data source, grouped by the reason for absence. Generated from `plots.coverage_over_time` output.

> **Status definitions**
> - **missing** — data was expected for the period but is absent in the source feed
> - **not downloaded** *(EODHD only)* — data was never fetched from the API; the ticker was outside the subscription plan, used an unsupported share class/exchange, or was skipped by the downloader

---

## Yahoo Finance

### 1. Company Acquired / Merged — Ticker Retired

The company was bought out, merged, or taken private. The ticker ceased trading at or near the end of the missing period.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| AABA | 1999-12-08 → 2017-06-16 | Yahoo Inc. original ticker; renamed after core business sold to Verizon, remainder became Altaba |
| AAL | 1996-01-02 → 1997-01-13 | American Airlines predecessor; reorganised under AMR Corp |
| AAMRQ | 1996-01-02 → 2003-03-10 | AMR Corp; filed for bankruptcy 2011, predecessor OTC ticker |
| ABI | 1996-01-02 → 2008-11-20 | Anheuser-Busch; acquired by InBev to form AB InBev |
| ABMD | 2018-05-31 → 2022-12-19 | Abiomed; acquired by Johnson & Johnson |
| ACS | 2004-04-02 → 2010-02-02 | Affiliated Computer Services; acquired by Xerox |
| ADT | 2012-10-02 → 2016-04-28 | ADT Inc.; spun off from Tyco International, then taken private by Apollo Global |
| AET | 1996-01-02 → 2018-11-28 | Aetna; acquired by CVS Health |
| AGN | 1996-01-02 → 2020-04-06 | Allergan; acquired by AbbVie |
| AKS | 2008-07-01 → 2011-12-14 | AK Steel; distress-related gap; later merged with Cleveland-Cliffs |
| ALTR | 2000-04-18 → 2015-12-21 | Altera; acquired by Intel |
| ALXN | 2012-05-25 → 2021-06-04 | Alexion Pharmaceuticals; acquired by AstraZeneca |
| ANDV | 2007-09-27 → 2018-09-24 | Andeavor (formerly Tesoro); acquired by Marathon Petroleum |
| ANTM | 2002-07-25 → 2022-06-21 | Anthem; renamed Elevance Health, ticker changed to ELV |
| APC | 1997-07-28 → 2019-08-08 | Anadarko Petroleum; acquired by Occidental Petroleum |
| ARG | 2009-09-09 → 2016-05-20 | Airgas; acquired by Air Liquide |
| ARNC | 1996-01-02 → 2020-04-03 | Arconic; split off from Alcoa in 2016, then taken private by Apollo |
| AT | 1996-01-02 → 2007-11-16 | Alltel; acquired by Verizon |
| ATVI | 2015-08-31 → 2023-10-02 | Activision Blizzard; acquired by Microsoft |
| AW | 1999-08-02 → 2008-12-04 | Allied Waste Industries; acquired by Republic Services |
| AYE | 2000-12-11 → 2011-02-23 | Allegheny Energy; merged into FirstEnergy |
| BAY | 1996-02-12 → 1998-08-28 | Bayer AG US ADR; coverage gap in early ADR listing period |
| BCR | 1996-01-02 → 2017-12-27 | C.R. Bard; acquired by Becton Dickinson |
| BDK | 1996-01-02 → 2010-03-11 | Black & Decker; merged with Stanley Works to form Stanley Black & Decker |
| BEAM | 1996-01-02 → 2014-04-22 | Beam Inc.; acquired by Suntory Holdings |
| BGEN | 2000-01-31 → 2003-11-12 | Biogen predecessor ticker; renamed Biogen Idec after Idec merger |
| BHGE | 1996-01-02 → 2019-10-03 | Baker Hughes, a GE company; merged entity later renamed Baker Hughes (BKR) |
| BJS | 2002-05-15 → 2010-04-21 | BJ Services; acquired by Baker Hughes |
| BLL | 1996-01-02 → 2022-04-11 | Ball Corporation; extended early-period data gap in Yahoo |
| BLS | 1996-01-02 → 2006-12-29 | BellSouth; acquired by AT&T |
| BMC | 1998-10-01 → 2012-06-15 | BMC Software; taken private by Bain Capital et al. |
| BMET | 1996-01-02 → 2007-07-10 | Biomet; taken private by consortium |
| BMS | 1996-01-02 → 2014-12-04 | Bemis Company; acquired by Amcor |
| BNI | 1996-01-02 → 2010-02-10 | Burlington Northern Santa Fe; acquired by Berkshire Hathaway |
| BRCM | 2000-07-03 → 2016-01-26 | Broadcom (original); acquired by Avago Technologies, which then took the Broadcom name |
| BSC | 1998-07-01 → 2008-05-29 | Bear Stearns; acquired by JPMorgan Chase during the 2008 financial crisis |
| BUD | 1996-01-02 → 2008-11-17 | Anheuser-Busch; acquired by InBev |
| BXLT | 2015-07-01 → 2016-06-01 | Baxalta; spun from Baxter, then acquired by Shire |
| CA | 1996-01-02 → 2018-10-31 | CA Technologies; acquired by Broadcom |
| CAM | 2008-01-29 → 2016-03-31 | Cameron International; acquired by Schlumberger |
| CBS | 1996-01-02 → 2019-11-21 | CBS Corporation; merged with Viacom to form ViacomCBS |
| CCE | 1998-10-08 → 2016-05-24 | Coca-Cola Enterprises; sold North American operations back to Coca-Cola |
| CEG | 1996-01-02 → 2012-03-02 | Constellation Energy; acquired by Exelon |
| CELG | 2006-11-06 → 2019-11-05 | Celgene; acquired by Bristol-Myers Squibb |
| CEPH | 2008-11-17 → 2011-10-11 | Cephalon; acquired by Teva Pharmaceuticals |
| CERN | 2010-04-30 → 2022-05-10 | Cerner; acquired by Oracle |
| CHIR | 2000-11-24 → 2006-04-19 | Chiron; acquired by Novartis |
| COG | 2008-06-23 → 2021-09-20 | Cabot Oil & Gas; merged with Cimarex Energy to form Coterra Energy |
| CPQ | 1996-01-02 → 2002-05-01 | Compaq; acquired by HP |
| CTX | 1996-01-02 → 2009-08-18 | Centex; acquired by PulteGroup |
| CTXS | 1999-12-01 → 2022-09-19 | Citrix Systems; taken private by Vista Equity and Elliott |
| DEC | 1996-01-02 → 1998-06-08 | Digital Equipment Corporation; acquired by Compaq |
| DELL | 1996-09-06 → 2013-10-18 | Dell; taken private by Michael Dell and Silver Lake |
| DFS | 2007-07-02 → 2025-03-24 | Discover Financial Services; acquired by Capital One |
| DISH | 2017-03-13 → 2023-06-07 | Dish Network; merged with DirecTV |
| DJ | 1996-01-02 → 2007-12-12 | Dow Jones & Company; acquired by News Corp |
| DNB | 2008-12-02 → 2017-04-04 | Dun & Bradstreet; taken private, later relisted |
| DOW | 1996-01-02 → 2017-08-31 | Dow Chemical; merged with DuPont to form DowDuPont |
| DPHIQ | 1999-05-28 → 2005-10-10 | Delphi; spun off from GM, filed for bankruptcy 2005 |
| DRE | 2017-07-26 → 2022-09-19 | Duke Realty; acquired by Prologis |
| DTV | 2006-12-04 → 2015-07-23 | DirecTV; acquired by AT&T |
| DWDP | 2017-09-01 → 2019-06-01 | DowDuPont; existed only as merged entity, then split into three companies |
| DYN | 2000-10-03 → 2009-12-17 | Dynegy; restructured and later filed for bankruptcy |
| EC | 1996-01-02 → 2006-06-05 | Engelhard; acquired by BASF |
| EDS | 1998-08-11 → 2008-08-25 | Electronic Data Systems; acquired by HP |
| EMC | 1996-03-28 → 2016-09-06 | EMC Corporation; acquired by Dell |
| EOP | 2001-10-10 → 2007-02-09 | Equity Office Properties; acquired by Blackstone Group |
| ESRX | 2003-09-26 → 2018-12-19 | Express Scripts; acquired by Cigna |
| FDC | 1996-01-02 → 2007-09-24 | First Data; taken private by KKR |
| FDO | 2001-08-06 → 2015-07-06 | Family Dollar; acquired by Dollar Tree |
| FLIR | 2009-01-02 → 2021-04-20 | FLIR Systems; acquired by Teledyne Technologies |
| FOX / FOXA | 2004-12-20 → 2019-02-27 | 21st Century Fox; acquired by Walt Disney Company |
| FRC | 2019-01-02 → 2023-03-20 | First Republic Bank; failed and acquired by JPMorgan Chase |
| FRX | 2000-11-22 → 2014-06-24 | Forest Laboratories; acquired by Actavis |
| FTR | 2001-02-27 → 2017-03-17 | Frontier Communications; partial gap; company later filed for bankruptcy |
| G | 1996-01-02 → 2005-09-28 | Gillette; acquired by Procter & Gamble |
| GENZ | 2001-12-14 → 2008-01-23 | Genzyme; acquired by Sanofi |
| GGP | 2007-07-02 → 2008-11-12 & 2013-12-10 → 2018-08-20 | General Growth Properties; filed bankruptcy 2009, emerged, then acquired by Brookfield |
| GMCR | 2014-03-24 → 2016-02-26 | Green Mountain Coffee Roasters; acquired by JAB Holding |
| GP | 1996-01-02 → 2005-12-16 | Georgia-Pacific; taken private by Koch Industries |
| GTW | 1998-04-27 → 2006-07-31 | Gateway; acquired by Acer |
| HET | 1996-01-02 → 2008-01-24 | Harrah's Entertainment; taken private, later renamed Caesars Entertainment |
| HLT | 1996-01-02 → 2007-10-24 | Hilton Hotels; taken private by Blackstone |
| HNZ | 1996-01-02 → 2013-06-06 | H.J. Heinz; taken private by Berkshire Hathaway and 3G Capital |
| HOT | 2000-11-17 → 2016-08-12 | Starwood Hotels; acquired by Marriott International |
| IGT | 2001-09-04 → 2014-06-19 | International Game Technology; acquired by GTECH |
| INFO | 2017-06-02 → 2022-02-17 | IHS Markit; acquired by S&P Global |
| JAVA | 1996-01-02 → 2010-01-21 | Sun Microsystems; acquired by Oracle |
| JCP | 1996-01-02 → 2013-11-27 | J.C. Penney; later also filed for bankruptcy |
| JEC | 2007-10-26 → 2019-12-09 | Jacobs Engineering; spun off government services segment (Leidos predecessor) |
| JNPR | 2006-06-02 → 2025-05-19 | Juniper Networks; acquired by Hewlett Packard Enterprise |
| KORS | 2013-11-13 → 2018-09-18 | Michael Kors; renamed Capri Holdings |
| KRFT | 2012-10-02 → 2015-07-02 | Kraft Foods Group; merged with H.J. Heinz to form Kraft Heinz |
| LEHMQ | 1998-01-12 → 2008-09-16 | Lehman Brothers; filed for bankruptcy September 2008, largest US bankruptcy ever |
| LIFE | 2008-11-24 → 2014-01-22 | Life Technologies; acquired by Thermo Fisher Scientific |
| LLL | 2004-12-01 → 2019-06-07 | L3 Technologies; merged with Harris Corporation to form L3Harris |
| LLTC | 2000-04-03 → 2017-03-10 | Linear Technology; acquired by Analog Devices |
| LO | 2008-06-11 → 2015-06-11 | Lorillard; acquired by Reynolds American |
| LSI | 1996-01-02 → 2014-05-06 | LSI Corporation; acquired by Avago Technologies |
| LU | 1996-10-01 → 2006-11-22 | Lucent Technologies; merged with Alcatel to form Alcatel-Lucent |
| LVLT | 2014-11-05 → 2017-10-10 | Level 3 Communications; acquired by CenturyLink |
| MAY | 1996-01-02 → 2005-08-22 | May Department Stores; acquired by Federated Department Stores |
| MEDI | 2000-06-16 → 2007-05-31 | MedImmune; acquired by AstraZeneca |
| MER | 1996-01-02 → 2008-12-29 | Merrill Lynch; acquired by Bank of America during the 2008 financial crisis |
| MERQ | 2000-06-29 → 2006-01-03 | Mercury Interactive; acquired by HP |
| MFE | 2008-12-23 → 2011-02-28 | McAfee; acquired by Intel |
| MHS | 2003-08-20 → 2012-03-22 | Medco Health Solutions; acquired by Express Scripts |
| MIL | 1996-01-02 → 2010-07-12 | Millipore; acquired by Merck KGaA |
| MJN | 2009-12-21 → 2017-06-07 | Mead Johnson Nutrition; acquired by Reckitt Benckiser |
| MMI | 2011-01-04 → 2012-05-15 | Motorola Mobility; acquired by Google |
| MON | 2002-08-14 → 2018-06-06 | Monsanto; acquired by Bayer |
| MYL | 2004-04-23 → 2020-10-12 | Mylan; merged with Upjohn division of Pfizer to form Viatris |
| NCC | 1996-01-02 → 2008-12-29 | National City Corp; acquired by PNC Financial Services |
| NLSN | 2013-07-09 → 2022-10-03 | Nielsen Holdings; taken private by consortium |
| NOVL | 1996-01-02 → 2011-04-25 | Novell; acquired by Attachmate |
| NSM | 1996-01-02 → 2011-09-21 | National Semiconductor; acquired by Texas Instruments |
| NXTL | 1998-04-01 → 2005-08-12 | Nextel Communications; merged with Sprint |
| NYX | 2007-10-25 → 2013-11-07 | NYSE Euronext; acquired by Intercontinental Exchange (ICE) |
| OMX | 1996-01-02 → 2008-06-18 | OfficeMax; merged with Office Depot |
| ONE | 1996-01-02 → 2004-06-28 | Bank One; acquired by JPMorgan Chase |
| PARA | 2022-02-17 → 2025-07-23 | Paramount Global (renamed from ViacomCBS); acquired by Skydance Media |
| PBCT | 2008-11-13 → 2022-03-02 | People's United Financial; acquired by M&T Bank |
| PCP | 2007-06-01 → 2016-01-26 | Precision Castparts; acquired by Berkshire Hathaway |
| PCL | 2002-01-17 → 2016-02-16 | Plum Creek Timber; acquired by Weyerhaeuser |
| PETM | 2012-10-05 → 2015-03-11 | PetSmart; taken private by BC Partners |
| PGN | 1996-01-02 → 2012-06-29 | Progress Energy; acquired by Duke Energy |
| PKI | 1996-01-02 → 2023-05-04 | PerkinElmer; renamed Revvity |
| PLL | 1996-01-02 → 2015-08-25 | Pall Corporation; acquired by Danaher |
| POM | 2007-11-09 → 2016-03-18 | Pepco Holdings; acquired by Exelon |
| PSFT | 1998-10-02 → 2004-12-27 | PeopleSoft; acquired by Oracle |
| PX | 1996-01-02 → 2018-10-25 | Praxair; merged with Linde to form Linde plc |
| PXD | 2008-09-24 → 2024-04-03 | Pioneer Natural Resources; acquired by ExxonMobil |
| Q | 2000-07-06 → 2011-03-23 | Qwest Communications; acquired by CenturyLink |
| RAI | 2002-09-04 → 2017-07-20 | Reynolds American; acquired by British American Tobacco |
| RHT | 2009-07-27 → 2019-07-01 | Red Hat; acquired by IBM |
| ROH | 1996-01-02 → 2009-04-01 | Rohm and Haas; acquired by Dow Chemical |
| RTN | 1996-01-02 → 2020-04-03 | Raytheon; merged with United Technologies to form RTX Corporation |
| S | 1996-01-02 → 2013-07-02 | Sprint Nextel; later acquired by T-Mobile |
| SBNY | 2021-12-20 → 2023-01-04 | Signature Bank; failed, placed in FDIC receivership March 2023 |
| SCG | 2009-01-02 → 2018-12-24 | SCANA Corporation; acquired by Dominion Energy |
| SEBL | 2000-05-05 → 2006-01-30 | Siebel Systems; acquired by Oracle |
| SGP | 1996-01-02 → 2009-10-29 | Schering-Plough; acquired by Merck |
| SIAL | 1996-01-02 → 2015-11-17 | Sigma-Aldrich; acquired by Merck KGaA |
| SIVB | 2018-03-19 → 2023-01-04 | Silicon Valley Bank; failed, placed in FDIC receivership March 2023 |
| SNDK | 2006-04-20 → 2016-05-11 | SanDisk; acquired by Western Digital |
| SNI | 2008-07-01 → 2018-02-28 | Scripps Networks Interactive; acquired by Discovery |
| SPLS | 1998-10-07 → 2017-09-12 | Staples; taken private by Sycamore Partners |
| STI | 1996-01-02 → 2019-12-05 | SunTrust Banks; merged with BB&T to form Truist Financial |
| STJ | 1996-01-02 → 2017-01-03 | St. Jude Medical; acquired by Abbott Laboratories |
| SUN | 1996-01-02 → 2012-09-13 | Sunoco; acquired by Energy Transfer |
| SVU | 1996-01-02 → 2012-04-30 | SUPERVALU; restructured, sold major assets |
| SWY | 1998-11-13 → 2015-01-15 | Safeway; acquired by Albertsons/Cerberus Capital |
| SYMC | 2003-03-31 → 2019-10-18 | Symantec; renamed NortonLifeLock |
| TEG | 2007-02-22 → 2015-06-24 | Integrys Energy; acquired by Wisconsin Energy |
| TIF | 2000-06-21 → 2020-12-21 | Tiffany & Co.; acquired by LVMH |
| TMK | 1996-01-02 → 2019-07-15 | Torchmark; renamed Globe Life |
| TOY | 1996-01-02 → 2005-07-21 | Toys"R"Us; taken private; later filed for bankruptcy |
| TRB | 1996-01-02 → 2007-12-17 | Tribune Company; taken private by Sam Zell |
| TRW | 1996-01-02 → 2002-12-09 | TRW Inc.; acquired by Northrop Grumman |
| TSG | 2000-03-16 → 2007-03-30 | Sabre Holdings; taken private by Silver Lake and TPG |
| TSS | 2008-01-02 → 2019-08-09 | Total System Services (TSYS); acquired by Global Payments |
| TWC | 2009-03-30 → 2016-05-17 | Time Warner Cable; acquired by Charter Communications |
| TWTR | 2018-06-07 → 2022-10-12 | Twitter; taken private by Elon Musk |
| TWX | 1996-01-02 → 2018-06-14 | Time Warner; acquired by AT&T |
| TXU | 1996-01-02 → 2007-10-09 | TXU Corp; taken private (Energy Future Holdings) by KKR/TPG |
| UTX | 1996-01-02 → 2020-03-03 | United Technologies; merged with Raytheon to form RTX |
| VAR | 2007-02-12 → 2021-03-22 | Varian Medical Systems; acquired by Siemens Healthineers |
| VIAB / VIAC | 2006-01-03 → 2022-02-15 | Viacom / ViacomCBS; renamed Paramount Global |
| WAMUQ | 1997-07-02 → 2008-09-26 | Washington Mutual; largest US bank failure in history, seized by FDIC September 2008 |
| WB | 1996-01-02 → 2008-12-29 | Wachovia; acquired by Wells Fargo |
| WCG | 2018-09-17 → 2019-12-23 | WellCare Health Plans; acquired by Centene |
| WFM | 2006-01-03 → 2017-08-17 | Whole Foods Market; acquired by Amazon |
| WIN | 2006-07-18 → 2015-03-31 | Windstream Holdings; later also filed for bankruptcy |
| WLP | 1999-06-09 → 2004-11-26 | WellPoint Health Networks; renamed Anthem |
| WWY | 1996-01-02 → 2008-10-06 | Wm. Wrigley Jr. Company; acquired by Mars |
| WYE | 1996-01-02 → 2009-10-15 | Wyeth; acquired by Pfizer |
| WYND | 2006-08-01 → 2018-05-24 | Wyndham Hotels predecessor; spun off and renamed |
| XEC | 2014-06-20 → 2020-01-28 | Cimarex Energy; merged with Coterra |
| XLNX | 1999-11-08 → 2022-02-02 | Xilinx; acquired by AMD |
| XTO | 2004-12-29 → 2010-06-21 | XTO Energy; acquired by ExxonMobil |

---

### 2. Bankruptcy / Delisting — Company Ceased to Trade

Companies that filed for bankruptcy or were delisted without a standard corporate acquisition. The `Q` suffix in many tickers denotes post-bankruptcy OTC trading.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| ABKFQ | 2000-12-11 → 2008-06-10 | Ambac Financial Group; filed for bankruptcy |
| ACAS | 2007-07-09 → 2009-03-02 | American Capital; severe financial distress during the 2008 crisis |
| ANRZQ | 2011-06-02 → 2012-10-01 | Anaren; bankruptcy-related OTC ticker |
| BTUUQ | 2006-11-20 → 2014-09-19 | Peabody Energy predecessor / bankruptcy OTC ticker |
| BVSN | 2000-11-06 → 2001-08-31 | BroadVision; dot-com era collapse |
| CPNLQ | 2000-12-01 → 2005-11-28 | Calpine Corporation; filed for bankruptcy 2005 |
| EKDKQ | 1996-01-02 → 2010-12-17 | Eastman Kodak; filed for bankruptcy January 2012 |
| ENRNQ | 1996-01-02 → 2001-11-26 | Enron; massive accounting fraud, largest US bankruptcy at the time |
| LEHMQ | 1998-01-12 → 2008-09-16 | Lehman Brothers; filed September 2008, largest US bankruptcy ever filed |
| MTLQQ | 1996-01-02 → 2009-05-29 | Metals USA; filed for bankruptcy |
| RSHCQ | 1996-01-02 → 2011-06-30 | RadioShack; later also filed for bankruptcy |
| SUNEQ | 2007-05-31 → 2011-12-14 | Suntech Power; OTC bankruptcy ticker |
| UAWGQ | 1996-01-02 → 2002-05-14 | UAW predecessor; bankruptcy |
| VSTNQ | 2000-06-29 → 2005-12-29 | Webvan / dot-com era bankruptcy |
| VTSS | 2000-12-12 → 2002-08-19 | Vitesse Semiconductor; dot-com era financial distress |
| WAMUQ | 1997-07-02 → 2008-09-26 | Washington Mutual; largest US bank failure in history |
| WCOEQ | 1996-04-01 → 2002-05-14 | WorldCom; massive accounting fraud and bankruptcy |
| WNDXQ | 1996-01-02 → 2004-12-02 | Winstar Communications; dot-com era bankruptcy |

---

### 3. Spin-off / Rename — Ticker Replaced by New Symbol

The company changed its ticker symbol or was spun off, creating a break in the historical series under the old symbol. The underlying entity continued trading under a new ticker.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| ADS | 2013-12-23 → 2020-05-22 | Alliance Data Systems; renamed Bread Financial |
| ANDW | 1996-01-02 → 2006-09-28 | Andrew Corporation; acquired by CommScope |
| APOL | 2002-05-15 → 2013-06-27 | Apollo Education Group; taken private |
| CDAY | 2021-09-20 → 2023-10-18 | Ceridian; renamed / rebranded to Dayforce |
| CMCSK | 2015-09-21 → 2015-12-09 | Comcast Class K shares; brief gap during share reclassification |
| COL | 2001-07-02 → 2018-08-06 (+ sparse days) | Rockwell Collins; spun off from Rockwell International, acquired by United Technologies |
| CPGX | 2015-07-02 → 2016-06-27 | CP Gypsum; brief spinoff window |
| CSRA | 2015-11-30 → 2018-04-02 | CSRA Inc.; spun off from CSC, acquired by GDIT |
| DAY | 2024-02-01 → 2026-01-14 | Dayforce (formerly Ceridian); coverage gap ongoing |
| DISCA / DISCK | 2010-03-01 → 2022-04-04 | Discovery; merged with WarnerMedia to form Warner Bros. Discovery |
| EVHC | on 2017-09-01 | Envision Healthcare; single-day gap on corporate rename |
| FBHS | 2016-06-24 → 2022-11-08 | Fortune Brands Home & Security; renamed Fortune Brands Innovations |
| FI | 2023-06-07 → 2025-11-04 | Fiserv; coverage gap post-rebranding |
| NLOK | 2019-11-05 → 2022-11-01 | NortonLifeLock; renamed Gen Digital |
| PARA | 2022-02-17 → 2025-07-23 | Paramount Global; renamed from ViacomCBS, acquired by Skydance |
| VIAC | 2019-12-05 → 2022-02-15 | ViacomCBS; renamed Paramount Global |
| VLTO | on 2023-10-02 | Veralto; single-day gap on date of spin-off from Danaher |
| WLTW | 2016-01-05 → 2021-12-20 | Willis Towers Watson; renamed WTW |
| WRK | 2015-07-02 → 2024-06-24 | WestRock; merged with Smurfit Kappa to form Smurfit WestRock |

---

### 4. Insufficient Historical Data — Yahoo Finance Coverage Limitation

Yahoo Finance does not carry price history far enough back for these tickers, or has persistent long-running gaps unrelated to a corporate event. Common causes: foreign ADR with limited US backfill, dual-class share series, or Yahoo simply never indexed this symbol historically.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| ABC | 2001-08-30 → 2023-08-25 | AmerisourceBergen; very sparse Yahoo coverage despite continuous active trading |
| AEE | 1996-01-02 → 1997-12-31 | Ameren; Yahoo data availability limited before 1998 |
| AM | 1996-01-02 → 2004-04-30 | American Greetings; limited historical backfill |
| AMH | 1996-01-02 → 1997-09-08 | American Health Holdings; limited Yahoo coverage |
| AMP | 1996-01-02 → 1999-03-30 | Ameriprise predecessor; limited early data |
| ANSS | 2017-06-19 → 2025-07-09 | Ansys; coverage gap during acquisition process by Synopsys |
| BF.B | 1996-01-02 → 2026-01-14 | Brown-Forman Class B; Yahoo Finance does not carry this dual-class share series historically |
| BLL | 1996-01-02 → 2022-04-11 | Ball Corporation; extended early-period data gap in Yahoo |
| BRK.B | 2010-02-16 → 2026-01-14 | Berkshire Hathaway Class B; persistent gaps, likely due to split-adjusted pricing complexity after 2010 50:1 split |
| BT | 1996-01-02 → 1999-06-03 | British Telecom ADR; patchy US coverage of foreign ADR in early listing period |
| CBB | 1996-01-02 → 1998-01-26 | Cincinnati Bell; limited early data |
| CMA | 1996-01-02 → 2024-05-08 | Comerica; extended Yahoo data gap |
| GPS | 1996-01-02 → 2022-01-10 | Gap Inc.; extended Yahoo data gap |
| HES | 1996-01-02 → 2025-07-18 | Hess Corporation; extended data gaps; acquired by Chevron 2024 |
| IPG | 1996-01-02 → 2025-11-11 | Interpublic Group; extended Yahoo coverage gap |
| JWN | 1996-01-02 → 2020-05-22 | Nordstrom; extended Yahoo data gap |
| K | 1996-01-02 → 2025-11-28 | Kellogg (renamed Kellanova); acquired by Mars 2024 |
| MMC | 1996-01-02 → 2025-12-22 | Marsh & McLennan; extended Yahoo coverage gap |
| MRO | 1996-01-02 → 2024-10-01 | Marathon Oil; acquired by ConocoPhillips 2024 |
| RDS.A | 1996-01-02 → 2002-07-18 | Royal Dutch Shell ADR A-shares; limited US ADR historical data |
| UN | 1996-01-02 → 2002-07-18 | Unilever NV ADR; limited historical coverage on US exchanges |
| WBA | 1996-01-02 → 2025-08-08 | Walgreens Boots Alliance; taken private by Sycamore Partners 2025 |

---

### 5. Patchy / Fragmented Data — Data Quality Issues

These tickers show many non-contiguous isolated missing days or short blocks scattered over a long period, indicating incomplete data scraping, Yahoo Finance data quality issues, or OTC-era trading irregularities — rather than a clean corporate event.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| BOL | 1996-01-02 → 2004-05-03 (dozens of isolated gaps) | Bausch & Lomb; highly fragmented early data in Yahoo Finance |
| CFC | 1997-06-18 → 2006-12-26 (dozens of isolated gaps) | Countrywide Financial; extensive patchy coverage before acquisition by Bank of America |
| CIN | on 1998-12-31 | Cincinnati Gas & Electric; single isolated missing day anomaly |
| COL | 2012-10-08 → 2018-08-06 (scattered single days) | Rockwell Collins; isolated missing trading days scattered across quarterly filings periods |
| GR | 2009-10-15 → 2011-10-10 (sporadic) | Goodrich Corporation; intermittent gaps before acquisition by United Technologies |
| MEE | 2008-07-16 → 2011-04-25 (many isolated gaps) | Massey Energy; fragmented data during distressed period preceding acquisition by Alpha Natural Resources |
| PBG | 2004-11-01 → 2008-11-11 (sporadic single days) | Pepsi Bottling Group; scattered missing days before acquisition by PepsiCo |
| RX | 1996-11-04 → 2010-02-23 (multiple disconnected blocks) | IMS Health; multiple discontinuous blocks from repeated Yahoo data gaps across the coverage period |

---
---

## EODHD

### 1. Company Acquired / Merged — Ticker Retired

The company was bought out, merged, or taken private. The ticker ceased trading at or near the end of the missing period.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| ABI | 1996-01-02 → 2008-11-20 | Anheuser-Busch; acquired by InBev |
| ADCT | 1999-08-02 → 2007-06-26 | ADC Telecommunications; acquired by Tyco Electronics |
| ADT | 2012-10-02 → 2016-04-28 | ADT Inc.; taken private by Apollo, later relisted |
| AGC | 1996-01-02 → 2001-08-20 | Agere Systems; acquired by LSI Logic |
| ALTR | 2000-04-18 → 2015-12-21 | Altera; acquired by Intel |
| AM | 1996-01-02 → 2004-04-30 | American Greetings; taken private |
| ANDW | 1996-01-02 → 1997-12-29 | Andrew Corporation; acquired by CommScope (early EODHD gap) |
| ARC | 1996-01-02 → 2000-04-10 | ARC International; acquired |
| ARNC | 1996-01-02 → 2016-10-31 | Arconic; split off from Alcoa |
| ASO | 1999-03-10 → 2006-10-31 | Academy Sports predecessor; early coverage gap |
| AT | 1996-01-02 → 2007-11-16 | Alltel; acquired by Verizon |
| AV | 2000-10-02 → 2007-10-25 | Avocent; acquired by Emerson Electric |
| BBBY | 1999-10-01 → 2002-05-29 | Bed Bath & Beyond; early data gap; company later also filed for bankruptcy |
| BEAM | 1996-01-02 → 2014-04-22 | Beam Inc.; acquired by Suntory Holdings |
| BHGE | 1996-01-02 → 2017-06-26 | Baker Hughes, a GE company; merged entity |
| BSC | 1998-07-01 → 2008-03-14 | Bear Stearns; acquired by JPMorgan Chase |
| BUD | 1996-01-02 → 2008-11-17 | Anheuser-Busch; acquired by InBev |
| CA | 1996-01-02 → 2018-10-31 | CA Technologies; acquired by Broadcom |
| CAM | 2008-01-29 → 2016-03-31 | Cameron International; acquired by Schlumberger |
| CCE | 1998-10-08 → 2003-09-08 (multiple annual blocks) | Coca-Cola Enterprises; EODHD has fragmentary annual-report-based blocks for this period |
| CE | 2001-04-02 → 2004-02-26 | Celanese; IPO / backfill gap |
| CEG | 1996-01-02 → 2012-03-02 | Constellation Energy; acquired by Exelon |
| CEN | 1996-01-02 → 2001-03-30 | Ceridian old entity; acquired |
| CF | 2000-06-19 → 2004-08-26 | CF Industries; pre-IPO / limited backfill |
| CHK | 2006-03-03 → 2015-12-31 | Chesapeake Energy; data gap; company later filed for bankruptcy |
| CHIR | 2000-11-24 → 2006-04-19 | Chiron; acquired by Novartis |
| CNC | 1997-01-15 → 2001-12-06 | Centene predecessor; restructured |
| CNXT | 2000-01-31 → 2002-06-19 | Conexant Systems; restructured |
| CPWR | 1999-01-04 → 2006-12-01 | Compuware; taken private |
| CR | 1996-01-02 → 2004-12-16 | Crane Co.; early coverage gap |
| DELL | 1996-09-06 → 2013-10-18 | Dell; taken private |
| DG | 1998-07-16 → 2007-07-06 | Dollar General; taken private, then relisted |
| DNB | 2008-12-02 → 2017-04-04 | Dun & Bradstreet; taken private, later relisted |
| DO | 2009-02-26 → 2016-09-28 | Diamond Offshore; later filed for bankruptcy |
| DOW | 1996-01-02 → 2017-08-31 | Dow Chemical; merged with DuPont |
| DTV | 2006-12-04 → 2015-07-23 | DirecTV; acquired by AT&T |
| DYN | 2000-10-03 → 2009-12-17 | Dynegy; restructured and filed for bankruptcy |
| EC | 1996-01-02 → 2006-06-05 | Engelhard; acquired by BASF |
| EMC | 1996-03-28 → 2016-09-06 | EMC Corporation; acquired by Dell |
| FB | 2013-12-23 → 2022-06-08 | Facebook; renamed Meta Platforms |
| FDC | 1996-01-02 → 2007-09-24 | First Data; taken private by KKR |
| FOX / FOXA | 2004-12-20 → 2019-02-27 | 21st Century Fox; acquired by Walt Disney |
| FRO | 1997-01-02 → 1999-09-21 | Frontline; ADR coverage gap in early listing period |
| FRX | 2000-11-22 → 2014-06-24 | Forest Laboratories; acquired by Actavis |
| G | 1996-01-02 → 2005-09-28 | Gillette; acquired by Procter & Gamble |
| GDT | 1996-12-19 → 2006-04-21 | Guidant; acquired by Boston Scientific |
| GLD | 1996-01-02 → 1997-04-29 | Glidden Co.; acquired |
| GLK | 1996-01-02 → 2004-01-28 | Great Lakes Chemical; acquired |
| GNT | 1996-03-13 → 1998-06-30 | Genentech; partial period before full acquisition by Roche |
| GP | 1996-01-02 → 2005-12-16 | Georgia-Pacific; taken private by Koch Industries |
| H | 1996-01-02 → 2007-04-05 (two blocks) | Hershey / Hyatt predecessor; restructured |
| HCA | 1996-01-02 → 2006-11-17 | Hospital Corporation of America; taken private, later relisted |
| HCP | 2008-03-31 → 2019-10-18 | HCP Inc.; renamed Healthpeak Properties (PEAK) |
| HCR | 1998-09-28 → 2007-11-05 | HCR ManorCare; taken private |
| HI | 1996-01-02 → 2003-03-28 | Household International; acquired by HSBC |
| HLT | 1996-01-02 → 2007-10-24 | Hilton Hotels; taken private by Blackstone |
| HM | 1996-01-02 → 2001-12-14 | Homestake Mining; acquired by Barrick Gold |
| HMA | 2001-11-07 → 2007-02-26 | Health Management Associates; acquired |
| HNZ | 1996-01-02 → 2003-09-08 | H.J. Heinz; taken private (shorter gap than Yahoo) |
| I | 1996-01-02 → 1996-03-29 | Inco Ltd.; acquired by Vale |
| INFO | 2017-06-02 → 2022-02-17 | IHS Markit; acquired by S&P Global |
| IR | 1996-01-02 → 2009-06-30 & 2010-11-17 → 2017-05-03 | Ingersoll Rand; spun off climate segment (Trane Technologies) |
| KG | 2000-10-03 → 2008-04-28 | King Pharmaceuticals; acquired by Pfizer |
| KMI | 2000-12-12 → 2007-05-24 | Kinder Morgan; taken private, later relisted |
| LB | 1996-01-02 → 2021-07-21 | L Brands; renamed Bath & Body Works |
| LIFE | 2008-11-24 → 2014-01-22 | Life Technologies; acquired by Thermo Fisher Scientific |
| LLL | 2004-12-01 → 2019-06-07 | L3 Technologies; merged with Harris to form L3Harris |
| LU | 1996-10-01 → 2006-11-22 | Lucent Technologies; merged with Alcatel |
| MDR | 1996-01-02 → 2003-08-18 | McDermott International; restructured |
| MEA | 1996-01-02 → 2002-01-28 | Mead Corporation; merged with Westvaco |
| MEDI | 2000-06-16 → 2007-05-31 | MedImmune; acquired by AstraZeneca |
| MI | 2002-02-11 → 2011-07-05 | Marshall & Ilsley; acquired by BMO Financial |
| MIL | 1996-01-02 → 2003-09-08 | Millipore; acquired by Merck KGaA |
| MIR | 1997-08-07 → 2003-07-16 (two blocks) | Mirant; restructured and renamed |
| MNK | 2014-08-19 → 2017-07-25 | Mallinckrodt; later filed for bankruptcy |
| MON | 2002-08-14 → 2015-12-31 | Monsanto; acquired by Bayer |
| NCC | 1996-01-02 → 2008-12-29 | National City Corp; acquired by PNC Financial |
| NSM | 1996-01-02 → 2011-09-21 | National Semiconductor; acquired by Texas Instruments |
| NYX | 2007-10-25 → 2013-11-07 (+ 2 isolated days 2010) | NYSE Euronext; acquired by ICE |
| ONE | 1996-01-02 → 2003-09-30 | Bank One; acquired by JPMorgan Chase |
| PCL | 2002-01-17 → 2016-02-16 | Plum Creek Timber; acquired by Weyerhaeuser |
| PCS | 1998-11-24 → 2004-04-19 | Sprint PCS; merged with Sprint |
| PD | 1996-01-02 → 2007-03-16 | Phelps Dodge; acquired by Freeport-McMoRan |
| PEAK | 2019-11-05 → 2024-02-01 | Healthpeak Properties; renamed from HCP |
| PGN | 1996-01-02 → 2012-06-29 | Progress Energy; acquired by Duke Energy |
| PLL | 1996-01-02 → 2015-08-25 | Pall Corporation; acquired by Danaher |
| POM | 2007-11-09 → 2016-03-18 | Pepco Holdings; acquired by Exelon |
| PSFT | 1998-10-02 → 2004-12-27 | PeopleSoft; acquired by Oracle |
| PX | 1996-01-02 → 2018-10-25 | Praxair; merged with Linde |
| Q | 2000-07-06 → 2011-03-23 | Qwest Communications; acquired by CenturyLink |
| RAL | 1996-01-02 → 2001-12-06 | Ralston Purina; acquired by Nestlé |
| S | 1996-01-02 → 2013-07-02 | Sprint; acquired by T-Mobile |
| SAF | 1996-01-02 → 2008-09-22 | Safeco; acquired by Liberty Mutual |
| SGP | 1996-01-02 → 2009-10-29 | Schering-Plough; acquired by Merck |
| SHLD | 2005-03-28 → 2012-08-23 | Sears Holdings; later filed for bankruptcy |
| SII | 2006-10-02 → 2010-02-19 | Smith International; acquired by Schlumberger |
| SNDK | 2006-04-20 → 2016-05-11 | SanDisk; acquired by Western Digital |
| SPLS | 1998-10-07 → 2017-09-12 | Staples; taken private |
| STI | 1996-01-02 → 2019-12-05 | SunTrust Banks; merged with BB&T to form Truist |
| SUN | 1996-01-02 → 2012-09-13 | Sunoco; acquired by Energy Transfer |
| SUNEQ | 2007-05-31 → 2011-12-14 | Suntech Power; bankruptcy |
| SYMC | 2003-03-31 → 2003-09-08 | Symantec; short gap around restructuring |
| TE | 2001-10-10 → 2016-06-27 | TECO Energy; acquired by Emera |
| TEK | 1996-01-02 → 2007-11-13 | Tektronix; acquired by Danaher |
| TMC | 1996-01-02 → 2000-06-09 | Times Mirror; acquired by Tribune |
| TMK | 1996-01-02 → 2003-09-08 | Torchmark; renamed Globe Life |
| TOS | 1999-09-20 → 2001-09-10 | Tosco Corporation; acquired by Phillips Petroleum |
| TRW | 1996-01-02 → 2002-12-09 | TRW Inc.; acquired by Northrop Grumman |
| TSG | 2000-03-16 → 2007-03-30 | Sabre Holdings; taken private |
| TX | 1996-01-02 → 2001-10-04 | Texaco; acquired by Chevron |
| UCL | 1996-01-02 → 2005-08-10 | Unocal; acquired by Chevron |
| UST | 1996-01-02 → 2009-01-05 | UST Inc.; acquired by Altria |
| WB | 1996-01-02 → 2008-12-29 | Wachovia; acquired by Wells Fargo |
| WLL | 1996-01-02 → 2002-02-07 | Whittman-Hart / MarchFirst; bankruptcy |
| WLP | 1999-06-09 → 2004-11-26 | WellPoint; renamed Anthem |
| WYND | 2006-08-01 → 2018-05-24 | Wyndham; spun off and renamed |
| XL | 2001-09-04 → 2015-12-31 | XL Capital; acquired by AXA |

---

### 2. Not Downloaded — EODHD API / Subscription Gap

EODHD explicitly flags these as `not downloaded`. The data was never retrieved from the API — typically because the ticker was outside the subscription plan, is a dual-class share series not supported by EODHD, is a foreign-exchange-listed ADR not in the US database, or is a post-bankruptcy OTC ticker excluded from standard coverage.

| Ticker | Not Downloaded Period | Reason |
|--------|-----------------------|--------|
| AAMRQ | 1996-01-02 → 2003-03-10 | AMR Corp bankruptcy OTC ticker; outside standard EODHD US equity coverage |
| ABKFQ | 2000-12-11 → 2008-06-10 | Ambac Financial bankruptcy OTC; outside standard coverage |
| AFS.A | 1998-04-08 → 2000-11-29 | American Fidelity dual-class share; EODHD does not support this class |
| ATGE | 2009-06-09 → 2012-09-25 | Adtalem Global Education predecessor; not fetched from API |
| AZA.A | 1996-01-02 → 2001-06-20 | Alza Corporation dual-class share; not in EODHD |
| BAY | 1996-02-12 → 1998-08-28 | Bayer AG US ADR; not downloaded in early period |
| BF.B | 1996-01-02 → 2026-01-14 | Brown-Forman Class B; EODHD does not carry this dual-class share series at all |
| BHMSQ | 1996-01-02 → 2000-12-08 | Bethlehem Steel bankruptcy OTC; outside standard coverage |
| BLY | 1996-01-02 → 1996-12-18 | Blyth Industries; very short early period not fetched |
| BRK.B | 2010-02-16 → 2026-01-14 | Berkshire Hathaway Class B; complex split-adjusted pricing post-2010 not retrieved |
| CDAY | 2021-09-20 → 2023-10-18 | Ceridian; not downloaded during rename/transition period |
| CIT.A | 2000-07-17 → 2001-05-31 | CIT Group dual-class share; not in standard EODHD coverage |
| CMB | 1996-01-02 → 1996-03-29 | Chase Manhattan Bank predecessor; very early, not fetched |
| COC.B | 1999-08-09 → 2002-08-29 | Corus Bankshares dual-class share; not downloaded |
| CYR | 1996-01-02 → 1996-03-25 | Cyrk International; not in EODHD database |
| DWD | 1996-01-02 → 1997-05-30 | Dun & Bradstreet old ticker; not fetched |
| FBO | 1996-01-02 → 1996-03-12 | FBR & Co. predecessor; very early, not downloaded |
| FTL.A | 1996-01-02 → 1999-09-30 | Fruit of the Loom dual-class share; not in EODHD |
| GFS.A | 1996-01-02 → 1998-07-13 | GlobalFoundries predecessor dual-class; not downloaded |
| GIDL | 1996-01-02 → 1997-07-09 | Obscure/defunct ticker; not in EODHD database |
| GWF | 1996-01-02 → 1997-06-26 | Golden West Financial very early period; not fetched |
| HFS | 1996-08-16 → 1997-12-12 | HFS Inc.; not downloaded from API |
| LDW.B | 1996-01-02 → 1999-12-07 | Laidlaw International dual-class B share; not in EODHD |
| LEHMQ | 1998-01-12 → 2008-09-16 | Lehman Brothers; bankruptcy OTC not in standard EODHD plan |
| LLX | 1996-01-02 → 1997-10-14 | LLX Logistics; not fetched from API |
| LOR | 1996-01-02 → 1996-04-22 | Loral Space & Communications very early period; not downloaded |
| MTLQQ | 1996-01-02 → 2009-05-29 | Metals USA bankruptcy OTC; outside EODHD standard coverage |
| NAE | 1996-01-02 → 1997-08-06 | National Western Financial; not in EODHD database |
| NLV | 1996-04-01 → 2000-01-05 | NLV Financial; not downloaded |
| NMK | 1996-01-02 → 2002-01-31 | Niagara Mohawk; not fetched — acquired by National Grid |
| NYN | 1996-01-02 → 1997-08-14 | NYNEX; not downloaded — acquired by Bell Atlantic |
| PEL | 1996-01-02 → 1997-06-18 | Pelican Financial (early period); not fetched |
| RE | 2017-06-19 → 2023-06-20 | Everest Re Group; not downloaded in this period |
| RDS.A | 1996-01-02 → 2002-07-18 | Royal Dutch Shell A-share ADR; not in standard EODHD US coverage |
| RSHCQ | 1996-01-02 → 2011-06-30 | RadioShack bankruptcy OTC; outside standard coverage |
| SHN | 1996-01-02 → 1996-12-27 | Shoney's; very early period not fetched |
| TDM | 1996-01-02 → 1997-08-26 | Tandem Computers; acquired by Compaq — not fetched |
| TMC.A | 1996-01-02 → 2000-06-09 | Times Mirror dual-class share; EODHD does not carry this class |
| UAWGQ | 1996-01-02 → 2002-05-14 | UAW predecessor bankruptcy OTC; outside EODHD |
| USH | 1996-01-02 → 1997-06-16 | USH; not downloaded |
| USHC | 1996-01-02 → 1996-07-18 | USHC; not downloaded |
| VAT | 1996-01-02 → 1996-08-28 | Vat Group (Swiss); not in EODHD US database |
| WCOEQ | 1996-04-01 → 2002-05-14 | WorldCom bankruptcy OTC; outside standard EODHD coverage |

---

### 3. Insufficient Historical Data — EODHD Coverage Start Limitation

EODHD's database for many US equities effectively begins around **1998** rather than 1996. Entries whose missing period ends on or near **1997-12-29** almost universally reflect EODHD's effective coverage start date for that security, not a corporate event. Entries with longer gaps beyond 1998 reflect either a later IPO, a spin-off, or genuinely limited EODHD backfill for that ticker.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| AAL | 1996-01-02 → 1997-01-13 | American Airlines predecessor; EODHD history starts 1997 |
| ABS | 1996-01-02 → 1997-12-29 | Albertson's; EODHD coverage starts ~1998 |
| ABX | 1996-01-02 → 2002-07-18 | Barrick Gold; limited EODHD backfill for this Canadian cross-listed ticker |
| ACKH | 1996-01-02 → 1997-12-29 | Ackerly Communications; EODHD starts ~1998 |
| ACV | 1996-01-02 → 2006-11-16 | Alberto-Culver; extended EODHD gap |
| AET | 1996-01-02 → 1997-12-29 | Aetna; EODHD coverage starts ~1998 |
| AHM | 1996-01-02 → 1997-12-29 | American Home Mortgage; EODHD starts ~1998 |
| AL | 1996-01-02 → 2002-07-18 | Alcan Aluminum; limited EODHD backfill (Canadian issuer) |
| AMH | 1996-01-02 → 1997-09-08 | American Health Holdings; EODHD starts ~1998 |
| AMP | 1996-01-02 → 1999-03-30 | Ameriprise predecessor; limited backfill |
| ANV | 1996-01-02 → 1999-04-08 | AnnVenture; EODHD backfill limitation |
| APC | 1997-07-28 → 1997-12-29 | Anadarko Petroleum; EODHD coverage starts ~1998 |
| AR | 1996-01-02 → 1999-10-26 | Antero Resources early ticker; limited backfill |
| AS | 1996-01-02 → 1998-11-23 | Armco Steel; EODHD backfill limitation |
| ASC | 1996-01-02 → 1999-06-23 | Aristar; limited data |
| AVP | 1996-01-02 → 1997-12-29 | Avon Products; EODHD starts ~1998 |
| BDK | 1996-01-02 → 1997-12-29 | Black & Decker; EODHD starts ~1998 |
| BEV | 1996-01-02 → 1997-12-02 | Beverly Enterprises; EODHD starts ~1998 |
| BFI | 1996-01-02 → 1999-07-30 | Browning-Ferris Industries; acquired by Allied Waste — limited backfill |
| BFO | 1996-01-02 → 2000-10-02 | Budget Group; limited EODHD history |
| BKB | 1996-01-02 → 1997-12-29 | BankBoston; EODHD starts ~1998 |
| BLS | 1996-01-02 → 1997-12-29 | BellSouth; EODHD starts ~1998 |
| BMET | 1996-01-02 → 1997-12-29 | Biomet; EODHD starts ~1998 |
| BMGCA | 1996-07-22 → 1997-12-29 | BMG Canada cross-listed; early EODHD gap |
| BMS | 1996-01-02 → 1997-12-29 | Bemis Company; EODHD starts ~1998 |
| BNI | 1996-01-02 → 1997-12-29 | Burlington Northern Santa Fe; EODHD starts ~1998 |
| BOL | 1996-01-02 → 1997-12-29 | Bausch & Lomb; EODHD starts ~1998 |
| BR | 1996-01-02 → 2006-03-30 | Automatic Data Processing predecessor; extended gap |
| CCTYQ | 1996-01-02 → 1997-12-29 | Century Communications; EODHD starts ~1998 |
| CGP | 1996-01-02 → 1997-12-29 | Coastal Corporation; EODHD starts ~1998 |
| CTX | 1996-01-02 → 1997-12-29 | Centex; EODHD starts ~1998 |
| CYM | 1996-01-02 → 1997-12-29 | Cymbal; EODHD starts ~1998 |
| DALRQ | 1996-01-02 → 1997-12-29 | Delta Air Lines old bankruptcy OTC; EODHD starts ~1998 |
| DCNAQ | 1996-01-02 → 1998-12-31 | Dun & Bradstreet predecessor OTC; EODHD limited backfill |
| DJ | 1996-01-02 → 1997-12-29 | Dow Jones; EODHD starts ~1998 |
| EKDKQ | 1996-01-02 → 1997-12-29 | Eastman Kodak; EODHD starts ~1998 |
| ENRNQ | 1996-01-02 → 1997-12-29 | Enron; EODHD starts ~1998 |
| FBF | 1996-01-02 → 1997-12-29 | Firstar; EODHD starts ~1998 |
| FJ | 1996-01-02 → 1997-12-29 | Fingerhut; EODHD starts ~1998 |
| FLMIQ | 1996-01-02 → 1997-12-19 | Fleming Companies; EODHD starts ~1998 |
| FLTWQ | 1996-01-02 → 1997-12-29 | Flagstar Bancorp OTC; EODHD starts ~1998 |
| FWLT | 1996-01-02 → 1997-12-29 | Foster Wheeler; EODHD starts ~1998 |
| GAS | 1996-01-02 → 1997-12-29 | New Jersey Resources predecessor; EODHD starts ~1998 |
| GDW | 1996-01-02 → 1997-12-29 | Golden West Financial; EODHD starts ~1998 |
| GPU | 1996-01-02 → 1997-12-29 | GPU Inc.; EODHD starts ~1998 |
| GR | 1996-01-02 → 1997-12-29 | Goodrich Corporation; EODHD starts ~1998 |
| HET | 1996-01-02 → 1997-12-29 | Harrah's Entertainment; EODHD starts ~1998 |
| HPC | 1996-01-02 → 1997-12-29 | Hercules Inc.; EODHD starts ~1998 |
| IKN | 1996-01-02 → 1997-12-29 | Ikon Office Solutions; EODHD starts ~1998 |
| INCLF | 1996-01-02 → 1997-12-29 | Inco (Canadian, foreign-listed); EODHD starts ~1998 |
| JOS | 1996-01-02 → 1997-12-29 | Jos. A. Bank Clothiers; EODHD starts ~1998 |
| KATE | 1996-01-02 → 1997-12-29 | Kate Spade predecessor; EODHD starts ~1998 |
| KM | 1996-01-02 → 1997-12-29 | K-Mart; EODHD starts ~1998 |
| KMG | 1996-01-02 → 1997-01-21 | Kerr-McGee; EODHD limited early data |
| KRB | 1996-01-02 → 1997-12-29 | MBNA predecessor; EODHD starts ~1998 |
| KRI | 1996-01-02 → 1997-12-29 | Knight Ridder; EODHD starts ~1998 |
| KWP | 1996-01-02 → 1997-12-29 | King World Productions; EODHD starts ~1998 |
| LDG | 1996-01-02 → 1997-12-29 | Longs Drug Stores; EODHD starts ~1998 |
| MAY | 1996-01-02 → 1997-12-29 | May Department Stores; EODHD starts ~1998 |
| MCIC | 1996-01-02 → 1997-09-16 | MCI Communications; EODHD starts ~1998 |
| MEE | 1996-01-02 → 1997-12-29 | Massey Energy; EODHD starts ~1998 |
| MEL | 1996-01-02 → 1997-12-29 | Mellon Bank; EODHD starts ~1998 |
| MER | 1996-01-02 → 1997-12-29 | Merrill Lynch; EODHD starts ~1998 |
| MII | 1996-01-02 → 1997-12-29 | McDermott Industries; EODHD starts ~1998 |
| MKG | 1996-01-02 → 1997-12-29 | Moog Inc. predecessor; EODHD starts ~1998 |
| MWI | 1996-01-02 → 1997-12-29 | MWI Veterinary Supply; EODHD starts ~1998 |
| MWV | 1996-01-02 → 1997-12-29 | MeadWestvaco; EODHD starts ~1998 |
| MZIAQ | 1996-01-02 → 1997-12-29 | Merizan; EODHD starts ~1998 |
| NOVL | 1996-01-02 → 1997-12-29 | Novell; EODHD starts ~1998 |
| NRTLQ | 1996-01-02 → 1997-12-29 | Nortel bankruptcy OTC; EODHD starts ~1998 |
| OAT | 1996-01-02 → 1997-12-29 | Quaker Oats; EODHD starts ~1998 |
| ORX | 1996-01-02 → 1997-12-29 | Oryx Energy; EODHD starts ~1998 |
| OWENQ | 1996-01-02 → 1997-12-29 | Owens Corning bankruptcy OTC; EODHD starts ~1998 |
| PAS | 1996-01-02 → 1997-12-29 | Parametric; EODHD starts ~1998 |
| PDG | 1996-01-02 → 1997-12-29 | Placer Dome (Canadian miner); EODHD starts ~1998 |
| PGL | 1996-01-02 → 1997-12-29 | Peoples Energy; EODHD starts ~1998 |
| PHA | 1996-01-02 → 1997-12-29 | Pharmacia; EODHD starts ~1998 |
| PNU | 1996-01-02 → 1997-12-29 | Pharmacia & Upjohn; EODHD starts ~1998 |
| PPW | 1996-01-02 → 1997-12-29 | PacifiCorp; EODHD starts ~1998 |
| PRD | 1996-01-02 → 1997-12-29 | Polaroid; EODHD starts ~1998 |
| PVN | 1996-01-02 → 1998-12-31 | Providian Financial; EODHD limited early backfill |
| RBD | 1996-01-02 → 1997-12-29 | Ramada Inc.; EODHD starts ~1998 |
| RBK | 1996-01-02 → 1997-12-29 | Reebok; EODHD starts ~1998 |
| RDC | 1996-01-02 → 1997-12-29 | Rowan Companies; EODHD starts ~1998 |
| RLM | 1996-01-02 → 2000-04-27 | RL Media; limited EODHD history |
| RML | 1996-01-02 → 1997-12-29 | Russell Corporation; EODHD starts ~1998 |
| RNB | 1996-01-02 → 1997-12-29 | R&B Inc.; EODHD starts ~1998 |
| ROH | 1996-01-02 → 1997-12-29 | Rohm and Haas; EODHD starts ~1998 |
| RTN | 1996-01-02 → 1997-12-29 (+2020-04-03) | Raytheon; EODHD starts ~1998; isolated 2020 gap on RTX merger date |
| RX | 1996-11-04 → 1997-12-29 | IMS Health; EODHD starts ~1998 (Yahoo has longer gap) |
| RYAN | 1996-01-02 → 1996-12-27 | Ryan's Family Steak Houses; very early period |
| RYC | 1996-01-02 → 1997-12-29 | Rymer Foods; EODHD starts ~1998 |
| SB | 1996-01-02 → 1997-11-21 | Sara Lee predecessor; EODHD starts ~1998 |
| SFA | 1996-01-02 → 1997-12-29 | Scientific Industries; EODHD starts ~1998 |
| SGID | 1996-01-02 → 1997-12-29 | SGI Inc.; EODHD starts ~1998 |
| SIAL | 1996-01-02 → 1997-12-29 | Sigma-Aldrich; EODHD starts ~1998 |
| SMS | 1996-01-02 → 1997-12-29 | Sunglass Hut International; EODHD starts ~1998 |
| STO | 1996-01-02 → 1997-12-29 | Stone Container; EODHD starts ~1998 |
| STJ | 1996-01-02 → 1997-12-29 | St. Jude Medical; EODHD starts ~1998 |
| TCOMA | 1996-01-02 → 1997-12-29 | TCI Communications; EODHD starts ~1998 |
| TEN | 1996-01-02 → 1999-10-29 | Tenneco; limited EODHD early data |
| TIN | 1996-01-02 → 1997-12-29 | Temple-Inland; EODHD starts ~1998 |
| TNB | 1996-01-02 → 1997-12-29 | Thomas & Betts; EODHD starts ~1998 |
| TOY | 1996-01-02 → 1997-12-29 | Toys"R"Us; EODHD starts ~1998 |
| TRB | 1996-01-02 → 1997-12-29 | Tribune; EODHD starts ~1998 |
| TXU | 1996-01-02 → 1997-12-29 | TXU Corp; EODHD starts ~1998 |
| TWX | 1996-01-02 → 1997-12-29 | Time Warner; EODHD starts ~1998 |
| UCM | 1996-01-02 → 1997-12-29 | UtiliCorp United; EODHD starts ~1998 |
| UPR | 1996-10-16 → 1997-12-29 | Union Pacific Resources; EODHD starts ~1998 |
| USS | 1996-01-02 → 1997-12-29 | United States Steel; EODHD starts ~1998 |
| USW | 1996-01-02 → 1997-12-29 | US WEST; EODHD starts ~1998 |
| WAMUQ | 1997-07-02 → 1997-12-29 | Washington Mutual; EODHD starts ~1998 (Yahoo has longer gap to failure) |
| WAI | 1996-01-02 → 1998-08-06 | Wang Laboratories; limited EODHD early data |
| WLA | 1996-01-02 → 1997-12-29 | Warner-Lambert; EODHD starts ~1998 |
| WMX | 1996-01-02 → 1997-12-29 | Waste Management (old ticker); EODHD starts ~1998 |
| WNDXQ | 1996-01-02 → 1997-12-29 | Winstar OTC; EODHD starts ~1998 |
| WWY | 1996-01-02 → 1997-12-29 | Wrigley; EODHD starts ~1998 |
| WYE | 1996-01-02 → 1997-12-29 | Wyeth; EODHD starts ~1998 |

---

### 4. Patchy / Fragmented Data — Data Quality Issues in EODHD

A small number of tickers exhibit many non-contiguous isolated missing days rather than clean contiguous blocks. This points to gaps in EODHD's raw data feed for specific securities rather than corporate events.

| Ticker | Missing Period | Reason |
|--------|---------------|--------|
| BBT | 1997-12-04 → 2000-06-27 + isolated 2001-12-05 | BB&T; fragmented early data plus one isolated stray day |
| BT | 1996-01-02 → 1999-05-19 (dozens of scattered gaps) | British Telecom ADR; EODHD has very patchy coverage of this UK-listed ADR — the US data feed received the London price intermittently |
| CSR | 1996-01-02 → 2000-06-01 (many isolated gaps) | CSR plc; Australian company cross-listed on US markets — EODHD has irregular coverage for this foreign issuer |
| DIGI | 1996-01-02 → 1998-08-17 (multiple short blocks) | Digi International; fragmented EODHD coverage across early period |
| MCIC | 1996-01-02 → 1997-09-16 (two segments + isolated day) | MCI Communications; fragmented early data |
| NYX | 2007-10-25 → 2013-11-07 (+ 2 isolated gaps in 2010) | NYSE Euronext; mostly contiguous gap with two stray missing days |
| SNT | isolated days in 1996–1999 | Sonat Inc.; very sparse individual missing trading days |
| SVU | isolated days in 1996–1997 | SUPERVALU; three scattered missing trading days |
