class Personality(object):
    name = 'Huskie Bot'
    slug = 'default'
    avatar_path = None
    greetings = (
        "Hey, What's up?",
    )
    member_greetings = (
        'Welcome {member}!',
    )
    eight_ball_responses = (
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes - Definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook Good',
        'Yes',
        'Signs point to yes',
        'Reply hasy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    )
    triggers = (
        ('i love huskie', 'He loves you more'),
    )
    presence_options = (
        (0, 'shitposting memes'),
        (0, 'Tuber Simulator'),
        (2, 'the developers'),
        (3, 'dank memes'),
        (0, 'Uploading dank memes'),
        (3, 'sad horse show'),
        (0, 'the game'),
        (0, 'Dungons and Drags'),
        (3, 'the world burn'),
    )

    """
    from discord.enums:
    class ActivityType(Enum):
        unknown = -1
        playing = 0
        streaming = 1
        listening = 2
        watching = 3
    """
