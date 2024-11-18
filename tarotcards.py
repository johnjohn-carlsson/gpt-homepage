import random

majorCards = {
    "The Fool": 
        ["Obegränsad Potential", "Nya Begynnelser, Nya Idéer, Oskuld, Äventyr",
         "Oansvarighet, Orädsla, Risk", "Ja", "tarot-fool.jpg"],
    "The Magician": 
        ["Beslutsamhet och Vilja", "Viljestyrka, Skapande, Inre Styrka, Manifestation",
         "Manipulering, Illusioner", "Ja", "tarot-magician.jpg"],
    "The High Priestess": 
        ["Att Lära och Lyssna", "Inre Röst, Omedvetande, Den Gudomliga Kvinnligheten, Trygghet",
         "Förtryckta Känslor, Återhållssamhet, Tystnad", "Yes", "tarot-highpriestess.jpg"],
    "The Empress": 
        ["Den Kvinnliga Sidan", "Kvinnlighet, Omsorg, Fertilitet, Överskott, Firande",
         "Beroende, Kvävande, Tomhet", "Ja", "tarot-empress.jpg"],
    "The Emperor":
        ["Fadersgestalten", "Auktoritet, Struktur, Fadersfigur, Förändring",
         "Överdriven kontroll, Rigiditet, Dominering", "Ja", "tarot-emperor.jpg"],
    "The Hierophant":
        ["Att Följa Strömmen", "Spritualitet, Tradition, Konformitet, Moral, Etik",
         "Uppror, Underminering, Frihet, Individuella Övertygelser", "Neutral", "tarot-hierophant.jpg"],
    "The Lovers":
        ["Livsförändrande Val", "Kärlek, Harmoni, Partnerskap, Val",
         "Obalans, Ensidighet, Harmonibrist", "Ja", "tarot-lovers.jpg"],
    "The Chariot": 
        ["Motiverande Uppmuntran", "Vägledning, Kontroll, Viljestyrka, Beslutsamhet, Framgång, Säkerhet",
         "Kontrollbrist, Motsättning, Avsaknad Vägledning, Självdisciplin", "Ja", "tarot-chariot.jpg"],
    "Strength":
        ["Styrka och Mod", "Styrka, Mod, Fokus, Medkänsla, Övertygelse, Inflytande",
         "Självtvivel, Svaghet, Osäkerhet, Orkeslöshet, Råkänsla", "Ja", "tarot-strength.jpg"],
    "The Hermit":
        ["Utveckling genom Självrannsakan", "Visdom, Sökande i Själen, Lugn, Upplysning, Intuition, Vägledning",
         "Ensamhet, Isolering, Paranoia, Sorg, Överväldigande Rädsla", "Ja", "tarot-hermit.jpg"],
    "Wheel of Fortune":
        ["Tur", "Chans, Öde, Karma, Vändpunkt, Avslutade konflikter", 
         "Omvälvning, Otur, Ovälkomna Förändringar, Bakslag", "Ja", "tarot-wheeloffortune.jpg"],
    "Justice":
        ["Balans och Ordning", "Rättvisa, Integritet, Rättsliga Tvister, Orsak och Verkan, Livsläxa",
         "Orättvisa, Ohederlighet, Oansvarighet, Bedrägeri, Negativ Karma", "Neutral", "tarot-justice.jpg"],
    "The Hanged Man":
        ["Släpp Taget", "Att Släppa Taget, Offra, Reflektera, Osäkerhet, Uppvaknande",
         "Missnöje, Avstannande, Negativitet, Utan Lösning, Rädsla för uppoffring", "Kanske", "tarot-hangedman.jpg"],
    "Death":
        ["Början och Slut", "Slutet på en cykel, Övergångar, Ta Bort Överskott, Mäktig Rörelse, Beslut",
         "Ovilja att förändra, Rädsla för det nya, Medberoende, Negativa Mönster", "Ja", "tarot-death.jpg"],
    "Temperance":
        ["Måttfullhet och Tålamod", "Balans, Lagom, God Hälsa, Samarbete, Flitighet",
         "Obalans, Disharmoni, Förhastning, Överkonsumtion, Riskfullt beteende", "Ja", "tarot-temperance.jpg"],
    "The Devil":
        ["Illusioner", "Materiell Fokus, Materiella Ägodelar, Fången i Slaveri, Beroenden, Depression, Negativitet, Förräderi",
         "Bryta Beroenden, Självständighet, Återerövra Makt, Frihet", "Nej", "tarot-devil.jpg"],
    "The Tower":
        ["Förstörelse", "Hastig förändring, Frigivning, Plågsam Förlust, Tragedi, Uppenbarelse",
         "Motstå Förändring, Undvika Tragedi, Nära Ögat-Ögonblick, Fördröja det Oundvikliga", "Nej", "tarot-tower.jpg"],
    "The Star":
        ["Efter Regn kommer Solsken", "Hopp, Förnyelse, Kreativitet, Inspiration, Generositet, Läkande, Förändring",
         "Förtvivlan, Hopplöshet, Uttråkan, Negativitet, Oförmåga till kreativitet", "Ja", "tarot-star.jpg"],
    "The Moon":
        ["Starka Känslor och Fantasier", "Rädsla, Ångest, Förvirring, Vanföreställning, Risk, Sorg",
         "Övervinna rädsla, Känslomässig stabilitet, Finna sanningen, Övervinna ångest", "Nej", "tarot-moon.jpg"],
    "The Sun":
        ["Livet från den Ljusa Sidan", "Lycka, Fertilitet, Glädje, Optimism, Sanning, Flitighet",
         "Sorg, Pessimism, Lögner, Misslyckande, Framskjutning", "Ja", "tarot-sun.jpg"],
    "Judgement":
        ["Självreflektion", "Reflektion, Magkänsla, Bedömning, Uppvaknande, Pånyttfödelse, Förlåtelse",
         "Nedstämdhet, Självtvivel", "Neutral/Ja", "tarot-judgement.jpg"],
    "The World":
        ["Framgång och Prestation", "Harmoni, Slutförande, Resa, Enande, Integrering",
         "Ofullständighet, Genvägar, Förseningar, Tomhet", "Ja", "tarot-world.jpg"]
    }

