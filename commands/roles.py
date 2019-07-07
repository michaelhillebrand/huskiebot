from commands.base import BaseCommand
from pprint import pprint
from discord import utils

class ListRoles(BaseCommand):
    trigger = 'roles'
    description = 'Lists the roles of the user who ran this command'
    allowed_arguments = {
        'all' : 'all',
        'current' : 'current'
    }

    def _build_formatted_role_list(self, roles):
        """
        Utility function for formatting a list of role object

        Parameters
        ----------
        roles : list of discord.Role objects

        Returns
        -------
        str : formatted list of roles
        """
        formatted_role_list = ''
        for role in roles:
            formatted_role_list += '- {}\n'.format(utils.escape_mentions(role.name))
        return formatted_role_list

    def _all(self, guild):
        """
        Lists the existing roles on the given guild that the message came from

        Parameters
        ----------
        guild : discord.Guild

        Returns
        -------
        str : list out roles that exist on the given guild
        """
        mesage_template = ('Here are the current roles available in this guild:\n'
                          '{list_of_all_roles}')
        all_roles = self._build_formatted_role_list(guild.roles)
        return mesage_template.format(list_of_all_roles = all_roles)

    def _current(self, member):
        """
        Lists the current roles assigned to the user who ran this command

        Parameters
        ----------
        member : discord.Member

        Returns
        -------
        str : mention user and list out roles the user is in
        """
        mesage_template = ('{member}, you are currently a part of the following roles in this guild:\n'
                          '{list_of_current_roles}')

        current_roles = self._build_formatted_role_list(member.roles)

        return mesage_template.format(member = member.mention, list_of_current_roles = current_roles)

    async def command(self, message):
        """
        Command to list the existing roles in a guild or the roles of the user who ran this command

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
        """
        args = message.content.split(' ')[1:]
        if len(args) == 0:
            response = self._all(message.guild)
        elif len(args) == 1:
            argument = args[-1].lower()
            if argument == self.allowed_arguments['all']:
                response = self._all(message.guild)
            elif argument == self.allowed_arguments['current']:
                response = self._current(message.author)
            else:
                response = "Invalid argument"
        else:
            response = "Invalid argument"

        await message.channel.send(response)
