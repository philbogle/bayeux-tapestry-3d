import json

with open('tituli.json', 'r') as f:
    data = json.load(f)

context_1 = "This scene marks the beginning of the tapestry's narrative in 1064, two years before the Battle of Hastings. King Edward the Confessor (who had no heir) has just dispatched his brother-in-law and the most powerful nobleman in England, Harold Godwinson, on an important mission. Harold and his followers are shown riding to his family's coastal estate at Bosham in Sussex. He visits the local church to pray for a safe journey before they set sail."
context_2 = "After enjoying a final feast at his manor, Harold and his men board their ships. They are depicted bringing hunting dogs and falcons on board with them, which historians believe was meant to signal that this was a peaceful diplomatic mission rather than a military expedition. Their intended destination was Normandy, likely to confirm William of Normandy as King Edward's successor."
context_3 = "The journey across the English Channel does not go as planned. A storm blows Harold's fleet off course, and they accidentally land in Ponthieu, a territory in northern France controlled by Count Guy (Wido). Count Guy immediately seizes Harold and his men, hoping to hold the wealthy English Earl for a massive ransom."

data[0]['context'] = context_1
data[1]['context'] = context_2
data[2]['context'] = context_3

with open('tituli.json', 'w') as f:
    json.dump(data, f, indent=2)
