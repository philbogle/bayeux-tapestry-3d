import json

with open('tituli.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check if Scene 1 is already there
if any(s.get('scene') == '1' for s in data):
    print("Scene 1 already exists.")
else:
    scene1 = {
      "scene": "1",
      "latin": "",
      "x": 3.7,
      "y": -1.76,
      "translations": {
        "en": { "text": "King Edward Dispatches Harold to Normandy", "context": "The tapestry begins in 1064. King Edward the Confessor, enthroned in his palace at Westminster, instructs Harold Godwinson, Earl of Wessex, to travel to Normandy on a diplomatic mission." },
        "zh": { "text": "爱德华国王派遣哈罗德前往诺曼底", "context": "故事开始于 1064 年。忏悔者爱德华国王在威斯敏斯特宫即位，指示哈罗德·戈德温森前往诺曼底执行外交任务。" },
        "fr": { "text": "Le roi Édouard envoie Harold en Normandie", "context": "La tapisserie commence en 1064. Le roi Édouard le Confesseur, intronisé dans son palais de Westminster, charge Harold Godwinson d'une mission diplomatique en Normandie." },
        "de": { "text": "König Eduard schickt Harold in die Normandie", "context": "Der Wandteppich beginnt im Jahr 1064. König Eduard der Bekenner, auf seinem Thron im Palast von Westminster, beauftragt Harold Godwinson mit einer diplomatischen Mission in die Normandie." },
        "es": { "text": "El rey Eduardo envía a Harold a Normandía", "context": "El tapiz comienza en 1064. El rey Eduardo el Confesor, entronizado en su palacio de Westminster, encomienda a Harold Godwinson una misión diplomática a Normandía." },
        "nl": { "text": "Koning Edward stuurt Harold naar Normandië", "context": "Het tapijt begint in 1064. Koning Edward de Belijder, op de troon in zijn paleis in Westminster, geeft Harold Godwinson de opdracht om op diplomatieke missie naar Normandië te reizen." },
        "pt": { "text": "O Rei Eduardo Envia Haroldo à Normandia", "context": "A tapeçaria começa em 1064. O rei Eduardo, o Confessor, entronizado em seu palácio em Westminster, instrui Harold Godwinson a viajar para a Normandia em uma missão diplomática." },
        "hi": { "text": "राजा एडवर्ड हेरोल्ड को नॉर्मंडी भेजते हैं", "context": "टेपेस्ट्री 1064 में शुरू होती है। राजा एडवर्ड द कन्फेसर हेरोल्ड गॉडविंसन को एक राजनयिक मिशन पर नॉर्मंडी की यात्रा करने का निर्देश देते हैं।" },
        "ar": { "text": "الملك إدوارد يرسل هارولد إلى نورماندي", "context": "يبدأ النسيج في عام 1064. يوجه الملك إدوارد المعترف هارولد جودوينسون للسفر إلى نورماندي في مهمة دبلوماسية." },
        "bn": { "text": "রাজা এডওয়ার্ড হ্যারল্ডকে নরম্যান্ডিতে পাঠান", "context": "টেপেস্ট্রি 1064 সালে শুরু হয়। রাজা এডওয়ার্ড কনফেসার হ্যারল্ড গডউইনসনকে একটি কূটনৈতিক মিশনে নরম্যান্ডিতে ভ্রমণ করার নির্দেশ দেন।" }
      }
    }
    
    data.insert(0, scene1)
    
    with open('tituli.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Added Scene 1 successfully.")
