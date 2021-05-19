import yaml
from discord import Embed


#LOAD CONFIG.YAML
with open('config.yml','r') as config_file:
    yaml_data = yaml.safe_load(stream=config_file)




#Get the Discord bot Token
#Path: 'auth/bot-token'
def get_bot_token():
    return yaml_data.get('auth').get('bot-token')

#Settings
def get_command_prefix():
    return yaml_data.get('settings').get('command-prefix')

def get_core_server_id():
    return yaml_data.get('settings').get('core-server-id')

def get_dashboard_endpoint():
    return yaml_data.get('settings').get('dashboard-endpoint')

def get_bot_footer():
    return yaml_data.get('settings').get('footer')

#Sql
def get_postgres_dsn():
    sql = yaml_data.get('sql')
    return f"asyncpg://{sql.get('user')}:{sql.get('password')}@{sql.get('hostname')}:{sql.get('port')}/{sql.get('db')}"

#Redis
def get_redis_hostname():
    return yaml_data.get('redis').get('hostname')

def get_redis_password():
    return yaml_data.get('redis').get('password')


#Ticket
def get_ticket_panel_embed():
    data = yaml_data.get('modules').get('ticket').get('panel').get('embed').copy()
    data.update({'footer': yaml_data.get('settings').get('footer')})
    color = int(data.pop('color'),16)
    embed : Embed = Embed.from_dict(data)
    embed.color = color
    return embed

def get_ticket_error_embed():
    data = yaml_data.get('modules').get('ticket').get('panel').get('embed').copy()
    data.update({'footer': yaml_data.get('settings').get('footer')})
    color = int(data.pop('color'),16)
    embed : Embed = Embed.from_dict(data)
    embed.color = color
    return embed

def get_ticket_create_emoji():
    return yaml_data.get('modules').get('ticket').get('create-emoji')

#Licence
def get_licence_new_licence_emoji():
    return yaml_data.get('modules').get('licence').get('new-licence-emoji')

def get_licence_no_licence_embed():
    data = yaml_data.get('modules').get('licence').get('no-licence').get('embed').copy()
    data.update({'footer': yaml_data.get('settings').get('footer')})
    color = int(data.pop('color'),16)
    embed = Embed.from_dict(data)
    embed.color = color
    return embed

def get_licence_show_licences_embed():
    data = yaml_data.get('modules').get('licence').get('show-licences').get('embed').copy()
    data.update({'footer': yaml_data.get('settings').get('footer')})
    color = int(data.pop('color'),16)
    embed = Embed.from_dict(data)
    embed.color = color
    return embed

#Suggestion
def get_suggestion_core_embed():
    data = yaml_data.get('modules').get('suggestion').get('core-embed').copy()
    color = int(data.pop('color'),16)
    embed = Embed.from_dict(data)
    embed.color = color
    return embed

#Moderation
def get_moderation_core_embed():
    data = yaml_data.get('modules').get('moderation').get('core-embed').copy()
    data.update({'footer': yaml_data.get('settings').get('footer')})
    color = int(data.pop('color'),16)
    embed = Embed.from_dict(data)
    embed.color = color
    return embed


def get_suggestion_channel_name():
    return yaml_data.get('modules').get('suggestion').get('channel-name')

def get_suggestion_embed_title():
    return yaml_data.get('modules').get('suggestion').get('core-embed').get('title')

def get_suggestion_embed_description():
    return yaml_data.get('modules').get('suggestion').get('core-embed').get('description')

def get_suggestion_embed_footer():
    return yaml_data.get('modules').get('suggestion').get('core-embed').get('footer')

def get_suggestion_embed_color():
    return yaml_data.get('modules').get('suggestion').get('core-embed').get('color')


def get_suggestion_syntax_embed_title():
    return yaml_data.get('modules').get('suggestion').get('syntax-embed').get('title')

def get_suggestion_syntax_embed_description():
    return yaml_data.get('modules').get('suggestion').get('syntax-embed').get('description')

def get_suggestion_syntax_embed_footer():
    return yaml_data.get('modules').get('suggestion').get('syntax-embed').get('footer')

def get_suggestion_syntax_embed_color():
    return yaml_data.get('modules').get('suggestion').get('syntax-embed').get('color')


def get_suggestion_syntax():
    return yaml_data.get('modules').get('suggestion').get('syntax')

def get_link_embed_title():
    return yaml_data.get('modules').get('links').get('embed').get('title')

def get_link_embed_footer():
    return yaml_data.get('modules').get('links').get('embed').get('footer')

def get_link_embed_color():
    return yaml_data.get('modules').get('links').get('embed').get('color')

def get_link_dict():
    return yaml_data.get('modules').get('links').get('link-list')
