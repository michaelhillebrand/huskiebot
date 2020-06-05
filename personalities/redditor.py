from personalities.base import Personality


class Redditor(Personality):
    name = 'A Redditor'
    avatar_path = 'redditor.png'
    greetings = (
        "Ah yes, Stonks",
    )
    member_greetings = (
        "And then {member} turned into a pickle! funniest shit I've ever seen!",
        'Are you winning {member}?',
    )
    eight_ball_responses = (
        'Hell ya',
        'It be like it do',
        'yes, I rate it 5 poorly groomed redditors out of 5',
        'My facebook group said so, so yes',
        "You don't think it be like it is but it do",
        'Reddit says yes',
        'Probs man',
        '.....Fuck it, sure',
        'Ya sure, just stop bothering me im playing Minecraft',
        'Not a chance, I give it 0 screaming cowboys out of 10',
        'Nigga say what?',
        "Why can't you be normal?!",
        'Not stonks',
        "Can't tell, reddit is down",
        'LeT mE gOoGlE tHaT fOr YoU.......jesus what a bitch',
        'No, and while we are here, did you ever hear the tragedy of darth plagueis the wise?',
        'Fuck no',
        "Let's ask twitter",
        'Not on your Waifus life',
        'Where do you think you are 9gag?'
    )
    presence_options = (
        (0, 'Japanese Dating Simulator'),
        (0, 'EGG'),
        (3, 'Them do surgery on a grape'),
        (1, 'Dank Memes'),
        (0, 'Fortnite'),
        (3, 'Rick and Morty'),
        (1, 'Myself chugging White Claws'),
        (2, 'Joe Rogan'),
        (3, 'Pickle Rick'),
    )