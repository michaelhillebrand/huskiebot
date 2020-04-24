from personalities.base import Personality


class BoJack(Personality):
    name = 'BoJack Horseman'
    avatar_path = 'bojack_horseman.jpg'
    greetings = (
        "Yeah, it's me, straight off your TV screens and into your shitty lives!",
    )
    member_greetings = (
        'Heeeeeey... You',
    )
    eight_ball_responses = (
        "What a stupid question. Are you Todd?",
    )
    triggers = (
        (['drug', 'drugs'], 'Drugs, where?'),
    )
    presence_options = (
        (3, 'Horsin\' Around'),
        (2, 'Diane talk about her problems'),
        (0, 'Decapathon VII with Todd'),
        (1, 'Philbert')
    )
    quotes = (
        "I’m responsible for my own happiness? I can’t even be responsible for my own breakfast!",
        "You sleep on my couch and you don’t pay rent. I’ve had tapeworms that are less parasitic. "
        "I don’t even remember why I let you stay with me in the first place.",
        "Laura! Clear our my schedule! I have to push a boulder up a hill and then have it roll over me "
        "time and time again with no regard for my well-being!",
        "I need to go take a shower so I can’t tell if I’m crying or not",
        "BoJack, I’m gonna level with you, honey. This whole you-hating-the-troops thing is not great",
        "Dead on the inside, dead on the outside",
        "Todd, I weigh 1200 pounds. It takes a lot of beer to get me drunk... Yes",
    )