wandCards = {
    "Ace of Cups":
        ["Kärlek", "Stagnation"],
    "Two of Cups":
        ["Ett kärleksengagemang", "Separation"],
    "Three of Cups":
        ["Växande, Läkande, Firande", "Förräderi"],
    "Four of Cups":
        ["Uttråkan", "Apati"],
    "Five of Cups":
        ["Olycklighet", "Psykiskt Läkande"],
    "Six of Cups":
        ["Dra nytta av Erfarenhet", "Sentimentalitet"],
    "Seven of Cups":
        ["Förvirring", "Illusion"],
    "Eight of Cups":
        ["Förändrade Känslor", "Dåligt Omdöme"],
    "Nine of Cups":
        ["En Dröm går i Uppfyllelse", "Självupptagenhet"],
    "Ten of Cups":
        ["Nöjdhet", "Isolering"],
    "Page of Cups":
        ["Vägledning", "Frustration"],
    "Knight of Cups":
        ["Älskvärdhet/Vänskap", "Tomhet"],
    "Queen of Cups":
        ["Omhändertagande/Insikt", "Avundsjuka/Otrohet"],
    "King of Cups":
        ["Problemlösning/Intuition", "Destruktivt Beteende"]
    }

pentacleCards = {
    "Ace of Pentacles": 
        ["Materiell Lycka", "Finansiell Förlust"],
    "Two of Pentacles":
        ["Soliditet/Säkerhet", "Pengaproblem"],
    "Three of Pentacles":
        ["Creativitet", "Idétorka"],
    "Four of Pentacles":
        ["Stabilitet/Självförtroende", "Begränsningar"],
    "Five of Pentacles":
        ["Svåra tider", "Girighet"],
    "Six of Pentacles":
        ["En Gåva", "Elakhet"],
    "Seven of Pentacles":
        ["Uthållighet", "Uppskjutande"],
    "Eight of Pentacles":
        ["Möjligheter", "Överbelastning"],
    "Nine of Pentacles":
        ["Ordning/Njutning", "Pengakris"],
    "Ten of Pentacles":
        ["Arv/Lycka", "Familjekonflikt"],
    "Page of Pentacles":
        ["Goda nyheter för pengar", "Oansvarighet"],
    "Knight of Pentacles":
        ["Säkerhet/Framsteg", "Passivitet/Ohederlighet"],
    "Queen of Pentacles":
        ["Generositet", "Girighet"],
    "King of Pentacles":
        ["Lösta Problem", "Korruption"]
    }

