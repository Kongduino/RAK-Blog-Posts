# LoRa 101

D'abord, un cocorico. LoRa est une technologie inventée en France, par Cycleo à Grenoble, puis of course les inventeurs ont vendu aux Ricains. Comme d'hab.

LoRa est la couche physique de transport des données par une sorte de radio à longue portée (LoRa = Long Range). C'est en quelque sorte l'UDP de l'internet. Fire and forget. Elle utilise des fréquences sub-GHz, en théorie de 150 à 950 MHz, mais les gouvernements se mêlent de ce qui ne les regardent pas 😉 et les fréquences autorisées pour LoRaWAN sont beaucoup plus restreintes. 70 cm (433 MHz), autour de 35 cm (868 MHz, parfois 865), 32 cm (915 MHz), voire 923 MHz en Asie. Il est possible de faire du LoRa sur un très large spectre, mais la maréchaussée pourrait objecter.

LoRa est un protocole patenté, et Semtech, le propriétaire, est féroce sur le sujet, et le protocole est quasi secret. Donc peu documenté. Mais le principe est : le message est précédé d'un préambule de X octets (8 en général mais paramétrable), les "bits" radio (chirps: Compressed High-Intensity Radar Pulse) sont "étalés" (comme la confiture sur une tartine) sur un certain spectre, paramétrable, et une bande passante, aussi paramétrable. Ces 2 facteurs, ainsi que d'autres, détermineront la vitesse de transmission, sa fiabilité et sa portée. Plus le spectre est élevé (max SF 12 : 2^12, 4096 chirps par symbole envoyé), plus il y a de chirps par octet transmis, et plus la transmission est fiable et peut aller loin (et plus elle est lente). A l'opposé, plus la bande passante est restreinte, moins il y a de chances d'interférences, et plus là aussi la transmission est fiable et peut aller loin (et se ralentit aussi : plus le tuyau est mince, moins y'a de bits qui sont envoyés par seconde...). SF11 et SF12 sont interdits aux Etats-Unis, alors que par exemple la puissance de transmission est légale jusqu'à 30 dbm. Donc vérifier dans chaque pays ce qui est légal quand on fait du LoRa – pour LoRaWAN les librairies des gateways et end-devices le font automatiquement.

|Spreading Factor|Speed|
|---|---|
|12|293 bps|
|11|537 bps|
|10|977 bps|
|9|1.8 kbps|
|8|3.1 kbps|
|7|5.5 kbps|

Les bandes passantes possibles sont, pour LoRa, 500, 250, 125, 62.5, 41.7, 31.25, 20.8, 15.6, 10.4, et 7.8 KHz, et en LoRaWAN, plus restrictif, 125, 250 et 500 kHz. Ce qui fait que beaucoup de développeurs limitent leur code à 125, 250, 500 même pour LoRa (et même chez Semtech...), alors qu'il n'y a aucune raison. Juste de l'ignorance et de la paresse... En fait, LoRaWAN est extrêmement codifié, en termes de réglages, et temps de transmission, pour coller aux lois locales, et assurer un "fair use", alors que LoRa même, ben euh, non. C'est pas par hasard que j'ai pris #LoRaBandit comme tag...

LoRa, c'est la CB de l'IoT, LoRaWAN les radio-amateurs licenciés, en quelque sorte. Y compris dans la structure, où les gateways LoRaWAN servent de relais pour tout le monde (sauf cas spéciaux, les réseaux privatifs). Avec LoRa tout le monde peut t'entendre – sur des réglages identiques – et te perturber tes comms, alors que pour LoRaWAN, avec 8 ou 16 canaux, chiffrage AES, etc, les messages passent chiffrés, proprement, et arrivent au destinataire seulement. Du coup LoRaWAN requiert plus de matos – il faut une ou plusieurs gateways – mais si la région est déjà couverte, l'investissement n'est pas nécessaire : on peut surfer sur les gateways existantes.

LoRa requiert moins de matos – en tout cas au début, mais tout le taf reste à faire en termes de transmission, chiffrage, adressage, etc. Et les produits LoRa de base ne sont pas toujours très bons, alors que les gateways elles sont faites pour être performantes. Donc il y a du pour et du contre aux deux.

LoRaWAN requiert ceci dit plus de travail sur le traitement des données – une fois les paquets arrivés chez TTN, le site concentrateur utilisé par une majorité de sustèmes, les récupérer peut demander un travail d'Hercule. Il y a pas mal d'options, y compris de redirection vers des services "cloud", ainsi que des webhooks vers un site web perso, ou un autre aggrégateur, ou encore un broker MQTT (TTN en fournit un : c'est souvent la solution la plus simple). Plein de choix, mais faut pouvoir assurer derrière.

L'avantage clair de LoRa dans ce cas est que les données ne font pas le tour de la terre pour arriver à destination. Elles ne quittent jamais l'appareil qui les a reçues, sauf si le traitement le demande. J'ai mon mini jardin sur le toit, un capteur sol en LoRaWAN, les données font capteur --> ma gateway --> eu1 TTN --> mon serveur ici. Round trip HK-Europe. Un autre capteur est en LoRa : capteur --> ordinateur, point barre.

De plus, la liberté 