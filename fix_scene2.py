import json

with open('bayeux_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

replacements = {
  "en": "Harold rides to his coastal estate at Bosham and prays at the local church before setting sail.",
  "zh": "哈罗德骑马前往他位于博舍姆的沿海庄园，在启航前在当地教堂祈祷。",
  "fr": "Harold se rend à son domaine côtier de Bosham et prie à l'église locale avant de mettre les voiles.",
  "de": "Harold reitet zu seinem Küstenanwesen in Bosham und betet in der örtlichen Kirche, bevor er in See sticht.",
  "es": "Harold viaja hasta su finca costera en Bosham y reza en la iglesia local antes de zarpar.",
  "nl": "Harold rijdt naar zijn landgoed aan de kust in Bosham en bidt in de plaatselijke kerk voordat hij vertrekt.",
  "pt": "Harold cavalga até sua propriedade costeira em Bosham e ora na igreja local antes de zarpar.",
  "hi": "हेरोल्ड बोशम में अपनी तटीय संपत्ति की ओर जाता है और यात्रा शुरू करने से पहले स्थानीय चर्च में प्रार्थना करता है।",
  "ar": "يركب هارولد إلى مزرعته الساحلية في بوشام ويصلي في الكنيسة المحلية قبل الإبحار.",
  "bn": "হ্যারল্ড বোশামে তার উপকূলীয় এস্টেটে চড়ে এবং যাত্রা করার আগে স্থানীয় চার্চে প্রার্থনা করে।"
}

# The second scene is at index 1 in the tituli array
scene2 = next(s for s in data["tituli"] if s["scene"] == "2")

for lang, new_context in replacements.items():
    if lang in scene2["translations"]:
        scene2["translations"][lang]["context"] = new_context

with open('bayeux_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Scene 2 context fixed successfully.")
