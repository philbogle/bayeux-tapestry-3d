import json

contexts = {
    "6": "Guy (Wido) of Ponthieu captures Harold. Shipwrecked travelers were often held for ransom in the Middle Ages. Harold is taken prisoner.",
    "7": "Harold is taken to Guy's stronghold at Beaurain. He is treated as a high-value prisoner rather than a common captive.",
    "8": "Guy and Harold converse. Guy is likely demanding a ransom or setting terms for Harold's captivity.",
    "9": "Duke William of Normandy hears of Harold's capture and sends messengers to Guy of Ponthieu. William demands that Guy hand Harold over to him, as Guy is William's vassal.",
    "11": "The messengers arrive. Note the aggressive posture and the dwarf holding the horses, often identified as Turold.",
    "12": "A messenger returns to William to report on the situation with Count Guy.",
    "13": "Guy complies with William's demands and hands Harold over. This shifts Harold from being Guy's prisoner to William's 'guest' (and political pawn).",
    "14": "William takes Harold back to his palace at Rouen. This begins Harold's time accompanying William on campaigns in Normandy.",
    "15": "This is one of the most mysterious scenes in the tapestry. Aelfgyva is an English name, and a cleric is touching her face or striking her. Its exact meaning has been lost to history, but it likely refers to a scandal familiar to contemporary audiences.",
    "16": "William and Harold go on a military campaign against Conan II, Duke of Brittany. They pass Mont Saint-Michel, a famous abbey on a tidal island.",
    "17": "The army crosses the river Couesnon, the border between Normandy and Brittany. The shifting sands of the river mouth were incredibly dangerous.",
    "18": "Several Norman soldiers sink into the quicksand. Harold, shown displaying great physical strength, rescues two Norman soldiers from drowning.",
    "19": "The army arrives at Dol, forcing Conan to flee down a rope from his castle.",
    "19.1": "The Norman army lays siege to the town of Dinan, fighting the Bretons.",
    "19.2": "Conan II surrenders Dinan to William, passing the keys to the castle on the tip of a lance.",
    "21": "William rewards Harold for his bravery in the campaign by giving him arms (knighting him). This cements a feudal bond where Harold becomes William's subordinate in the Norman tradition.",
    "22": "The army arrives in Bayeux, the seat of Bishop Odo (William's half-brother), who likely commissioned this tapestry.",
    "23": "The climax of the Norman narrative: Harold swears a sacred oath on holy relics to support William's claim to the English throne. By later breaking this oath, Harold is cast as a perjurer, justifying William's invasion.",
    "24": "Harold is released and sails back to England.",
    "25": "Harold reports back to King Edward the Confessor. Edward appears frail and aged, foreshadowing his impending death.",
    "26": "King Edward dies. The tapestry uses non-linear storytelling here: his body is carried to Westminster Abbey, the great church he just finished building, before his death bed scene is shown.",
    "27": "On his deathbed, Edward speaks to his followers. English tradition claims he appointed Harold as his successor with his dying breath, complicating William's claim.",
    "28": "Edward passes away on January 5, 1066.",
    "29": "The English nobles offer the crown to Harold. He accepts, breaking the oath he made to William in Bayeux.",
    "30": "Harold is crowned King of England. He is shown holding the orb and sceptre, symbols of royal authority, with Archbishop Stigand nearby.",
    "32": "Halley's Comet appears in the sky in April 1066. The Anglo-Saxons view it as a terrible omen of doom, pointing at the comet in fear while a spectral invasion fleet is hinted at below.",
    "34": "News of Harold's coronation and the breaking of the oath reaches Duke William in Normandy. An English ship arrives with the message.",
    "35": "William decides to invade England to claim the throne. He orders a massive fleet of transport ships to be built.",
    "36": "The Normans cut down trees and construct ships, dragging them to the sea in preparation for the invasion.",
    "37": "Weapons, armor, and supplies (including large casks of wine) are loaded onto the ships.",
    "38": "The Norman fleet crosses the English Channel. William's flagship, the Mora, was a gift from his wife Matilda. They land at Pevensey in Sussex on September 28, 1066.",
    "39": "The valuable warhorses are unloaded from the ships. The Norman use of cavalry would prove decisive in the coming battle.",
    "40": "The Norman army moves to Hastings and begins foraging for supplies, which involved pillaging the local English countryside to provoke Harold into battle.",
    "42": "A feast is prepared. Meat is boiled and roasted on spits. This highlights the logistics of feeding a medieval army on campaign.",
    "43": "Bishop Odo blesses the food at a banquet. The semicircular table resembles depictions of the Last Supper.",
    "45": "William orders the construction of a motte-and-bailey castle at Hastings to secure his beachhead and protect his forces.",
    "46": "A messenger informs William that Harold's army is approaching. Harold had just defeated a Norwegian invasion in the north and marched his army rapidly south to meet William.",
    "47": "The Normans burn a local house, terrorizing the population. A woman and child flee the burning building.",
    "48": "The Norman cavalry rides out from Hastings on the morning of October 14, 1066, to meet the English army in battle.",
    "49": "William asks his scout, Vital, if he has spotted Harold's forces.",
    "50": "An English scout spots the Norman army and reports back to King Harold.",
    "51": "Duke William delivers a pre-battle speech to rally his troops, urging them to fight bravely.",
    "52": "The Battle of Hastings begins. The English form a shield wall on Senlac Hill. Harold's brothers, Leofwine and Gyrth, are killed early in the brutal fighting.",
    "53": "The fighting is fierce, with heavy casualties on both sides. Horses tumble, and the lower border is filled with the bodies of the dead and dying.",
    "54": "A rumor spreads that William has been killed, causing the Normans to panic. Bishop Odo rides into the fray wielding a club to rally the fleeing troops.",
    "55": "Duke William lifts his helmet to show his face to his men, proving he is still alive and restoring their morale.",
    "57": "The death of King Harold. He is traditionally identified as the figure with an arrow in his eye, though he may also be the figure being struck down by a Norman knight's sword. His death breaks the English resistance.",
    "58": "With their king dead, the English army collapses and flees the battlefield. The Normans are victorious, and William will become the Conqueror."
}

with open('tituli.json', 'r') as f:
    data = json.load(f)

for item in data:
    if item['scene'] in contexts:
        item['context'] = contexts[item['scene']]

with open('tituli.json', 'w') as f:
    json.dump(data, f, indent=2)

