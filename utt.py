#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

data = {}

data['names'] = {'Ballade an der Reichstag 1': 'ballade1',
                 'Ballade an den Reichstag 2': 'ballade2',
                 'Faust Auszug': 'faust',
                 'Egmont Auszug': 'egmont',
                 'Ballade von der Mäusefrau': 'ballademaus',
                 'Gegen die Objektiven': 'brecht_gegendieobjektiven'
                 }

data['examples'] = {
    'Ballade an der Reichstag 1': ('Als man den Galgen mir hat zudiktiert,\n'
        'Da hab ich an den Reichstag appeliert.\n'
        'Denn jedes Tier, das hier auf Erden kraucht,\n'
        'Hält seinen Kopf nicht zum Vergnügen still,\n'
        'Wenn ihm ein Bösewicht ans Leder will.\n'
        'Da wirst du ganz gehörig angefaucht.\n'
        'Und ich?! Ich soll in diesem kalten,\n'
        'Verfluchten Hundeloch den Schnabel halten?!',
        'Als man den Gal -gen mir hat zu -dik -tiert, '
        'Da hab ich an den Reichs -tag a -ppe -liert. '
        'Denn je -des Tier, das hier auf Er -den kraucht, '
        'Hält sei -nen Kopf nicht zum Ver -gnu ̈-gen still, '
        'Wenn ihm ein Bö -se -wicht ans Le -der will. '
        'Da wirst du ganz ge -hö -rig an -ge -faucht. '
        'Und ich?! Ich soll in die -sem kal -ten, '
        'Ver -fluch -ten Hun -de -loch den Schna -bel hal -ten?!'),
    'Ballade an den Reichstag 2': ('Und hätte ich im Kopf nur Häcksel drin!\n'
        'Und wär ich dümmer noch, als ich schon bin!\n'
        'Den Schädel soll man mir in Stücke haun,\n'
        'Wenn ich nicht mit dem letzten Atemzug\n'
        'noch protestier, dass man mich grundlos schlug!\n'
        'Und wenn der Henker winkt und wie ein Zaun\n'
        'Soldaten ihre Eisenlanzen halten,\n'
        'Soll ich da wie ein Stein den Schnabel halten?',
        'Und hä-tte ich im Kopf nur Häck-sel drin! '
        'Und wär ich dümm-er noch, als ich schon bin! '
        'Den Schä-del soll man mir in Stü-cke haun, '
        'Wenn ich nicht mit dem letz-ten A-tem-zug '
        'noch pro-tes-tier, dass man mich grund-los schlug! '
        'Und wenn der Hen-ker winkt und wie ein Zaun '
        'Sol-da-ten ih-re Ei-sen-lan-zen hal-ten, '
        'Soll ich da wie ein Stein den Schna-bel hal-ten?'),
    'Faust Auszug': ('In diesem Sinne kannst du‘s wagen.\n'
        'Verbinde dich! Du sollst in diesen Tagen\n'
        'Mit Freuden meine Künste sehen.\n'
        'Ich gebe dir, was noch kein Mensch gesehn.',
        'In die-sem Sinn-e kannst du‘s wa-gen. '
        'Ver-bin-de dich! Du sollst in die-sen Ta-gen '
        'Mit Freu-den mei-ne Kün-ste seh-en. '
        'Ich ge-be dir, was noch kein Mensch ge-sehn.'),
    'Egmont Auszug': ('Es war mein Blut und vieler Edlen Blut.\n'
        'Nein, es ward nicht umsonst vergossen.\n'
        'Schreitet durch!\n'
        'Braves Volk! Die Siegesgöttin führt dich an!\n'
        'Und wie das Meer durch eure Dämme bricht,\n'
        'so brecht, so reißt den Wall der Tyrannei zusammen\n'
        'und schwemmt ersäufend sie von ihrem Grunde,\n'
        'den sie sich anmaßt, hinweg!',
        'Es war mein Blut und vie-ler Ed-len Blut. '
        'Nein, es ward nicht um-sonst ver-goss-en. '
        'Schrei-tet durch! '
        'Bra-ves Volk! Die Sie-ges-gött-in führt dich an! '
        'Und wie das Meer durch eu-re Dämm-e bricht, '
        'so brecht, so reißt den Wall der Ty-rann-ei zu-samm-en '
        'und schwemmt er-säuf-end sie von ih-rem Grun-de, '
        'den sie sich an-maßt, hin-weg!'),
    'Ballade von der Mäusefrau': ('Im milden Licht der Winternacht\n'
        'Hab ich mich zu den Mäusen aufgemacht.\n'
        'Du aber fragst: Warum denn nur?\n'
        'Hör zu! Es ist kein Tier so klein,\n'
        'Dass nicht von dir ein Bruder könnte sein.',
        'Im mil-den Licht der Win-ter-nacht '
        'Hab ich mich zu den Mäu-sen auf-ge-macht. '
        'Du a-ber fragst: Wa-rum denn nur? '
        'Hör zu! Es ist kein Tier so klein, '
        'Dass nicht von dir ein Bru-der könn-te sein.'),
    'Gegen die Objektiven': ('Wer mit Gewalt vorgeht, '
        'darf die Gewalt nicht beschuldigen!\n'
        'Ach, Freunde, warum so feindlich?\n'
        'Sind wir eure Feinde; die wir Feinde des Unrechts sind?\n'
        'Wenn die Kämpfer gegen das Unrecht besiegt sind,\n'
        'hat das Unrecht doch nicht recht!',
        'Wer mit Ge-walt vor-geht, '
        'darf die Ge-walt nicht be-schul-digen! '
        'Ach, Freun-de, wa-rum so feind-lich? '
        'Sind wir eu-re Fein-de; die wir Fein-de des Un-rechts sind? '
        'Wenn die Käm-pfer ge-gen das Un-recht be-siegt sind, '
        'hat das Un-recht doch nicht recht!')
}

data['welcome'] = {
    'welcome_text': 'Willkommen zur Ernst Buschs Spielwiese. Wollen Sie auch mal was aufnehmen?',
    'instructions': 'Drücken Sie auf "Aufnahme" und suchen Sie sich einen der Sätze aus. Sprechen Sie diesen Satz'
                    'in das Mikrofon. Danach können Sie auf "Analyse" gehen, um Ihre Aufnahme graphisch sichtbar zu machen.'
}
