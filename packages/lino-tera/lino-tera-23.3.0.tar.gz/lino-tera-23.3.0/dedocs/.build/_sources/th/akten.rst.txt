.. include:: /../docs/shared/include/defs.rst
             
=====             
Akten
=====

Akten anlegen
=============

Einzeltherapie
==============

- :menuselection:`Akten --> Meine Patienten` und gehe auf den Patienten.
- Klicke auf den Button |insert| im Panel **Einschreibungen in Akten**.
  Lino öffnet das Fenster **Einfügen in Einschreibungen in Akten**
- :kbd:`Ctrl+S` um das Fenster zu bestätigen.

Du brauchst keine Akte anzugeben, denn die wird automatisch erstellt mit dem
Namen des Patienten.

Lebensgruppe
============

- :menuselection:`Kontakte--> Haushalte` und gehe auf den Haushalt, der
  Rechnungsempfänger sein soll.
- Klicke auf den Button |insert| im Panel **Rechnungsempfänger in Akten**.
  Lino öffnet das Fenster **Einfügen in Rechnungsempfänger in Akten**
- Im Feld **Aktenart** wähle "Lebensgruppen"
- :kbd:`Ctrl+S`  um das Fenster zu bestätigen.



Meine Akten
===========

Wähle im Hauptmenü :menuselection:`Akten --> Meine Akten`, um alle
Akten zu sehen, deren verantworlicher Therapeut du bist.

Jede Akte hat einen einzigen verantwortlichen Therapeuten.  Wenn
dieser wechselt, kann man entweder eine neue Akte starten oder die
bestehende verändern.

Hier kannst du z.B. eine neue Akte einfügen (Button |insert| in der
Werkzeugleiste) oder die Akte aussuchen, mit der du arbeiten möchtest.


.. Die Tabelle "Meine Akten" gibt es in zwei Versionen: für Therapeuten
   und für das Sekretariat.

Datenfelder einer Akte
======================

Die Angaben einer Akte sind in fünf Reiter unterteilt

- Allgemein:

  - Referenz : die aus TIM importierte Aktennummer

  - Bezeichnung : der Name der Akte. Kann manuell angepasst werden. Bei ET
    steht hier der Name des Patienten, bei LG der des Rechnungsempfängers.

  - Rechnungsempfänger : wer die Rechnungen bezahlt. Das kann der Patient
    selber, ein Haushalt oder eine Organisation sein.

  - Der Verwalter einer Therapie kann ein anderer sein als der
    Therapeut. Zum Beispiel für Therapien, deren Termine durch das
    Sekretariat verwalten werden.

  - Aktenart : ET, LG oder TG

  - ID : die interne Aktennummer

  - Workflow :  Entwurf, Inaktiv oder Abgeschlossen. wurde so gut es geht aus
    TIM importiert. Für neue Akten steht es auf Entwurf. Akten in Entwurf werden
    an manchen Stellen nicht angezeigt.

  - Teilnehmer : siehe `Teilnehmer einer Akte`_

- Therapie

  - Bereich
  - Vermittler : ist noch nicht richtig importiert.
  - Verpflichend
  - Übersetzung
  - Beendigungsgrund

  - Interessen : auf |insert| klicken, um ein neues Thema hinzuzufügen. Auf
    |eject| klicken, um die Dadten in einem eigenen Fenster zu öffnen (z.B. Interessen löschen)
  - Notizen :  auf |insert| klicken, um eine neue Notiz hinzuzufügen.
    Auf den blauen Text klicken, um eine Notiz im Detail anzuzeigen.
    Auf
    |eject| klicken, um die Dadten in einem eigenen Fenster zu öffnen (z.B. Notiz löschen, ausdrucken)


- Termine

  - Auf |lightning| in der Werkzeugliste klicken, um Terminvorschläge automatisch zu erstellen.

  - **Wiederholung** : auf "täglich" setzen (und einen oder mehrere Wochentage
    ankreuzen), damit Lino automatische Termine erstellt.

  - **Termine generieren bis** : bis zu welchem Datum Lino Termine vorschlagen
    soll.

  - **Enddatum:** : sollte immer leer sein.

  - **Raum** : zur Zeit nicht benutzt.

  - **... alle** : hier normalerweise 1 eintragen.  2 in Kombination mit
    "wöchentlich" hiesse z.B., dass alle zwei Wochen ein Termin vorgeschlagen
    werden soll.

- Fakturierung

  - Krankenversicherung : welche Krankenkasse
  - Pauschale : "Jeder Termin" "Max. 20 pro Monat"
  - Fakturierungen : welche Rechnungen bereits ausgestellt wurden
  - Bestehende Auszüge : (kommt wahrscheinlich raus)

- Mehr
  - Bemerkung
  - Aufgaben : (kommt vielleicht raus)

Der **Rechnungsempfänger** einer Akte ist der Partner, der die
Rechnungen kriegt und bezahlen muss.  Das kann eine Person, eine
Organisation oder ein Haushalt sein.  Dieses Feld kann leer sein,
z.B. in therapeutischen Gruppen. In diesem Fall sind die einzelnen
Teilnehmer Rechnungsempfänger.


Teilnehmer einer Akte
=====================

Die beiden Buttons |insert| und 👤 fügen einen neuen Teilnehmer hinzu. Bei 👤
steht die Teilnehmerrolle auf "Cotherapeut" (das ist der einzige Unterschied
zwischen den beiden Buttons)

- Rolle : leer bedeutet "Patient".

  In Akten mit mehr als einem Therapeuten müssen die Therapeuten
  sich einigen, wer in Lino der Verantwortliche ist.  Die anderen
  Therapeuten stehen als Cotherapeuten in der Liste der Teilnehmer.




