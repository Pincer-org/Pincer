# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from pincer.objects import Guild, Emoji, Channel, Role

FAKE_GUILD = {
    'id': '0',
    'name': 'test-server',
    'features': [],
    'emojis': [
        {'name': 'test-emoji',
         'roles': [],
         'id': '0',
         'require_colons': True,
         'managed': False,
         'animated': False,
         'available': True
         }
    ],
    'stickers': [],
    'owner_id': '0',
    'region': 'us-east',
    'afk_timeout': 300,
    'system_channel_id': '0',
    'widget_enabled': False,
    'widget_channel_id': '0',
    'verification_level': 0,
    'roles': [
        {'id': '0',
         'name': '@everyone',
         'permissions': '0',
         'position': 0,
         'color': 0,
         'hoist': False,
         'managed': False,
         'mentionable': False,
         }
    ],
    'default_message_notifications': 0,
    'mfa_level': 0,
    'explicit_content_filter': 0,
    'max_members': 250000,
    'max_video_channel_users': 25,
    'premium_tier': 0,
    'premium_subscription_count': 0,
    'system_channel_flags': 0,
    'preferred_locale': 'en-US',
    'premium_progress_bar_enabled': False,
    'nsfw': False,
    'nsfw_level': 0,
    'channels':
    # This is not how channels are passed into Guild.from_dict in the code. A
    # Channel object is passed in instead. I haven't done that here because the
    # Guild.from_dict() method expects a Dict without APIObjects in it.
    # The code should be changed to reflect that once this test is made passing.
    [
        {'id': '0',
         'type': 4,
         'name': 'Text Channels',
         'position': 0,
         'guild_id': '0',
         'permission_overwrites': [],
         'nsfw': False
         },
    ]
}


class TestChannel:

    @staticmethod
    def test_get():

        guild = Guild.from_dict(FAKE_GUILD)

        assert guild == Guild(
            id=0,
            name="test-server",
            features=[],
            emojis=[
                Emoji(
                    name="test-emoji",
                    roles=[],
                    id=0,
                    require_colons=True,
                    managed=False,
                    animated=False,
                    available=True
                )
            ],
            stickers=[],
            owner_id=0,
            region="us-east",
            afk_timeout=300,
            system_channel_id=0,
            widget_enabled=False,
            widget_channel_id=0,
            verification_level=0,
            roles=[
                Role(
                    id=0,
                    name="@everyone",
                    permissions=0,
                    position=0,
                    color=0,
                    hoist=False,
                    managed=False,
                    mentionable=False,
                )
            ],
            default_message_notifications=0,
            mfa_level=0,
            explicit_content_filter=0,
            max_members=250000,
            max_video_channel_users=25,
            premium_tier=0,
            premium_subscription_count=0,
            system_channel_flags=0,
            preferred_locale="en-US",
            premium_progress_bar_enabled=False,
            nsfw=False,
            nsfw_level=0,
            channels=[
                Channel(
                    id=0,
                    type=4,
                    name="Text Channels",
                    position=0,
                    guild_id=0,
                    permission_overwrites=[],
                    nsfw=False
                )
            ]
        )
