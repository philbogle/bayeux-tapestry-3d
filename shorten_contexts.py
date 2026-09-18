import json

contexts = {
    "2": "The tapestry begins in 1064. King Edward the Confessor sends Harold Godwinson on a diplomatic mission to Normandy. Harold rides to his coastal estate at Bosham and prays at the local church before setting sail.",
    "3": "Harold and his men board their ships with hunting dogs and falcons. These animals signal that this is a peaceful diplomatic mission, not a military expedition.",
    "4": "A storm blows Harold's fleet off course across the English Channel. They land in Ponthieu, where Count Guy (Wido) immediately seizes Harold in hopes of demanding a massive ransom."
}

with open('tituli.json', 'r') as f:
    data = json.load(f)

for item in data:
    if item['scene'] in contexts:
        item['context'] = contexts[item['scene']]

with open('tituli.json', 'w') as f:
    json.dump(data, f, indent=2)

