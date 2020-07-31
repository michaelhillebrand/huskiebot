from personalities.base import Personality


class Saitama(Personality):
    name = 'Saitama'
    slug = 'saitama'
    avatar_path = 'saitama.jpeg'
    greetings = (
        "Hey, What's up?",
    )
    member_greetings = (
        'Welcome {member}!',
    )
    eight_ball_responses = ()
    triggers = ()
    presence_options = (
        (0, 'video games'),
        (2, 'to Genos complain'),
        (3, 'anime'),
    )
    quotes = (
        'ONE PUUUUUUNCH!'
        'あなたの承認が欲しいので、私はヒーローではありません。 やりたいからやる！',
        '圧倒的な強さは退屈です。',
        '一生懸命働いたって？ まあ、多分もう少し長く働く必要があるでしょう。'
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
