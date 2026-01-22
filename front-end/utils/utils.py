# ------------------------------------------- MAPEOS -----------------------------------------------
METRIC_VIDEO_LABEL_MAP = {
    "views": "Visualizaciones",
    "likes": "Likes",
    "comments": "Comentarios"
}

METRIC_CHANNEL_LABEL_MAP = {
    "views": "Visualizaciones",
    "videos": "Vídeos",
    "subscribers": "Suscriptores"
}

SENTIMENT_UI_TO_DB = {
    "Positivo": "positive",
    "Neutral": "neutral",
    "Negativo": "negative",
}

EMOTION_UI_TO_DB = {
    "Alegría": "Joy",
    "Tristeza": "Sadness",
    "Ira": "Anger",
    "Asco": "Disgust",
    "Miedo": "Fear",
    "Sorpresa": "Surprise",
    "Neutral": "Neutral",
    "Otros": "Others",
}

EMOTION_LABEL_MAP = {
    "Joy": "Alegría",
    "Sadness": "Tristeza",
    "Anger": "Ira",
    "Fear": "Miedo",
    "Surprise": "Sorpresa",
    "Disgust": "Asco",
    "Neutral": "Neutral",
    "Others": "Otros"
}

EMOTION_COLOR_MAP = {
    "Joy": "#ffd700",
    "Sadness": "#3b82f6",
    "Anger": "#ef4444",
    "Fear": "#a855f7",
    "Surprise": "#f38e3c",
    "Disgust": "#22c55e",
    "Neutral": "#e15c97",
    "Others": "#32ae9e"
}

SENTIMENT_LABEL_MAP = {
    "positive": "Positivo",
    "negative": "Negativo",
    "neutral": "Neutral"
}

SENTIMENT_COLOR_MAP = {
    "positive": "#22c55e",
    "negative": "#ef4444",
    "neutral": "#3b82f6"
}

MONTH_MAP = {
    1: "Ene", 
    2: "Feb", 
    3: "Mar", 
    4: "Abr", 
    5: "May", 
    6: "Jun", 
    7: "Jul", 
    8: "Ago", 
    9: "Sep", 
    10: "Oct", 
    11: "Nov", 
    12: "Dic"
}

