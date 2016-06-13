export default [
  {
    id: 0,
    lane: 0,
    type: "Feature Request",
    post_date: 1462372465,
    author: "s3",
    title: "Newsfeed, nur eigene Nachrichten anzeigen",
    body: 'Da meine eigenen Posts bereits weit zurückliegen, muss ich lange ' +
    'scrollen, um sie wieder zu finden. Es wäre praktisch, wenn bei den Filtern ' +
    '"Open Newsfeed" auch eine Option "Own Comments" zu finden wäre.',
    upvotes: 2,
    comments: []
  },
  {
    id: 1,
    lane: 1,
    type: "Bug",
    post_date: 1463728834,
    author: "s1",
    title: "Vorreihen von nicht-Dummy-Abgaben",
    body: 'Ich glaube, ein Grund für das aktuelle Review-Problem ist, dass es ' +
    'übermäßig viele Dummies gibt bzw. richtige Abgaben nicht bevorzugt werden. ' +
    'Gegen Anfang des Semesters wurden echte Abgaben anscheinend noch ' +
    'vorgereiht, da man sogar schon wenige Stunden nach Veröffentlichung einer ' +
    'Challenge richtige Abgaben reviewen konnte. Aktuell sieht man, selbst wenn ' +
    'man erst Tage nachher abgibt, fast ausschließlich nur Dummies. Ich denke, ' +
    'dass man die Situation durch Vorreihen der richtigen Abgaben wieder ' +
    'deutlich verbessern könnte. (Es scheint, als wäre es in den ersten Wochen ' +
    'so gewesen, vllt. ist irgendwo ein Bug; z.B. eine nicht-gesetzte Dummy-Flag ' +
    'oder Ähnliches.)',
    upvotes: 4,
    comments: [
      {
        id: 0,
        post_date: 1463833234,
        pic: "/static/img/7.png",
        author: "peterpur",
        comment: "sorry, die überdurchschnittliche vergabe von dummy-arbeiten " +
        "war ein fehler, den wir jetzt behoben haben. ich hoffe, dass es ab " +
        "jetzt runder läuft."
      },
      {
        id: 1,
        post_date: 1463847634,
        pic: "/static/img/2.png",
        author: "s1",
        comment: "Kurzes Feedback: Ich hatte, nach geschätzten 10 Dummies in " +
        "letzter Zeit, gerade eben wieder die ersten 3 " +
        "ordentlichen Abgaben." +
        " Scheint jetzt also wieder besser zu klappen. Danke!"
      }
    ]
  },
  {
    id: 2,
    lane: 0,
    type: "Bug",
    post_date: 1463063665,
    author: "s0",
    title: "Darstellungsfehler auf der Startseite",
    body: 'Auf der Startseite wird das Kästchen mit den Lecturedates falsch ' +
    'dargestellt. Sobald man irgendein anderes Kästechen auf-/zuklappt, rutscht ' +
    'es dann auf seinen richtigen Platz zurück.',
    images: [
      "/static/img/NqFjrql.png"
    ],
    upvotes: 1,
    comments: [
      {
        id: 0,
        post_date: 1463067297,
        pic: "/static/img/1.png",
        author: "s0",
        comment: "Habe dazu einen kleinen clip gemacht: " +
        "https://flowlo.me/tmp/aurora.webm"
      },
      {
        id: 1,
        pic: "/static/img/1.png",
        author: "s0",
        post_date: 1463068257,
        comment: "Chrome Version 50.0.2661.102 m<br/>" +
        "Bildschirm 1920x1080<br/>" +
        "Safari 8.0.7 / 1920x1080"
      }
    ]
  }
];