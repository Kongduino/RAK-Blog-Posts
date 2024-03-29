# LoRa 101

D'abord, un cocorico. LoRa est une technologie inventée en France, par Cycleo à Grenoble, puis of course les inventeurs ont vendu aux Ricains. Comme d'hab.

LoRa est la couche physique de transport des données par une sorte de radio à longue portée (LoRa = Long Range). C'est en quelque sorte l'UDP de l'internet. Fire and forget. Elle utilise des fréquences sub-GHz, en théorie de 150 à 950 MHz, mais les gouvernements se mêlent de ce qui ne les regardent pas 😉 et les fréquences autorisées pour LoRaWAN sont beaucoup plus restreintes. 70 cm (433 MHz), autour de 35 cm (868 MHz, parfois 865), 32 cm (915 MHz), voire 923 MHz en Asie. Il est possible de faire du LoRa sur un très large spectre, mais la maréchaussée pourrait objecter.

LoRa est un protocole patenté, et Semtech, le propriétaire, est féroce sur le sujet, et le protocole est quasi secret. Donc peu documenté. Mais le principe est que LoRa® est une technique de modulation à spectre étalé basée sur le Compressed High-Intensity Radar Pulse, en abrégé le "chirp". Le message à envoyer est précédé d'un préambule de X octets (8 en général mais paramétrable, plus 4 octets rajoutés par le module) et les "bits" radio (*chips*) sont "étalés" (comme de la confiture sur une tartine) sur un certain spectre, paramétrable, et une bande passante, aussi paramétrable. Ces 2 facteurs, ainsi que d'autres, détermineront la vitesse de transmission, sa fiabilité et sa portée. Plus le spectre est élevé (max SF 12 : 2^12, 4'096 *chips* par symbole envoyé), plus il y a de *chips* par octet transmis, et plus la transmission est fiable et peut aller loin (et plus elle est lente). A l'opposé, plus la bande passante est restreinte, moins il y a de chances d'interférences, et plus là aussi la transmission est fiable et peut aller loin (et se ralentit aussi : plus le tuyau est mince, moins y'a de bits qui sont envoyés par seconde...). SF11 et SF12 sont interdits aux Etats-Unis, alors que par exemple la puissance de transmission est légale jusqu'à 30 dbm. Donc vérifier dans chaque pays ce qui est légal quand on fait du LoRa – pour LoRaWAN les librairies des gateways et end-devices le font automatiquement.

Figure 1 : vitesse de transmission en fonction de SF / BW
|SF|BW 500|BW 250|BW 125|
|---|---|---|---|
|12|1,172 bps|586 bps|293 bps|
|11|2,148 bps|1,074 bps|537 bps|
|10|3,906 bps|1,953 bps|977 bps|
|9|7,031 bps|3,516 bps|1.8 kbps|
|8|12,500 bps|6,250 bps|3.1 kbps|
|7|21,875 bps|10,938 bps|5.5 kbps|


Les bandes passantes possibles sont, pour LoRa, 500, 250, 125, 62.5, 41.7, 31.25, 20.8, 15.6, 10.4, et 7.8 KHz, et en LoRaWAN, plus restrictif, 125, 250 et 500 kHz. Ce qui fait que beaucoup de développeurs limitent leur code à 125, 250, 500 même pour LoRa (et même chez Semtech...), alors qu'il n'y a aucune raison. Juste de l'ignorance et de la paresse... En fait, LoRaWAN est extrêmement codifié, en termes de réglages, et temps de transmission, pour coller aux lois locales, et assurer un "fair use", alors que LoRa même, ben euh, non. C'est pas par hasard que j'ai pris [#LoRaBandit](https://twitter.com/search?q=%23LoRaBandit&src=typed_query&f=live) comme tag...

![SF7_BW125](SF7_BW125.png)
*SF 7, BW 125 KHz*

![SF7_BW62.5](SF7_BW62.5.png)
*SF 7, BW 62.5 KHz*

![SF7_BW20.8](SF7_BW20.8.png)
*SF 7, BW 20.8 KHz*

![SF12_BW125](SF12_BW125.png)
*SF 12, BW 125 KHz*

![SF12_BW62.5](SF12_BW62.5.png)
*SF 12, BW 62.5 KHz*

![SF12_BW20.8](SF12_BW20.8.png)
*SF 12, BW 20.8 KHz*



LoRa, c'est la CB de l'IoT, LoRaWAN les radio-amateurs licenciés, en quelque sorte. Y compris dans la structure, où les gateways LoRaWAN servent de relais pour tout le monde (sauf cas spéciaux, les réseaux privatifs). Avec LoRa tout le monde peut t'entendre – sur des réglages identiques – et te perturber tes comms, alors que pour LoRaWAN, avec 8 ou 16 canaux, chiffrage AES, etc, les messages passent chiffrés, proprement, et arrivent au destinataire seulement. Du coup LoRaWAN requiert plus de matos – il faut une ou plusieurs gateways – mais si la région est déjà couverte, l'investissement n'est pas nécessaire : on peut surfer sur les gateways existantes.

LoRa requiert moins de matériel – en tout cas au début, mais tout le travail reste à faire en terme de transmission, chiffrage, adressage, etc. Et les produits LoRa de base ne sont pas toujours très bons, alors que les gateways elles sont faites pour être performantes. Donc il y a du pour et du contre aux deux.

LoRaWAN requiert ceci dit plus de travail sur le traitement des données – une fois les paquets arrivés chez TTN, le site concentrateur utilisé par une majorité de systèmes, les récupérer peut demander un travail d'Hercule. Il y a pas mal d'options, y compris de redirection vers des services "cloud", ainsi que des webhooks vers un site web perso, ou un autre aggrégateur, ou encore un broker MQTT (TTN en fournit un : c'est souvent la solution la plus simple). Plein de choix, mais faut pouvoir assurer derrière.

L’avantage clair de LoRa dans ce cas est que les données ne font pas le tour de la terre pour arriver à destination. Elles ne quittent jamais l’appareil qui les a reçues, sauf si le traitement le demande. J’ai mon mini jardin sur le toit, un capteur sol en LoRaWAN, les données font capteur → ma gateway → eu1 TTN → mon serveur ici. Round trip HK-Europe. Un autre capteur est en LoRa : capteur → carte RAK811 → ordinateur, point barre.
Mais une fois les données arrivées, le traitement est plus ou moins le même : est-ce que je fais ma petite sauce moi-même (Python → SQLite → CSV/Autre format text → HTML/CSS/JS), ou est-ce que je passe par Node Red, InfluxDB, Grafananana ? (Dans mon cas la réponse est toujours ma propre sauce mais vous n'êtes pas obligés d'être des abrutis comme moi).

Enfin, la liberté (technique)  de réglages de LoRa permet d'atteindre des performances souvent meilleures que LoRaWAN : j'ai déjà mentionné l'impossibilité d'utiliser SF11 et SF12 en LoRaWAN aux Etats-Unis, alors que ces réglages apportent des performances supérieures, mais aussi la possibilité de réduire la bande passante en dessous de 125 KHz. Evidemment, ces réglages influencent la vitesse de transmission, et un petit paquet d'une dizaine d'octets peut facilement prendre 2 à 3 secondes. Voir [LoRa Calc](https://kongduino.github.io/Lora-Calculations/) pour tester.

![Exemple](Exemple.png)

