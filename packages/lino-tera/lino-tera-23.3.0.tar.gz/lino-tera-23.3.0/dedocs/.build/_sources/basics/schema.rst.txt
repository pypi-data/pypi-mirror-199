=================
Datenbankstruktur
=================

.. contents::
   :depth: 1
   :local:



Patienten, Akten und Einschreibungen
====================================

Anders als TIM unterscheidet Lino zwischen "Patienten" und "Akten".
Die Akten eines gleichen Patienten wurden in TIM über ihre Erstanfrage
verknüpft.  Beim Datenimport wurde das größtenteils automatisch
erkannt.

.. Statt Akte könnte man eigentlich auch "Therapie" sagen. Das wäre
   linguistisch korrekter, aber auch länger.  Schon in TIM hieß es
   "Akten", und daran habt ihr euch gewöhnt.

Ein **Patient** ist eine physische Person und wird nur einmal erfasst. Ein
Patient kann an mehreren *Akten* teilnehmen, im Laufe der Jahre oder
zeitgleich.  Eine *Einschreibung** ist die Tatsache, dass ein bestimmter
Patient an einer bestimmten Akte teilnimmt.

Patienten werden eher im Sektretariat erstellt und verwaltet, Akten
eher durch den Therapeuten.

Es gibt wie in TIM **drei Arten von Akten**: Einzeltherapien (ET),
Lebensgruppen (LG) und Therapeutische Gruppen (TG).  Jede Akte kann unabhängig
ihrer Art mehrere Teilnehmer haben.  Bei ET ist das eher die Ausnahme (aber
theoretisch möglich), bei LG sind es eher wenige und konstante Teilnehmer, bei
TG können es viele sein und die Teilnehmerliste kann sich ändern.

Merke: Eine Einzeltherapie wird in Lino behandelt wie eine Therapie mit nur
einer Einschreibung.

Akten
=====

Der **Zahler** einer Akte in TIM wird in Lino der **Rechnungsempfänger**
genannt. Wenn das Feld *Zahler* in TIM leer war, dann steht in Lino der Patient
bzw. der Haushalt als *Rechnungsempfänger*.


Dienstleistungen sind Termine
=============================

Das, was in TIM "Dienstleistung" hieß, heißt in Lino "Termin". Ein Termin ist,
wenn ein Therapeut (oder mehrere) sich mit einem (oder mehreren) Patienten
trifft.

Pro Termin muss man die wie in TIM die *Dienstleistungsart* eingeben.

Pro Termin gibt es ein Feld *Beschreibung*. Das kann verwendet werden für
Informationen zur Terminplanung, die auch das Sekretariat sehen darf und soll.

Lino bezeichnet Termine machmal auch als **Kalendereintrag**. Diese
Unterscheidung wird erst wichtig, wenn wir den Kalender auch mal zur Planung
benutzen.  Dann kommen Kalendereintragsarten wie "Feiertage" oder "Versammlung"
hinzu.


Notizen
=======

Therapeutische Berichte, die Du mit Kollegen teilen willst, solltest
Du als **Notiz** erfassen.

Notizen sind vertraulich und können im Sekretariat nicht gesehen werden.

Notizen beziehen sich immer auf eine und eine einzige Akte. In TIM war das zum
Teil anders.


Partner
=======

Als **Partner** bezeichnet Lino jede physische oder juristische Person.  Ein
Patient ist ein Partner, eine Firma ist ein Partner, ein Haushalt ist ein
Partner, auch jeder Therapeut ist ein Partner.

Jeder Partner kann potentiell eine Rechnung kriegen oder schicken.
