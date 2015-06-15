
import POStagger_text

testText = "De piloten kwamen er pas achter toen het vliegtuig weer veilig op het vliegveld geland was \nDaar ontdekten ze dat er twee koffers ontbraken\n\nTurbulentie\nTijdens de vlucht hoorden de piloten wel een geluid, maar ze dachten dat het gewoon turbulentie was\nDat de complete achterklep ontbrak, hadden ze niet verwacht\nEr was voor Bono, zijn drie vrienden en het personeel aan boord geen crashgevaar, omdat de luchtdruk in de cabine niet weg kon vallen\nDeze was namelijk niet verbonden met het bagageruim\nDe luchtvaartautoriteiten gaan nu het incident onderzoeken"

print(POStagger_text.getPOStags(testText))
