# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date, timedelta

import random
import traceback
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from AuroraUser.models import AuroraUser
from Course.models import *
from Challenge.models import Challenge
from Elaboration.models import Elaboration
from Stack.models import Stack, StackChallengeRelation
from Review.models import Review
from ReviewQuestion.models import ReviewQuestion
from Slides.models import *
from Comments.models import Comment, CommentsConfig
from Notification.models import Notification
from Faq.models import Faq
from AuroraProject.settings import STATIC_ROOT
import os
from django.core.files import File
from PlagCheck.tests import PlagcheckTestData


class Command(BaseCommand):
    help = 'Populates database with demo data'

    def handle(self, *args, **options):
        populate_demo_data()


def populate_demo_data():
    try:
        with transaction.atomic():
            print("Starting transaction...")
            import_data()

    except Exception as e:
        traceback.print_exc()
        print("Caught error during transaction: %s" % e)
        print("Database has rolled back the transaction!")
    print("All Done!")


def import_data():
    CommentsConfig.setup()

    number_of_users = 50
    number_of_tutors = 5
    users = []
    dummy_users = []
    tutors = []

    for i in range(number_of_users):
        print("adding student %s of %s" % (i, number_of_users))
        username = "s%s" % i
        user = AuroraUser(username=username)
        user.email = '%s@student.tuwien.ac.at' % username
        user.first_name = 'Firstname_%s' % username
        user.last_name = 'Lastname_%s' % username
        user.nickname = 'Nickname_%s' % username
        user.matriculation_number = "{0:0=2d}".format(i) + ''.join(["%s" % random.randint(0, 9) for num in range(0, 5)])
        user.is_staff = False
        user.is_superuser = False
        password = username
        user.set_password(password)
        user.save()
        users.append(user)
    s0 = users[0]

    # create the three dummy users for jumpstarting the peer review process
    for i in range(4):
        print("adding dummy user %s of %s" % (i, 3))
        username = "d%s" % i
        dummy_user = AuroraUser(username=username)
        dummy_user.email = '%s@student.tuwien.ac.at' % username
        dummy_user.first_name = 'Firstname_%s' % username
        dummy_user.last_name = 'Lastname_%s' % username
        dummy_user.nickname = 'Nickname_%s' % username
        dummy_user.is_staff = True
        dummy_user.is_superuser = False
        password = username
        dummy_user.set_password(password)
        dummy_user.save()
        dummy_users.append(dummy_user)
    d1 = dummy_users[0]
    d2 = dummy_users[1]
    d3 = dummy_users[2]
    d4 = dummy_users[3]

    # adding tutors
    for i in range(number_of_tutors):
        print("adding tutor %s of %s" % (i, number_of_tutors))
        username = "t%s" % i
        tutor = AuroraUser(username=username)
        tutor.email = '%s@student.tuwien.ac.at' % username
        tutor.first_name = 'Firstname_%s' % username
        tutor.last_name = 'Lastname_%s' % username
        tutor.nickname = 'Nickname_%s' % username
        tutor.is_staff = True
        tutor.is_superuser = False
        password = username
        tutor.set_password(password)
        tutor.save()
        print("***tutor username: %s" % tutor.username)
        tutors.append(tutor)

    # create an admin user with password amanaman
    print('adding superuser')
    username = "amanaman"
    amanaman = AuroraUser(username=username)
    amanaman.first_name = 'Firstname_%s' % username
    amanaman.last_name = 'Lastname_%s' % username
    amanaman.nickname = 'Nickname_%s' % username
    amanaman.set_password(username)
    amanaman.is_staff = True
    amanaman.is_superuser = True
    amanaman.save()

    # hagrid staff user
    print('adding staff')
    username = "hagrid"
    superuser = AuroraUser(username=username)
    superuser.first_name = 'Firstname_%s' % username
    superuser.last_name = 'Lastname_%s' % username
    superuser.nickname = 'Nickname_%s' % username
    superuser.set_password(username)
    superuser.is_staff = True
    superuser.is_superuser = False
    superuser.save()


    # create courses "GSI" and "HCI"
    print('adding course gsi')
    gsi = Course(
        title='Gesellschaftliche Spannungsfelder der Informatik',
        short_title='gsi',
        description='GSI Description',
        course_number='123.456',
        start_date=date.today() - timedelta(days=100),
        end_date=date.today() + timedelta(days=100),
    )
    gsi.save()

    print('adding course hci')
    hci = Course(
        title='Human Computer Interaction',
        short_title='hci',
        description='HCI Description',
        course_number='123.457',
        start_date=date.today() - timedelta(days=100),
        end_date=date.today() + timedelta(days=100),
    )
    hci.save()

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
                       "eine Challenge absolvieren. Ansonsten steht Ihnen frei, was sie wann machen.",
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
                answer="Für eine positive Note müssen sie bis Ende des Semesters (Fr 3.7., 23:59) ausreichend Punkte "
                       "gesammelt haben, und aus jeder Kategorie (s.o.) mindestens eine Challenge geschafft haben. "
                       "Punkte bekommen sie für fertiggestellte Challenges, aber zB. auch für ausgezeichnete Kommentare "
                       "bei den Folien. Beachten sie jedoch, dass sie nach dem Abgeben einer Challenge (also des Final "
                       "Tasks) 11 Tage warten müssen (ab 22.6.: 7 Tage), bevor sie wieder einen Final Task einreichen "
                       "können!",
                order=3
            ),
            [hci, gsi]
        ),
        (
            Faq(
                question="Was kann ich machen, wenn die Bewertung meiner Arbeit nicht meinen Erwartungen entspricht?",
                answer="Sie können einen Kommentar zu ihrer Arbeit formulieren, in dem sie zb. eine Frage stellen, "
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
                answer="Sobald sie eine Challenge abgeschlossen haben, wird für sie am Ende des Semesters ein "
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
                       "bei der Beschreibung von Challenges explizit angeführt (zB. »Sie können für Ihre Arbeit hier bis "
                       "zu 10 Punkten bekommen«) Wir bewerten eine Challenge, wenn der final Task abgegeben wurde. Für "
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


    # create course-user relations
    print('adding course-user relations')
    CourseUserRelation(course=gsi, user=amanaman).save()
    CourseUserRelation(course=hci, user=amanaman).save()
    CourseUserRelation(course=gsi, user=superuser).save()
    CourseUserRelation(course=hci, user=superuser).save()

    for tutor in tutors:
        CourseUserRelation(course=gsi, user=tutor).save()
        CourseUserRelation(course=hci, user=tutor).save()
        Notification(user=tutor, course=gsi, text="Welcome to GSI!").save()
        Notification(user=tutor, course=hci, text="Welcome to HCI!").save()

    for user in users:
        CourseUserRelation(course=gsi, user=user).save()
        CourseUserRelation(course=hci, user=user).save()
        Notification(user=user, course=gsi, text="Welcome to GSI!").save()
        Notification(user=user, course=hci, text="Welcome to HCI!").save()


    # create challenges
    print('adding challenges')
    challenge_1 = Challenge(id=1,
                            title='meine meinung',
                            subtitle='meine meinung',
                            description='Gehen Sie nach derstandard.at, suchen Sie einen beliebigen Artikel und posten Sie den Text dieses Artikels hier.',
                            accepted_files='',
                            course=gsi,
                            points=15,
    )
    challenge_1.image.save('1.png', File(open(os.path.join(STATIC_ROOT, 'img', '1.png'), 'rb')))
    challenge_1.save()

    ReviewQuestion(challenge=challenge_1, order=1, text='In wie fern stellt der gepostete Artikel einen Beitrag zur Entwicklung der Gesellschaft dar?').save()
    ReviewQuestion(challenge=challenge_1, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_1, order=3, text="Anmerkungen an das LVA-Team:", visible_to_author=False).save()
	
    challenge_2 = Challenge(id=2,
                            title='rage-comic',
                            subtitle='rage-comic',
                            prerequisite=challenge_1,
                            description='Finden Sie einen Webcomic, den Sie lustig finden und laden Sie ihn hier hoch. Beschreiben Sie kurz, wie lange Sie diesen Webcomic schon lesen.',
                            accepted_files='image/*',
                            course=gsi,
                            points=10,
    )
    challenge_2.image.save('2.png', File(open(os.path.join(STATIC_ROOT, 'img', '2.png'), 'rb')))
    challenge_2.save()

    ReviewQuestion(challenge=challenge_2, order=1, text="Empfinden Sie den Webcomic als lustig? Begründen Sie Ihre Antwort.").save()
    ReviewQuestion(challenge=challenge_2, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_2, order=3, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()

    challenge_3 = Challenge(id=3,
                            title='wikipedia',
                            subtitle='wikipedia',
                            prerequisite=challenge_2,
                            description='Kopieren Sie 4 Absätze aus einem Wikipedia-Artikel und geben Sie sie ab! Setzen Sie ans Ende der arbeit den Link auf den Wikipedia-Artikel!',
                            accepted_files='',
                            course=gsi,
                            points=8,
    )
    challenge_3.image.save('3.png', File(open(os.path.join(STATIC_ROOT, 'img', '3.png'), 'rb')))
    challenge_3.save()

    ReviewQuestion(challenge=challenge_3, order=1, text="Was möchte die Autorin bzw. der Autor mit den 4 Absätzen ausdrücken?").save()
    ReviewQuestion(challenge=challenge_3, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_3, order=3, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()
				   
    challenge_4 = Challenge(id=4,
                            title='wissenschaft',
                            subtitle='wissenschaft',
                            prerequisite=challenge_3,
                            description='Finden Sie einen pseudowissenschaftlichen Artikel und laden Sie ihn hier hoch.',
                            accepted_files='application/pdf',
                            course=hci,
                            points=9,
    )
    challenge_4.image.save('4.png', File(open(os.path.join(STATIC_ROOT, 'img', '4.png'), 'rb')))
    challenge_4.save()

    challenge_5 = Challenge(id=5,
                            title='ping',
                            subtitle='ping',
                            description='Laden Sie drei Bilder im png-Format hoch. Beschreiben Sie dann kurz, was auf diesen Bildern zu sehen ist.',
                            accepted_files='image/png',
                            course=gsi,
                            points=10,
    )
    challenge_5.image.save('5.png', File(open(os.path.join(STATIC_ROOT, 'img', '5.png'), 'rb')))
    challenge_5.save()
    ReviewQuestion(challenge=challenge_5, order=1, text="In welchem Zusammenhang stehen die Bilder? Ist ein Muster erkennbar?").save()
    ReviewQuestion(challenge=challenge_5, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_5, order=3, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()
				   
    challenge_6 = Challenge(id=6,
                            title='advice animal',
                            subtitle='advice animal',
                            prerequisite=challenge_5,
                            description='Suchen Sie ein »advice animal« Bild und posten Sie es hier. Geben sie die Quelle dazu an.',
                            accepted_files='image/*',
                            course=hci,
                            points=12,
    )
    challenge_6.image.save('6.png', File(open(os.path.join(STATIC_ROOT, 'img', '6.png'), 'rb')))
    challenge_6.save()
	
    ReviewQuestion(challenge=challenge_6, order=1, text="Was steckt hinter dem »advice«? Welche Probleme werden dadurch aufgezeigt?").save()
    ReviewQuestion(challenge=challenge_6, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_6, order=3, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()

    challenge_7 = Challenge(id=7,
                            title='animated gif',
                            subtitle='animated gif',
                            prerequisite=challenge_6,
                            description='suchen sie ein animated gif und posten sie es. geben sie die quelle dazu an.',
                            accepted_files='image/gif',
                            course=hci,
                            points=14,
    )
    challenge_7.image.save('7.png', File(open(os.path.join(STATIC_ROOT, 'img', '7.png'), 'rb')))
    challenge_7.save()
    ReviewQuestion(challenge=challenge_7, order=1, text="Weshalb wurde das GIF animiert? Würde es auch ohne Animation funktionieren? Begründen Sie Ihre Antwort.").save()
    ReviewQuestion(challenge=challenge_7, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_7, order=3, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()

    challenge_8 = Challenge(id=8,
                            title='zwei menschen',
                            subtitle='zwei menschen',
                            prerequisite=challenge_7,
                            description='Laden Sie zwei Bilder von zwei verschiedenen Menschen hoch. Erklären Sie dann, wer diese beiden Menschen sind. Vergessen Sie nicht auf die Quellenangabe!!11elf',
                            accepted_files='image/*',
                            course=hci,
                            points=5,
    )
    challenge_8.image.save('8.png', File(open(os.path.join(STATIC_ROOT, 'img', '8.png'), 'rb')))
    challenge_8.save()

    challenge_9 = Challenge(id=9,
                            title='youtube',
                            subtitle='youtube',
                            description='Suchen Sie ein gutes YouTube-Video und posten Sie den Link hier. Wenn Sherlock Holmes darin vorkommt, dann können Sie auch einen Extrapunkt bekommen.',
                            accepted_files='',
                            course=gsi,
                            points=25,
    )
    challenge_9.image.save('9.png', File(open(os.path.join(STATIC_ROOT, 'img', '9.png'), 'rb')))
    challenge_9.save()
    ReviewQuestion(challenge=challenge_9, order=1, text="Beschreiben Sie jemandem der Blind ist die Szene. Versuchen Sie dabei auch auf Details einzugehen, die für das Gesamtverständnis von Relevanz sein könnten.").save()
    ReviewQuestion(challenge=challenge_9, order=2, text='Was würden Sie verbessern bzw. wo könnte die Autorin oder der Autor ansetzen, damit die Abgabe besser wird?').save()
    ReviewQuestion(challenge=challenge_9, order=3, text="Kommt in dem Video Sherlock Holmes vor?",
                   visible_to_author=False, boolean_answer=True).save()
    ReviewQuestion(challenge=challenge_9, order=4, text="Anmerkungen an das LVA-Team:",
                   visible_to_author=False).save()
				   
    challenge_10 = Challenge(id=10,
                             title='schmetterling',
                             subtitle='schmetterling',
                             prerequisite=challenge_9,
                             description='Suchen Sie in Google Image Search Schmetterlingsbilder und laden Sie diese hier hoch. Vergessen Sie nicht auf die Quellenangaben!',
                             accepted_files='image/*',
                             course=gsi,
                             points=3,
    )
    challenge_10.image.save('4.png', File(open(os.path.join(STATIC_ROOT, 'img', '4.png'), 'rb')))
    challenge_10.save()

    # create stacks
    print('adding stack accessibility')
    accessibility = Stack(
        title='Universal Design',
        description='In diesem Block setzen sie sich mit »Unversal Design« auseinander. Universal Design (Universelles Design) ist ein internationales Design-Konzept, das Produkte, Geräte, Umgebungen und Systeme derart gestaltet, dass sie für so viele Menschen wie möglich ohne weitere Anpassung oder Spezialisierung nutzbar sind. In der Informatik bedeutet das im allgemeinen, Systeme so zu gestalten, dass sie von Menschen mit Behinderungen, insbesondere blinde Menschen, auch benutzt werden können.',
        course=gsi,
        start_date=date.today() - timedelta(days=100),
        end_date=date.today() + timedelta(days=100),
    )
    accessibility.save()

    print('adding stack digital life')
    digitallife = Stack(
        title='Copyleft vs. Business',
        description='In diesem Block geht es um die Suche nach neuen Business-Modellen für die geänderten Bedingngen, die durch neue Technologien geschaffen wurden. Viele traditionelel Business-Modelle gehen dabei den Bach runter, neue Ansätze sind gefragt.',
        course=gsi,
        start_date=date.today() - timedelta(days=100),
        end_date=date.today() + timedelta(days=100),
    )
    digitallife.save()

    print('adding stack gtav')
    gtav = Stack(
        title='Geschichte der Informatik',
        description='Dieser Block führt sie in die Geschichte der Informatik, zurück zu den Anfängen des interaktiven Computers. Sie setzen sich damit auseinander, welche Vorstellungen von Interaktivität im Laufe der Geschichte entstanden, probiert und wieder verworfen wurden. Dabei werden Darstellungen in Film und Fernsehen ebenso aufgearbeitet wie die Visionen der Techniker und wissenschaftliche Diskussionen.',
        course=gsi,
        start_date=date.today() - timedelta(days=100),
        end_date=date.today() + timedelta(days=100),
    )
    gtav.save()

    # create dummy elaborations
    challenges = Challenge.objects.all()
    for challenge in challenges:
        for dummy_user in dummy_users:
            if not challenge.is_final_challenge():
                Elaboration(challenge=challenge, user=dummy_user, elaboration_text=PlagcheckTestData.get_random_text(),
                            submission_time='2013-11-01 10:00:00').save()

    print('adding final elaboration 1 for challenge 10')
    de4 = Elaboration(challenge=challenge_10, user=d1, elaboration_text="final submission user d1 " + PlagcheckTestData.get_random_text(),
                      submission_time=datetime.now())
    de4.save()

    print('adding FAIL review for dummy user d1')
    Review(elaboration=de4, reviewer=d3, appraisal='F', submission_time=datetime.now()).save()

    print('adding final elaboration 2 for challenge 10')
    de5 = Elaboration(challenge=challenge_10, user=d2, elaboration_text="final submission user d2 " + PlagcheckTestData.get_random_text(),
                      submission_time=datetime.now())
    de5.save()

    print('adding final elaboration 1 for challenge 8')
    de6 = Elaboration(challenge=challenge_8, user=d3, elaboration_text="final submission user d3 " + PlagcheckTestData.get_random_text(),
                      submission_time=datetime.now())
    de6.save()

    # create elaboration for challenge 1 for s0
    print('adding elaboration for challenge 1 for s0')
    e1 = Elaboration(challenge=challenge_1, user=s0, elaboration_text="this elaboration text is from populate demo data " + PlagcheckTestData.get_random_text(),
                     submission_time=datetime.now())
    e1.save()

    elaborations = Elaboration.objects.all()
    e1 = elaborations[0]
    e2 = elaborations[1]
    e3 = elaborations[2]

    # create review for elaboration
    print('adding review 1 for elaboration for challenge 1 for s0')
    r1 = Review(elaboration=e1, reviewer=s0, appraisal='N', submission_time=datetime.now())
    r1.save()
    print('adding review 2 for elaboration for challenge 1 for s0')
    r2 = Review(elaboration=e2, reviewer=s0, appraisal='F', submission_time=datetime.now())
    r2.save()
    print('adding review 3 for elaboration for challenge 1 for s0')
    Review(elaboration=e3, reviewer=s0, appraisal='A', submission_time=datetime.now()).save()
    print('adding review 4 for elaboration for challenge 1 for s0')
    Review(elaboration=e3, reviewer=d2, appraisal='F', submission_time=datetime.now()).save()


    # create elaboration for challenge 2 for s0
    print('adding elaboration for challenge 2 for s0')
    e2 = Elaboration(challenge=challenge_2, user=s0, elaboration_text="this elaboration text is from populate demo data " + PlagcheckTestData.get_random_text(),
                     submission_time=datetime.now())
    e2.save()

    # create review for elaboration
    print('adding review 1 for elaboration for challenge 2 for s0')
    Review(elaboration=de4, reviewer=s0, appraisal='N', submission_time=datetime.now()).save()

    de5.save()
    print('adding review 1 for elaboration for challenge 2 for s0')
    Review(elaboration=de5, reviewer=d1, appraisal='A', submission_time=datetime.now()).save()
    print('adding review 2 for elaboration for challenge 2 for s0')
    Review(elaboration=de5, reviewer=d2, appraisal='S', submission_time=datetime.now()).save()

    # create stack-challenge relations
    print('adding stack challenge relations')
    StackChallengeRelation(stack=accessibility, challenge=challenge_1).save()
    StackChallengeRelation(stack=accessibility, challenge=challenge_2).save()
    StackChallengeRelation(stack=accessibility, challenge=challenge_3).save()
    StackChallengeRelation(stack=accessibility, challenge=challenge_4).save()

    StackChallengeRelation(stack=digitallife, challenge=challenge_5).save()
    StackChallengeRelation(stack=digitallife, challenge=challenge_6).save()
    StackChallengeRelation(stack=digitallife, challenge=challenge_7).save()
    StackChallengeRelation(stack=digitallife, challenge=challenge_8).save()

    StackChallengeRelation(stack=gtav, challenge=challenge_9).save()
    StackChallengeRelation(stack=gtav, challenge=challenge_10).save()

    print('adding escalation for challenge 1 for s0')
    com1 = Comment(text="escalation for review 1 for challenge 1 for d1", author=superuser, post_date=datetime.now(),
                   content_type=ContentType.objects.get_for_model(Review), object_id=r1.id, visibility=Comment.STAFF)
    com1.save()
    com2 = Comment(text="escalation for review 2 for challenge 1 for d2", author=superuser, post_date=datetime.now(),
                   content_type=ContentType.objects.get_for_model(Review), object_id=r2.id, visibility=Comment.PUBLIC)
    com2.save()

    print('Adding Sample Lectures')
    Lecture(
        course=gsi,
        start=datetime(2013, 2, 15, 15, 00, 17, 345952),
        end=datetime(2013, 2, 15, 17, 20, 17, 345952),
        active=True,
    ).save()
    Lecture(
        course=gsi,
        start=datetime(2013, 2, 16, 15, 00, 17, 345952),
        end=datetime(2013, 2, 16, 17, 20, 17, 345952),
        active=True,
    ).save()
    Lecture(
        course=gsi,
        start=datetime(2013, 2, 17, 15, 00, 17, 345952),
        end=datetime(2013, 2, 17, 17, 20, 17, 345952),
        active=True,
    ).save()
#    Lecture(
#        course=gsi,
#        start=datetime(2013, 2, 24, 15, 00, 17, 345952),
#        end=datetime(2014, 2, 24, 17, 20, 17, 345952),
#        active=True,
#    ).save()
    Lecture(
        course=hci,
        start=datetime(2013, 1, 15, 15, 00, 17, 345952),
        end=datetime(2013, 1, 15, 17, 20, 17, 345952),
        active=True,
    ).save()
    Lecture(
        course=hci,
        start=datetime(2013, 1, 16, 15, 00, 17, 345952),
        end=datetime(2013, 1, 16, 17, 20, 17, 345952),
        active=True,
    ).save()

    print('Adding Sample Slides')
    Slide(
        lecture_id=1,
        title="Preparation Slide #1 - Lecture 1",
        pub_date=datetime(2013, 2, 10, 15, 21, 17, 345952),
        filename="vo_10_02_13_1",
        tags='.preparation',
    ).save()
    Slide(
        lecture_id=1,
        title="Preparation Slide #2 - Lecture 1",
        pub_date=datetime(2013, 2, 10, 15, 22, 17, 345952),
        filename="vo_10_02_13_2",
        tags='.preparation',
    ).save()
    Slide(
        lecture_id=1,
        title="Preparation Slide #3 - Lecture 1",
        pub_date=datetime(2013, 2, 10, 15, 23, 17, 345952),
        filename="vo_10_02_13_3",
        tags='.preparation',
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #1 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 20, 17, 345952),
        filename="vo_15_02_13_1",
        tags='.exercise',
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #2 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 22, 17, 345952),
        filename="vo_15_02_13_2",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #3 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 24, 17, 345952),
        filename="vo_15_02_13_3",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #4 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 26, 17, 345952),
        filename="vo_15_02_13_4",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #5 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 28, 17, 345952),
        filename="vo_15_02_13_5",
        tags='.exercise',
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #6 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 30, 17, 345952),
        filename="vo_15_02_13_6",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #7 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 32, 17, 345952),
        filename="vo_15_02_13_7",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #8 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 34, 17, 345952),
        filename="vo_15_02_13_8",
    ).save()
    Slide(
        lecture_id=1,
        title="Super Sample Slide #9 - Lecture 1",
        pub_date=datetime(2013, 2, 15, 15, 36, 17, 345952),
        filename="vo_15_02_13_9",
        tags='.exercise',
    ).save()
    Slide(
        lecture_id=2,
        title="Super Sample Slide #1 - Lecture 2",
        pub_date=datetime(2013, 2, 16, 15, 20, 17, 345952),
        filename="vo_16_02_13_1",
    ).save()
    Slide(
        lecture_id=2,
        title="Super Sample Slide #2 - Lecture 2",
        pub_date=datetime(2013, 2, 16, 15, 22, 17, 345952),
        filename="vo_16_02_13_2",
    ).save()
    Slide(
        lecture_id=2,
        title="Super Sample Slide #2 - Lecture 2",
        pub_date=datetime(2013, 2, 16, 15, 24, 17, 345952),
        filename="vo_16_02_13_3",
    ).save()
    Slide(
        lecture_id=3,
        title="Super Sample Slide #1 - Lecture 3",
        pub_date=datetime(2013, 2, 17, 15, 20, 17, 345952),
        filename="vo_17_02_13_1",
    ).save()
    Slide(
        lecture_id=3,
        title="Super Sample Slide #2 - Lecture 3",
        pub_date=datetime(2013, 2, 17, 15, 22, 17, 345952),
        filename="vo_17_02_13_2",
        tags='.exercise',
    ).save()

    print("Adding sample stream")
    Stream(
        lecture_id=1,
        url="rtmp://video.zserv.tuwien.ac.at/lecturetube_public",
        type="rtmp",
        clipname="gsiss13e10",
        offset=-656,
    ).save()

    for user in AuroraUser.objects.all():
        if not user.avatar:
            user.get_gravatar()

if __name__ == '__main__':
    populate_demo_data()