SPANISH_STOPWORDS = {
    "a", "actualmente", "adelante", "además", "afirmó", "agregó", "ahora", "ahí", "al", "algo", "alguien",
    "alguna", "algunas", "alguno", "algunos", "algún", "alrededor", "ambos", "ampleamos", "ante",
    "anterior", "antes", "apenas", "aproximadamente", "aquel", "aquellas", "aquellos", "aqui",
    "aquí", "arriba", "aseguró", "así", "atras", "aunque", "ayer", "añadió", "aún", "bajo", "bastante",
    "bien", "buen", "buena", "buenas", "bueno", "buenos", "cada", "casi", "cerca", "cierta", "ciertas",
    "cierto", "ciertos", "cinco", "comentó", "como", "con", "conocer", "conseguimos", "conseguir",
    "considera", "consideró", "consigo", "consigue", "consiguen", "consigues", "contra", "cosas",
    "creo", "cual", "cuales", "cualquier", "cuando", "cuanto", "cuatro", "cuenta", "cómo", "da", "dado",
    "dan", "dar", "de", "debe", "deben", "debido", "decir", "dejó", "del", "demás", "dentro", "desde",
    "después", "dice", "dicen", "dicho", "dieron", "diferente", "diferentes", "dijeron", "dijo", "dio",
    "donde", "dos", "durante", "e", "ejemplo", "el", "él", "ella", "ellas", "ello", "ellos", "embargo",
    "empleais", "emplean", "emplear", "empleas", "empleo", "en", "encima", "encuentra", "entonces",
    "entre", "era", "erais", "eramos", "eran", "eras", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estabais", "estaban", "estabas", "estad", "estada", "estadas", "estado", "estados",
    "estais", "estamos", "estan", "estando", "estar", "estaremos", "estará", "estarán", "estarás", "estaré",
    "estaréis", "estaría", "estaríais", "estaríamos", "estarían", "estarías", "estas", "este", "estemos",
    "esto", "estos", "estoy", "estuve", "estuviera", "estuvierais", "estuvieran", "estuvieras", "estuvieron",
    "estuviese", "estuvieseis", "estuviesen", "estuvieses", "estuvimos", "estuviste", "estuvisteis",
    "estuvíéramos", "estuviésemos", "estuvo", "está", "estábamos", "estáis", "están", "estás", "esté",
    "estéis", "estén", "estés", "ex", "existe", "existen", "explicó", "expresó", "fin", "fue", "fuera",
    "fuerais", "fueran", "fueras", "fueron", "fuese", "fueseis", "fuesen", "fueses", "fui", "fuimos",
    "fuiste", "fuisteis", "fuéramos", "fuésemos", "gran", "grandes", "gueno", "ha", "haber", "habida",
    "habidas", "habido", "habidos", "habiendo", "habremos", "habrá", "habrán", "habrás", "habré",
    "habréis", "habría", "habríais", "habríamos", "habrían", "habrías", "habéis", "había", "habíais",
    "habíamos", "habían", "habías", "hace", "haceis", "hacemos", "hacen", "hacer", "hacerlo", "haces",
    "hacia", "haciendo", "hago", "han", "has", "hasta", "hay", "haya", "hayamos", "hayan", "hayas",
    "hayáis", "he", "hecho", "hemos", "hicieron", "hizo", "hoy", "hola", "hube", "hubiera", "hubierais", "hubieran",
    "hubieras", "hubieron", "hubiese", "hubieseis", "hubiesen", "hubieses", "hubimos", "hubiste",
    "hubisteis", "hubiéramos", "hubiésemos", "hubo", "igual", "incluso", "indicó", "informó", "intenta",
    "intentais", "intentamos", "intentan", "intentar", "intentas", "intento", "ir", "junto", "la", "lado",
    "largo", "las", "le", "les", "llegó", "lleva", "llevar", "lo", "los", "luego", "lugar", "manera", "más", "mas",
    "manifestó", "mayor", "me", "mediante", "mejor", "mencionó", "menos", "mi", "mientras", "mio",
    "mis", "misma", "mismas", "mismo", "mismos", "modo", "momento", "mucha", "muchas", "mucho", "muchos",
    "muy", "más", "mí", "mía", "mías", "mío", "míos", "nada", "nadie", "ni", "ninguna", "ningunas",
    "ninguno", "ningunos", "ningún", "no", "nos", "nosotras", "nosotros", "nuestra", "nuestras", "nuestro",
    "nuestros", "nueva", "nuevas", "nuevo", "nuevos", "nunca", "o", "ocho", "os", "otra", "otras", "otro",
    "otros", "para", "parece", "parte", "pasar", "pasada", "pasado", "pero", "poca", "pocas", "poco",
    "pocos", "podeis", "podemos", "poder", "podría", "podrías", "podríais", "podríamos", "podrían", "podrias",
    "podrá", "podrán", "podría", "podrían", "poner", "por", "por qué", "porque", "posible", "primer",
    "primera", "primero", "primeros", "principalmente", "propia", "propias", "propio", "propios", "próximo", "q",
    "próximos", "pudo", "pueda", "puede", "pueden", "puedo", "pues", "que", "quedó", "queremos", "quien",
    "quienes", "quiere", "quién", "qué", "realizado", "realizar", "realizó", "respecto", "saludo", "saludos", "sabe", "sabeis",
    "sabemos", "saben", "saber", "sabes", "se", "sea", "seamos", "sean", "seas", "segunda", "segundo",
    "según", "seis", "ser", "seremos", "será", "serán", "serás", "seré", "seréis", "sería", "seríais",
    "seríamos", "serían", "serías", "seáis", "señaló", "si", "sido", "siempre", "siendo", "siete", "sigue",
    "siguiente", "sin", "sino", "sobre", "sois", "sola", "solamente", "solas", "solo", "solos", "somos",
    "son", "soy", "su", "sus", "suya", "suyas", "suyo", "suyos", "sí", "sólo", "tal", "también", "tampoco",
    "tan", "tanto", "te", "tengo", "tenemos", "tenía", "tener", "ti", "tiene", "tienen", "tienes", "tiempo", "tipo", "toda", "todas", "todavía",
    "todo", "todos", "total", "trabaja", "trabajais", "trabajamos", "trabajan", "trabajar", "trabajas", "trabajo",
    "tras", "trata", "través", "tres", "tu", "tus", "tuve", "tuvo", "tuya", "tuyas", "tuyo", "tuyos", "tú",
    "ultimo", "un", "una", "unas", "uno", "unos", "usa", "usais", "usamos", "usan", "usar", "usas", "uso",
    "usted", "va", "vais", "valor", "vamos", "van", "varias", "varios", "vaya", "veces", "ver", "verdad",
    "verdadera", "verdadero", "vez", "vosotras", "vosotros", "voy", "vuestra", "vuestras", "vuestro", "vuestros", "x", "y", "ya", "yo"
}

YOUTUBE_LANGUAGE = { "video", "videos", "vídeo", "vídeos", "canal", "like", "gracias", "podcast"}