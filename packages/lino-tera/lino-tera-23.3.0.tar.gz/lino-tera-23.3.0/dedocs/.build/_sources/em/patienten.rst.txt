.. doctest tera_de/em/patienten.rst
.. include:: /../docs/shared/include/defs.rst


.. init
    >>> from lino import startup
    >>> startup('lino_book.projects.lydia.settings.doctests')
    >>> from lino.api.doctest import *
    >>> from django.db import models

=========
Patienten
=========

Einen neuen Patienten erfassen
==============================

Um einen neuen Patienten zu erfassen:

- Hauptmenü :menuselection:`Kontakte --> Patienten`

- Nachprüfen, ob er nicht doch schon existiert.  Siehe :doc:`/basics/suchen`.

- Klicke auf |insert| in der Werkzeugleiste.


Datenfelder Patienten
=====================

Im Panel **Einschreibungen in Akten** eines Patienten kann man die Akten sehen,
an denen der Patient teilnimmt.

Hier kann man auch auf das |insert| klicken. Lino zeigt dann das Dialogfenster
"Einfügen in Einschreibungen in Akten" mit folgenden Feldern:

- Layout (unwichtig, schreibgeschützt)

- Akte : in welcher Akte der Patient eingeschrieben werden soll. Entweder eine
  bestehende therapeutische Gruppe oder Lebensgruppe auswählen, oder das Feld
  leer lassen, um eine Zeinzeltherapie zu erstellen.

- Bemerkung : unwichtig
- Datum der Anfrage : wann die Einschreibung gemacht wurde

- Autor : wer die Einschreibung gemacht hat. NB der Primärbegleiter der Akte
  kann ein anderer sein.

