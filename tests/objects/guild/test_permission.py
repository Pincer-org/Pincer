# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
import pytest
from pincer.objects.guild.permissions import Permission, PermissionEnums


class TestPermission:
    @staticmethod
    def test_invalid_permissions():
        with pytest.raises(ValueError):
            Permission(this_permisison_does_not_exist=True)

        with pytest.raises(ValueError):
            Permission(
                manage_channels="True",
            )

    @staticmethod
    def test_valid_permissions():
        valid_perms = (
            "create_instant_invite",
            "kick_members",
            "ban_members",
            "administrator",
            "manage_channels",
            "manage_guild",
            "add_reactions",
            "view_audit_log",
            "priority_speaker",
            "stream",
            "view_channel",
            "send_messages",
            "send_tts_messages",
            "manage_messages",
            "embed_links",
            "attach_files",
            "read_message_history",
            "mention_everyone",
            "use_external_emojis",
            "view_guild_insights",
            "connect",
            "speak",
            "mute_members",
            "deafen_members",
            "move_members",
            "use_vad",
            "change_nickname",
            "manage_nicknames",
            "manage_roles",
            "manage_webhooks",
            "manage_emojis_and_stickers",
            "use_application_commands",
            "request_to_speak",
            "manage_events",
            "manage_threads",
            "create_public_threads",
            "create_private_threads",
            "use_external_stickers",
            "send_messages_in_threads",
            "start_embedded_activities",
            "moderate_members",
        )

        for perm in valid_perms:
            assert hasattr(Permission(), perm)

    @staticmethod
    def test_from_int():
        assert Permission.from_int(1025, 268435472) == Permission(
            view_channel=True,
            manage_channels=False,
            create_instant_invite=True,
            manage_roles=False,
        )

        assert Permission.from_int(0, 0) == Permission()

    @staticmethod
    def test_to_int():
        allow, deny = Permission.to_int(Permission())
        assert allow == 0
        assert deny == 0

        permission = Permission()
        for enum in PermissionEnums:
            if getattr(permission, enum.name.lower()):
                allow |= enum.value
            elif getattr(permission, enum.name.lower()) is False:
                deny |= enum.value

        assert Permission.to_int(Permission()) == (0, 0)
