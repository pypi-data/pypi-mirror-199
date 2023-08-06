.. doctest tera_de/th/barzahlungen.rst
.. include:: /../docs/shared/include/defs.rst
.. init

    >>> from lino import startup
    >>> startup('lino_book.projects.lydia.settings.doctests')
    >>> from lino.api.doctest import *
    >>> from django.db import models

============
Barzahlungen
============

Ein Therapeut, der von Klienten Geld kassiert, muss seine eigene
Bargeldkasse führen.  Dazu bietet :ref:`tera` ein vereinfachtes
Verfahren, bei dem jede Einnahme an den jeweiligen Termin gekoppelt
ist.

Zunächst musst du dir ein "Kassenbuch eröffnen", indem du das Feld
*Kassenbuch** in deinen Benutzereinstellungen  ausfüllst (Siehe
:doc:`/basics/settings` ).

Im Feld **Betrag** eines Termins oder einer Anwesenheit trägst du den Betrag
ein, den du vom Patienten kassiert hast.

Bei Einzeltherapien und Lebensgruppen steht dieses Feld auf dem
*Termin* (im oberen Bildschirmteil), bei therapeutischen Gruppen auf
der Anwesenheit (im unteren Bildschirmteil).  Bei therapeutischen
Gruppen steht auf dem Termin die Summe aller kassierten Beträge.

Es gibt kein Feld **Zahlart**, weil es sich immer um Barzahlung handelt, wenn
ein Betrag kassiert wurde.

Man muss den Betrag jedesmal selber manuell eintragen.  (Frage: wie könnte man
das vereinfachen? Lino soll ja nicht bei jeder Sitzung einen Betrag eintragen.)

Man kann den Betrag auch rückwirkend ändern solange der Termin nicht schon
fakturiert wurde.

Im Menü :menuselection:`Kalender --> Meine Kassenrolle` kannst du alle Termine
im letzten Monat sehen, bei denen du etwas kasssiert hast.

>>> show_menu_path(rt.models.cal.MyCashRoll, language="de")
Kalender --> Meine Kassenrolle

Und wie sieht das in der Buchhaltung aus?

Nehmen wir einen einfachen Fall. Ein
Klient hatte eine Sitzung, und hat diese bar bezahlt (20€). Der Therapeut hat
das im Termin eingegeben. Dann druckt die Buchhaltung die Rechnungen aus. Der
Klient kriegt eine Rechnung über 20€, auf der steht, dass sie schon bezahlt
ist. In der Buchhaltung kreditiert die Rechnung das Konto "Umsatz Therapeuten"
um 20€, und ein Konto "Durch Therapeuten kassiert" wird debitiert. Und wenn ein
Therapeut sein Bargeld in die Kasse bringt, wird dieses Konto kreditiert.

Unklar ist mir noch, wie die Abrechnungen der Therapeuten aussehen und
verbucht werden sollen? Der Therapeut muss ja regelmäßig eine
Abrechnung machen. Das ist bisher in TIM ein Dokument, auf dem die
kassierten Beträge stehen. Wenn der Therapeut das Dokument bestätigt,
deklariert er damit, dass er jetzt die Summe in die zentrale
Bargeldkasse zahlen muss.

Und wie werden Bancontact-Zahlungen erfasst? Geht der Therapeut mit
dem Klienten zum Sekretariat und tippt den Betrag dort ein und
vergewissert sich, ob er bezahlt? Oder macht das die Sekretärin?
