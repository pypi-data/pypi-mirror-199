.. include:: /../docs/shared/include/defs.rst
             
=======
Einkauf
=======

.. contents::
   :depth: 1
   :local:



Einkaufsrechnungen erfassen
===========================

Um eine neue EKR zu erfassen, wähle im Hauptmenü
:menuselection:`Buchhaltung --> Einkauf --> Einkaufsrechnungen` und
klicke dann auf |insert| um eine neue Rechnung einzufügen.

Der Partner einer EKR ist der Lieferant. Das ist üblicherweise eine
Firma oder Organisation, kann aber potentiell auch eine Einzelperson
oder ein Haushalt sein.

Das Buchungsdatum ist fast immer das gleiche wie das
Rechnungsdatum. Ausnahme: Wenn eine Rechnung n einem anderen
Kalenderjahr gebucht wird, dann muss als Buchungsdatum der 01.01. oder
31.12. des Buchungsjahres genommen werden.

In Total inkl. MWSt. gib den Gesamtbetrag der Rechnung ein. Lino wird
diesen Betrag ggf im folgenden Bildschirm verteilen.

Tipp : tippe :kbd:`Ctrl-S`, um dieses Dialogfenster ohne Maus zu
bestätigen.

Hier hat Lino den Gesamtbetrag so gut es ging aufgeteilt. Im Idealfall
kannst du hier auf "Registriert" klicken, um die Rechnung zu
registrieren. Und dann wieder auf um die nächste Rechnung einzugeben.

Alternativ kannst du Konto, Analysekonto, MWSt-Klasse und Beträge
manuell für diese eine Rechnung ändern.

Lino schaut beim Partner nach, welches Konto Einkauf dieser Partner
hat. Falls das Feld dort leer ist, nimmt Lino das Gemeinkonto
„Wareneinkäufe“. Das MWSt-Regime der Rechnung nimmt Lino ebenfalls vom
Partner. Beide Felder kannst du in den Partnerstammdaten nachschauen
gehen, indem du auf die Lupe (|search|) hinterm Feld „Partner“
klickst. Dort kannst du diese beiden Felder dann für alle zukünftigen
Rechnungen festlegen.

Analysekonten
=============

Analysekonten und Generalkonten sind zwei unterschiedliche
Klassierungen der Kosten. Der Buchhalter interessiert sich nur für die
G-Konten und weiß von den A-Konten nichts. Der VWR dagegen
interessiert sich eher für die A-Konten.

Über :menuselection:`Konfigurierung --> Buchhaltung --> Konten` kann
man den Kontenplan (d.h. die Liste aller Generalkonten) sehen und
ggf. verändern.

Pro Generalkonto kann man sagen :

- Braucht AK : wenn angekreuzt, dann muss für Buchungen auf dieses
  Konto auch ein A-Konto angegeben werden. Wenn nicht angekreuzt, dann
  darf für Buchungen auf dieses Konto kein A-Konto angegeben werden.
  
- Analysekonto : welches A-Konto Lino vorschlagen soll, wenn man
  dieses Generalkonto für eine Buchung auswählt.
  
NB das A-Konto des Generalkontos ist lediglich der Vorschlag
bzw. Standardwert. Man kann das A-Konto einer individuellen Buchung
manuell dennoch ändern.

Pro Generalkonto kannst du das Analysekonto angeben, das Lino
vorschlagen soll, wenn du eine neue Einkaufsrechnung (EKR)
eingibst. In der EKR kannst du dann immer noch ein anderes AK
auswählen. Du kannst das AK im Generalkonto auch leer lassen (selbst
wenn "Braucht AK" angekreuzt ist). Das bedeutet dann, dass Lino in der
EKR keinen Vorschlag machen soll. Dann ist man sozusagen gezwungen,
bei jeder Buchung zu überlegen, welches AK man auswählt.

.. rubric:: Tipps

Pro Partner kannst Du das Konto Einkauf festlegen. Dieses Konto trägt
Lino dann automatisch als Generalkonto in Einkaufsrechnungen von
diesem Partner ein.

Nach Ändern des Generalkontos in einer Rechnungszeile setzt Lino immer
das Analysekonto, selbst wenn dieses Feld schon ausgefüllt war.

