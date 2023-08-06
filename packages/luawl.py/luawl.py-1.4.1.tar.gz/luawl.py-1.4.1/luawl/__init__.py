from datetime import datetime
import requests
from luawl.definition import luawl_whitelist
# END OF IMPORTS

luawl_token = ''
luawl_api_url = 'https://api.luawl.com/'

class luawl_object:
	def __init__(self):
		self.token = luawl_token

def send_luawl_request(href, body):
	if hasattr(body, 'HWID') and len(body.HWID) <= 40:
		delattr(body, 'HWID')

	if hasattr(body, 'discord_id') and len(body.discord_id) >= 20:
		delattr(body, 'discord_id')

	if hasattr(body, 'wl_key') and len(body.wl_key) != 40:
		delattr(body, 'wl_key')
			
	return requests.post(luawl_api_url + href + '.php', json = body.__dict__).json()

def add_whitelist(discord_id, trial_hours = None, wl_script_id = None):
	body = luawl_object()
	body.discord_id = discord_id
	body.trial_hours = trial_hours
	body.wl_script_id = wl_script_id
	
	return send_luawl_request('whitelistUser', body)

def get_whitelist(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	response = send_luawl_request('getKey', body)
	
	return luawl_whitelist(response)

def delete_whitelist(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('deleteKey', body)

def reset_hwid(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	response = send_luawl_request('resetHWID', body)

	if (type(response) == str):
		return response

	raise Exception(response.get('error'))

def is_on_cooldown(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('isOnCooldown', body)

def remove_cooldown(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('removeCooldown', body)

def update_key_status(discord_id_or_key, key_status: str):
	if (not (key_status == 'Active' or key_status == 'Disabled' or key_status == 'Unassigned' or key_status == 'Assigned')):
		raise Exception('Valid status: Active|Assigned|Disabled|Unassigned')
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key
	body.status = key_status

	return send_luawl_request('updateKeyStatus', body)

def disable_user_key(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('disableKey', body)

def add_blacklist(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('createBlacklist', body)

def remove_blacklist(discord_id_or_key):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key

	return send_luawl_request('removeBlacklist', body)

def get_logs(discord_id_or_key_or_hwid):
	body = luawl_object()
	body.discord_id = discord_id_or_key_or_hwid
	body.wl_key = discord_id_or_key_or_hwid
	body.HWID = discord_id_or_key_or_hwid

	return send_luawl_request('getLogs', body)

def get_scripts():
	return send_luawl_request('getAccountScripts', luawl_object())

def get_buyer_role():
	return send_luawl_request('getBuyerRole', luawl_object())

def add_key_tags(discord_id_or_key, tags, wl_script_id):
	body = luawl_object()
	body.wl_script_id = wl_script_id
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key
	body.tags = tags

	return send_luawl_request('addKeyTags', body)

def get_account_stats():
	data = send_luawl_request('getAccountStats', luawl_object())

	if type(data) is dict:
		for key, value in data.items():
			if type(value) is str:
				try:
					data[key] = int(value)
				except:
					data[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

	return data

def update_key_expiration(discord_id_or_key, expiry_hours):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key
	body.expiryHours = expiry_hours

	return send_luawl_request('updateKeyExpiration', body)

def transfer_keys_to_new_script(old_script_id, new_script_id):
	body = luawl_object()
	body.old_wl_script_id = old_script_id
	body.new_wl_script_id = new_script_id

	return send_luawl_request('bulkUpdateKeyWLScript', body)

def transfer_key_to_new_script(discord_id_or_key, new_script_id):
	body = luawl_object()
	body.discord_id = discord_id_or_key
	body.wl_key = discord_id_or_key
	body.wl_script_id = new_script_id

	return send_luawl_request('updateKeyWLScript', body)

def get_all_keys():
	return send_luawl_request('getAllKeys', luawl_object())