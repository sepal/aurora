# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from Course.models import Course
from Faq.models import Faq


class Command(BaseCommand):
    help = 'Populates database with demo data'

    def handle(self, *args, **options):
        import_faq()


def import_faq():
	# create courses "GSI" and "HCI"
    print('getting courses')
    gsi = Course.objects.get(short_title='gsi');
    hci = Course.objects.get(short_title='hci');
    # add faq
    print('adding faq')
    faqs = [
        (
            Faq(
                question="Wie unterscheidet sich der Modus zu dem des Vorjahres?",
                answer="So gut wie gar nicht. Aurora wurde überarbeitet, viele Bugs wurden behoben, und es wurden einige "
                       "kleine Verbesserungen implementiert. Wir haben aber noch Pläne, über das Semester hinweg ein paar "
                       "neue Dinge zu versuchen.",
                order=0
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Kann ich einfach irgendwelche Challenges machen, bis ich genug Punkte habe?",
                answer="Nein. Sie müssen für eine positive Note aus jeder der vier Kategorien (s.u.) mindestens "
                       "eine Challenge absolvieren. Ansonsten steht Ihnen frei, was Sie wann machen.",
                order=1
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Was sind die 4 Kategorien in BHCI?",
                answer="<ul><li>Kategorie 1: User-centered design + design basics (B1cX)</li>"
                       "<li>Kategorie 2: Methoden (B2cX)</li>"
                       "<li>Kategorie 3: psycholog. Grundlagen, Evaluation (B3cX)</li>"
                       "<li>Kategorie 4: Prototyping, Beyond the desktop (B4cX)</li></ul>",
                order=2
            ),
            [hci]
        ),
        (
            Faq(
                question="Was sind die 4 Kategorien in GSI?",
                answer="<ul><li>Kategorie 1: Praxis (G1cX)</li>"
                       "<li>Kategorie 2: IT-Branche (G2cX)</li>"
                       "<li>Kategorie 3: Ideen (G3cX)</li>"
                       "<li>Kategorie 4: Gesellschaft (G4cX)</li></ul>",
                order=2
            ),
            [gsi]
        ),
        (
            Faq(
                question="Wann ist die Deadline für (eine/diese/alle) Challenges?",
                answer="Für eine positive Note müssen Sie bis Ende des Semesters (Fr 3.7., 23:59) ausreichend Punkte "
                       "gesammelt haben, und aus jeder Kategorie (s.o.) mindestens eine Challenge geschafft haben. "
                       "Punkte bekommen Sie für fertiggestellte Challenges, aber zB. auch für ausgezeichnete Kommentare "
                       "bei den Folien. Beachten Sie jedoch, dass Sie nach dem Abgeben einer Challenge (also des Final "
                       "Tasks) 11 Tage warten müssen (ab 22.6.: 7 Tage), bevor Sie wieder einen Final Task einreichen "
                       "können!",
                order=3
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Was kann ich machen, wenn die Bewertung meiner Arbeit nicht meinen Erwartungen entspricht?",
                answer="Sie können einen Kommentar zu ihrer Arbeit formulieren, in dem Sie zb. eine Frage stellen, "
                       "oder ihre Arbeit noch einmal besser erklären. Damit wird ihre Arbeit intern markiert und für "
                       "uns noch einmal sichtbar. Ihr Kommentar wird jedenfalls beantwortet werden, auch wenn es "
                       "manchmal etwas dauert.",
                order=4
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Ab wann werde ich bewertet?",
                answer="Sobald Sie eine Challenge abgeschlossen haben, wird für Sie am Ende des Semesters ein "
                       "Zeugnis ausgestellt.",
                order=5
            ),
            [hci,gsi]
        ),
        (
            Faq(
                question="Wie sind die Bewertungskategorien am Ende jedes Reviews zu verstehen?",
                answer='Siehe <a href="http://igw.tuwien.ac.at/aurora/aurora_reviews.pdf">Zum Schreiben von Reviews</a>',
                order=6
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Wie ist das jetzt mit den Punkten?",
                answer="Sie <b>müssen</b> Challenges im Umfang von mind. 60 Punkten komplett abarbeiten. Die Punkte sind "
                       "bei der Beschreibung von Challenges explizit angeführt (zB. Sie können für Ihre Arbeit hier bis "
                       "zu 10 Punkten bekommen) Wir bewerten eine Challenge, wenn der final Task abgegeben wurde. Für "
                       "Mängel bei einzelnen Tasks ziehen wir Punkte vom erreichbaren Maximum ab, wobei die relative "
                       "Wertigkeit der Tasks in der Taskbeschreibung in % angegeben ist. Diese Bewertung erfolgt unabhängig "
                       "von den Review-Ergebnissen, die Sie bekommen haben. Die Summe der Punkte, die Sie für alle "
                       "Challenges bekommen, bestimmt Ihre Note nach dem oben angegebenen Notenspiegel.",
                order=7
            ),
            [hci, gsi]
        ),
    ]
    for (faq, courses) in faqs:
        print("Adding faq")
        faq.save()
        for c in courses:
            faq.course.add(c)