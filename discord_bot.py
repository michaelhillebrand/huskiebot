import logging

import discord
from discord.ext import commands

from cogs.poll import get_new_description, string_description_to_dictionary


class HuskieBot(commands.Bot):

    async def on_ready(self):
        logging.info('Huskie Bot Online')

    async def on_raw_reaction_add(self, payload):
        """ This method is triggered when there is a reaction added to any message. For now it only works for messages
        that have a Poll in the embed footer.

        :param payload: RawReactionActionEvent
        :return: None
        """
        updated_message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        description_dict = string_description_to_dictionary(updated_message.embeds[0].description)
        if "Poll" in updated_message.embeds[0].footer.text:
            new_description = get_new_description(description_dict, updated_message.reactions)
            new_embed = discord.Embed(title=updated_message.embeds[0].title,
                                      description=new_description,
                                      colour=discord.Color.orange())
            new_embed.set_footer(text='Poll'.format(updated_message.id))
            await updated_message.edit(embed=new_embed)

    async def on_raw_reaction_remove(self, payload):
        """ This method is triggered when there is a reaction removed from any message. For now it only works for
        messages that have a Poll in the embed footer.

        :param payload: RawReactionActionEvent
        :return: None
        """
        updated_message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        description_dict = string_description_to_dictionary(updated_message.embeds[0].description)
        if "Poll" in updated_message.embeds[0].footer.text:
            new_description = get_new_description(description_dict, updated_message.reactions)
            new_embed = discord.Embed(title=updated_message.embeds[0].title, description=new_description)
            new_embed.set_footer(text='Poll'.format(updated_message.id))
            await updated_message.edit(embed=new_embed)
