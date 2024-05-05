<h1 align="center"> Narcotic Bot</h1>

<p align="center" >
</p>

<p align="center">

<img src="https://camo.githubusercontent.com/4ec342876a40b53ffc6230a41196528690f9f42b1098fd354df46c649720b4c6/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d446f636b657226636f6c6f723d323439364544266c6f676f3d446f636b6572266c6f676f436f6c6f723d464646464646266c6162656c3d">
  
<img src="https://camo.githubusercontent.com/0d38b6315bf13f3cae659b1e1c4d966d767a1c107ee017db5b5c8ed77af62e8d/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d4f70656e2b41636365737326636f6c6f723d463638323132266c6f676f3d4f70656e2b416363657373266c6f676f436f6c6f723d464646464646266c6162656c3d">
  
<img src="https://camo.githubusercontent.com/9e84c0c211dfc29162133715e87b2e359a9301d7a8b90d0fc15299d417416569/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d4f70656e2b536f757263652b496e697469617469766526636f6c6f723d334441363339266c6f676f3d4f70656e2b536f757263652b496e6974696174697665266c6f676f436f6c6f723d464646464646266c6162656c3d">
 
<img src="https://camo.githubusercontent.com/3df944c2b99f86f1361df72285183e890f11c52d36dfcd3c2844c6823c823fc1/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d507974686f6e26636f6c6f723d333737364142266c6f676f3d507974686f6e266c6f676f436f6c6f723d464646464646266c6162656c3d">

<img src="https://camo.githubusercontent.com/f14087986b1e42f4fd93d7f1d266c0b059236febb6f9f052311f60de2c0309da/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d546f722b50726f6a65637426636f6c6f723d374534373938266c6f676f3d546f722b50726f6a656374266c6f676f436f6c6f723d464646464646266c6162656c3d">

<img src="https://img.shields.io/github/license/adamlabrash/Narcotic-Bot">
  
</p>

*The White House Market online marketplace has been taken down, as such this project is now archived.*

Narcotic Bot is an open-source data extraction system and dataset that monitors narcotic product listings on illicit darknet marketplaces. Despite the significance of the drug health crisis, there is little to no public data available on the actual marketplaces and products that feed the epidemic; this project aims to address this lack of information by tracking the online narcotics trade over a sustained period. *Narcotic Bot is a resource to study the drug health crisis and is intended for academic purposes only.*

For now, the project monitors the White House Market, which is one of the most popular illicit marketplaces. The initial dataset has over 33000 product listings, and will increase as more products are listed and more marketplaces are tracked by the project.

While this project is completely legal, I do not hold responsibility for how others may use this software.

-----

## Dataset Overview

The data is available in CSV format, and will be updated periodically.

Note that the categories are taken directly from the marketplace listings:


| Main Categories        | Sub-categories           | Total Listings (Aug 2021) |
| ------------- |:-------------| ---|
| Benzos      | Pills, Powder, RC | 2677 |
| Cannabis      | Buds and Flowers, Concentrates, Edibles, Hash, Seeds, Shake, Synthetic    | 12520 |
| Dissociatives | GHB, Ketamine, MXE     | 1608 |
| Ecstasy      | MDA, MDMA, Methylone and BK     | 2026 |
| Opioids | Buprenorphine, Codeine, Dihydrocodeine, Heroin, Hydrocodone, Hydromorphone, Morphine, Opium, Oxycodone    | 1522 |
| Prescription Drugs      | Other      | 1925 |
| Psychedelics | 2C-B, DMT, LSD, Shrooms      | 4315 |
| Steroids      | Other      | 1182 |
| Stimulants | Adderall, Cocaine, Crack, Mephedrone, Meth, Speed     | 5520 |
| Tobacco      | Other      | 19 |
| Weight Loss | Other      | 41 |


-----

## Schema

The narcotics table is populated with products each with the following schema:

| Attribute | Data Properties | Description |
| ----- |:-----| ------------|
| id | SERIAL PRIMARY KEY | Unique number identifying the product within the dataset|
| website | VARCHAR(50) NOT NULL | The website that the product is listed |
| title | TEXT NOT NULL | Description of the product listing |
| update_at | TIMESTAMP NOT NULL | Date that the product listing was extracted (GST) |
| vendor | VARCHAR(100) NOT NULL | The name of the product lister |
| category | VARCHAR(50) NOT NULL | General classification of the drug i.e. 'benzos' or 'cannabis'|
| price | FLOAT NOT NULL | Cost of the product in USD |
| sub_category | VARCHAR(50) | Specific classification of the drug i.e. 'pills', 'edibles' |
| shipping_origin | VARCHAR(50) | Where the product is shipped from (not always the true origin) |
| ships_to | VARCHAR(50) | Regions and countries where the product is available |
| inventory_status | VARCHAR(50) | In stock, low stock, etc. |


Example entry:

| id | website | title | update_at | vendor | category | price | sub_category | shipping_origin | ships_to | inventory_status |
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27910 | White House Market | 1g SPEEDPASTE AMPHETAMINE 63-73% PURITY | 2020-07-12 00:00:00 | clicknbuy | Stimulants | 9.24 | Speed | Netherlands | Worldwide | In stock |


-----

Future scope:
* Extract products from additional marketplaces
* NLP and advanced analysis based on title and descriptions
* Web-hosted dashboard
* Seperate dataset of vendors
