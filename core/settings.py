import yaml



#LOAD CONFIG.YAML
with open('config.yml','r') as config_file:
    yaml_data = yaml.safe_load(stream=config_file)


#Get the Discord bot Token
#Path: 'auth/bot-token'
def get_bot_token():
    return yaml_data.get('auth').get('bot-token')

def get_command_prefix():
    return yaml_data.get('settings').get('command-prefix')

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

def get_ticket_channel_name():
    return yaml_data.get('modules').get('ticket').get('channel-name')

def get_ticket_create_emoji():
    return yaml_data.get('modules').get('ticket').get('create-ticket-emoji')

def get_ticket_close_emoji():
    return yaml_data.get('modules').get('ticket').get('close-ticket-emoji')

def get_ticket_embed_title():
    return yaml_data.get('modules').get('ticket').get('create-embed').get('title')

def get_ticket_embed_description():
    return yaml_data.get('modules').get('ticket').get('create-embed').get('description')

def get_ticket_embed_footer():
    return yaml_data.get('modules').get('ticket').get('create-embed').get('footer')

def get_ticket_embed_color():
    return yaml_data.get('modules').get('ticket').get('create-embed').get('color')

def get_ticket_suport_role():
    return yaml_data.get('modules').get('ticket').get('suport-team-role')

def get_ticket_close_embed_title():
    return yaml_data.get('modules').get('ticket').get('close-embed').get('title')

def get_ticket_close_embed_description():
    return yaml_data.get('modules').get('ticket').get('close-embed').get('description')

def get_ticket_close_embed_footer():
    return yaml_data.get('modules').get('ticket').get('close-embed').get('footer')

def get_ticket_close_embed_color():
    return yaml_data.get('modules').get('ticket').get('close-embed').get('color')