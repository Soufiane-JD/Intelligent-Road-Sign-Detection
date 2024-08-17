import csv

# Dictionary containing the sign details
sign_details = {
    "Speed limit (20km/h)": {
        "description": "Maximum speed of 20 km/h allowed.",
        "image": "assets/0.png"
    },
    "Limite de vitesse (20 km/h)": {
        "description": "Vitesse maximale autorisée de 20 km/h.",
        "image": "assets/0.png"
    },
    "حد السرعة (20 كم/س)": {
        "description": "السرعة القصوى المسموح بها 20 كم/س.",
        "image": "assets/0.png"
    },

    "Speed limit (30km/h)": {
        "description": "Maximum speed of 30 km/h allowed.",
        "image": "assets/1.png"
    },
    "Limite de vitesse (30 km/h)": {
        "description": "Vitesse maximale autorisée de 30 km/h.",
        "image": "assets/1.png"
    },
    "حد السرعة (30 كم/س)": {
        "description": "السرعة القصوى المسموح بها 30 كم/س.",
        "image": "assets/1.png"
    },

    "Speed limit (50km/h)": {
        "description": "Maximum speed of 50 km/h allowed.",
        "image": "assets/2.png"
    },
    "Limite de vitesse (50 km/h)": {
        "description": "Vitesse maximale autorisée de 50 km/h.",
        "image": "assets/2.png"
    },
    "حد السرعة (50 كم/س)": {
        "description": "السرعة القصوى المسموح بها 50 كم/س.",
        "image": "assets/2.png"
    },

    "Speed limit (60km/h)": {
        "description": "Maximum speed of 60 km/h allowed.",
        "image": "assets/3.png"
    },
    "Limite de vitesse (60 km/h)": {
        "description": "Vitesse maximale autorisée de 60 km/h.",
        "image": "assets/3.png"
    },
    "حد السرعة (60 كم/س)": {
        "description": "السرعة القصوى المسموح بها 60 كم/س.",
        "image": "assets/3.png"
    },

    "Speed limit (70km/h)": {
        "description": "Maximum speed of 70 km/h allowed.",
        "image": "assets/4.png"
    },
    "Limite de vitesse (70 km/h)": {
        "description": "Vitesse maximale autorisée de 70 km/h.",
        "image": "assets/4.png"
    },
    "حد السرعة (70 كم/س)": {
        "description": "السرعة القصوى المسموح بها 70 كم/س.",
        "image": "assets/4.png"
    },

    "Speed limit (80km/h)": {
        "description": "Maximum speed of 80 km/h allowed.",
        "image": "assets/5.png"
    },
    "Limite de vitesse (80 km/h)": {
        "description": "Vitesse maximale autorisée de 80 km/h.",
        "image": "assets/5.png"
    },
    "حد السرعة (80 كم/س)": {
        "description": "السرعة القصوى المسموح بها 80 كم/س.",
        "image": "assets/5.png"
    },

    "Speed limit (100km/h)": {
        "description": "Maximum speed of 100 km/h allowed.",
        "image": "assets/7.png"
    },
    "Limite de vitesse (100 km/h)": {
        "description": "Vitesse maximale autorisée de 100 km/h.",
        "image": "assets/7.png"
    },
    "حد السرعة (100 كم/س)": {
        "description": "السرعة القصوى المسموح بها 100 كم/س.",
        "image": "assets/7.png"
    },

    "Speed limit (120km/h)": {
        "description": "Maximum speed of 120 km/h allowed.",
        "image": "assets/8.png"
    },
    "Limite de vitesse (120 km/h)": {
        "description": "Vitesse maximale autorisée de 120 km/h.",
        "image": "assets/8.png"
    },
    "حد السرعة (120 كم/س)": {
        "description": "السرعة القصوى المسموح بها 120 كم/س.",
        "image": "assets/8.png"
    },

    "Yield": {
        "description": "Slow down and be ready to stop if necessary to let a pedestrian pass.",
        "image": "assets/13.png"
    },
    "Cédez le passage": {
        "description": "Cédez le passage aux autres véhicules et piétons.",
        "image": "assets/13.png"
    },
    "إعطاء الأولوية": {
        "description": "أعط الأولوية للمركبات والمشاة الآخرين.",
        "image": "assets/13.png"
    },

    "Stop": {
        "description": "You must stop completely and check for other vehicles.",
        "image": "assets/14.png"
    },
    "Arret": {
        "description": "Vous devez vous arrêter complètement et vérifier les autres véhicules.",
        "image": "assets/14.png"
    },
    "قف": {
        "description": "يجب أن تتوقف تمامًا وتتحقق من السيارات الأخرى.",
        "image": "assets/14.png"
    },

    "Vehicles over 3.5 metric tons prohibited": {
        "description": "Vehicles over 3.5 metric tons are prohibited from entering.",
        "image": "assets/16.png"
    },
    "Véhicules de plus de 3,5 tonnes interdits": {
        "description": "Les véhicules de plus de 3,5 tonnes sont interdits d'entrée.",
        "image": "assets/16.png"
    },
    "ممنوع المركبات فوق 3.5 طن": {
        "description": "ممنوع دخول المركبات التي تزيد عن 3.5 طن.",
        "image": "assets/16.png"
    },

    "No entry": {
        "description": "No vehicles are allowed to enter.",
        "image": "assets/17.png"
    },
    "Sens interdit": {
        "description": "Entrée interdite aux véhicules.",
        "image": "assets/17.png"
    },
    "ممنوع الدخول": {
        "description": "لا يُسمح بدخول المركبات.",
        "image": "assets/17.png"
    },

    "Pedestrians": {
        "description": "Alerts drivers to areas where pedestrians may be crossing the street. Drivers should slow down and prepare to stop.",
        "image": "assets/27.png"
    },
    "Pietons": {
        "description": "Avertit les conducteurs des zones où les piétons peuvent traverser la rue. Les conducteurs doivent ralentir et se préparer à s'arrêter.",
        "image": "assets/27.png"
    },
    "مشاة": {
        "description": "ينبه السائقين إلى المناطق التي قد يعبر فيها المشاة الشارع. يجب على السائقين التباطؤ والاستعداد للتوقف.",
        "image": "assets/27.png",
    },

    "Children crossing": {
        "description": "Indicates areas near schools or parks where children are likely to cross the road. Extra caution is advised.",
        "image": "assets/28.png",
    },
    "Passage d'enfants": {
        "description": "Indique les zones proches des écoles ou des parcs où les enfants sont susceptibles de traverser la route. Une prudence accrue est conseillée.",
        "image": "assets/28.png",
    },
    "معبر للأطفال": {
        "description": "يشير إلى المناطق القريبة من المدارس أو الحدائق حيث من المرجح أن يعبر الأطفال الطريق. يُنصح بتوخي الحذر الشديد.",
        "image": "assets/28.png",
    },

    "Bicycles crossing": {
        "description": "Indicates a crossing where bicycles and possibly pedestrians share the crossing path. Drivers should watch for cyclists.",
        "image": "assets/29.png"
    },
    "Passage de velos": {
        "description": "Indique un passage où les bicyclettes et éventuellement les piétons partagent le chemin de croisement. Les conducteurs doivent surveiller les cyclistes.",
        "image": "assets/29.png",
    },
    "عبور الدراجات": {
        "description": "يشير إلى معبر حيث تشترك الدراجات وربما المشاة في مسار العبور. يجب على السائقين مراقبة الدراجين.",
        "image": "assets/29.png",
    },

    "Roundabout": {
        "description": "Indicates the approach to a roundabout, a circular intersection where drivers must yield to traffic in the roundabout before entering.",
        "image": "assets/40.png"
    },
    "Rond-point": {
        "description": "Indique l'approche d'un rond-point, une intersection circulaire où les conducteurs doivent céder le passage à la circulation dans le rond-point avant d'entrer.",
        "image": "assets/40.png",
    },
    "الدوار": {
        "description": "يشير إلى الاقتراب من دوار، وهو تقاطع دائري حيث يجب على السائقين إعطاء الأولوية لحركة المرور في الدوار قبل الدخول.",
        "image": "assets/40.png",
    },

    "Parking": {
        "description": "Indicates a designated area where vehicles are allowed to park. Follow local rules for duration and payment if applicable.",
        "image": "assets/43.png"
    },
    "stationnement": {
        "description": "Indique une zone désignée où les véhicules sont autorisés à se garer. Suivez les règles locales concernant la durée et le paiement si applicable.",
        "image": "assets/43.png",
    },
    "موقف سيارات": {
        "description": "يشير إلى منطقة مخصصة يُسمح فيها بوقوف السيارات. اتبع القواعد المحلية بخصوص المدة والدفع إن وجدت.",
        "image": "assets/43.png",
    },

    "No Parking": {
        "description": "Indicates areas where vehicles are not allowed to park. Parking here may lead to fines or towing.",
        "image": "assets/44.png"
    },
    "Pas de stationnement": {
        "description": "Indique les zones où le stationnement des véhicules est interdit. Se garer ici peut entraîner des amendes ou le remorquage.",
        "image": "assets/44.png",
    },
    "ممنوع الوقوف": {
        "description": "يشير إلى المناطق التي لا يُسمح بوقوف السيارات فيها. الوقوف هنا قد يؤدي إلى غرامات أو سحب السيارة.",
        "image": "assets/44.png",
    },
}

# Open a CSV file to write to
with open('SignDetails.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Sign', 'Description', 'Image'])

    # Write data rows for each sign
    for sign, details in sign_details.items():
        writer.writerow([sign, details['description'], details['image']])

print("CSV file has been created successfully.")
