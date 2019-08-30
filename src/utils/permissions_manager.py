import yaml
import requests
import discord


class PermissionsManager:
    """
    dev => 3
    admin => 2
    modo => 1
    peuple => 0
    """

    base_url = 'https://epimodo.gastbob40.ovh/api/'

    def get_permissions(self, member: discord.Member or discord.User, guild: discord.Guild):
        with open('run/config/permissions.yml', 'r') as file:
            permissions = yaml.safe_load(file)

        r = requests.get(f'{self.base_url}servers/?discord_id={str(guild.id)}',
                         headers=self.get_headers())

        if not r.ok:
            return False, f'API error: {r.reason}'

        admin_role, modo_role = None, None

        if len(r.json()) == 1:
            data = r.json()[0]
            admin_role = guild.get_role(data['discord_admin_role_id'])
            modo_role = guild.get_role(data['discord_modo_role_id'])

        if member.id in permissions['dev']:
            return True, 3

        if member.id in permissions['epilogin'] or admin_role in member.roles:
            return True, 2

        if modo_role in member.roles:
            return True, 1

        return True, 0

    @staticmethod
    def get_headers():
        with open('run/config/tokens.yml', 'r') as file:
            token = yaml.safe_load(file)['epimodo_website_token']

        return {
            'content-type': 'application/json',
            'Authorization': f'Token {token}'
        }