swordCards = {
    "Ace of Swords":
        ["Seger/Framgång", "Förlust"],
    "Two of Swords":
        ["Vapenvila", "Misstankar"],
    "Three of Swords":
        ["Hjärtesorg", "Kaos"],
    "Four of Swords":
        ["Återhämtning", "Sjukdom/Avbrott"],
    "Five of Swords":
        ["Nederlag", "Utsatthet"],
    "Six of Swords":
        ["Återfunnen Fred", "Tvingad Försening"],
    "Seven of Swords":
        ["Egendomsberövande", "Ohederlighet"],
    "Eight of Swords":
        ["Förnekande", "Självkritik"],
    "Nine of Swords":
        ["Lidande/Utsatthet", "Självuppoffring"],
    "Ten of Swords":
        ["Avslut", "Ruinering"],
    "Page of Swords":
        ["Intelligens", "Bus"],
    "Knight of Swords":
        ["Ett Slag", "Falsk Hjältedom"],
    "Queen of Swords":
        ["Elegans", "Hänsynslöshet"],
    "King of Swords":
        ["Ambition", "Grymhet"]
}

aceCards = {
    "Ace of Wands":
        ["Keativ framgång", "Försening"],
    "Two of Wands":
        ["En Pålitlig Partner", "Ojämlikhet"],
    "Three of Wands":
        ["Självuttryckande/Effektivitet", "Missförstående"],
    "Four of Wands":
        ["Tillfredsställelse", "Förskjutning"],
    "Five of Wands":
        ["Flitighet/Ett Prov", "Bedrägeri"],
    "Six of Wands":
        ["Triumf/Belöning", "Besvikelse"],
    "Seven of Wands":
        ["Uthållighet", "Svårigheter att kommunicera"],
    "Eight of Wands":
        ["Möjligheter", "Bedömningsförmåga"],
    "Nine of Wands":
        ["Lösningsförmåga", "Press"],
    "Ten of Wands":
        ["En Börda", "Självbedrägeri"],
    "Page of Wands":
        ["Försiktig Framgång", "Manipulering"],
    "Knight of Wands":
        ["Kreativitet/Framgång", "Oärlighet"],
    "Queen of Wands":
        ["Inspiration/Passion", "Opålitlighet"],
    "King of Wands":
        ["Heder/Medkänsla", "Fördom"]
}

allCards = [majorCards, wandCards, pentacleCards, swordCards, aceCards]

def drawMajor(n):
    drawnCards = []
    counter = 1

    while counter <= n:
        card_already_drawn = False

        card_name, card_attributes = random.choice(list(majorCards.items()))
        card_description = card_attributes[0]
        standing_attributes = card_attributes[1]
        laying_attributes = card_attributes[2]
        card_image = card_attributes[4]
        
        for card in drawnCards:
            if card_name == card[0]:
                card_already_drawn = True
        
        if not card_already_drawn:
            drawnCards.append([card_name, card_description, standing_attributes, laying_attributes, card_image])
            counter += 1
    
    return drawnCards