
import nettoolkit as nt

# --------------------------------------------- 


def get_physical_if_up(df):
	return df[ (df['link_status'] != 'administratively down')| (df['link_status'] != 'Enabled')].fillna("")

def get_physical_if_relevants(df):
	relevant_cols = ['interface', 'nbr_dev_type', 
	# 'media_type', 
	'int_filter',
	'nbr_hostname',   'nbr_interface',
	# 'nbr_serial', 'nbr_ip',
	'vlan_members', 
	# 'channel_group_interface', 'channel_grp'
	]
	return df[relevant_cols]

# --------------------------------------------- 

def get_vlan_if_up(df):
	return df[ (df['link_status'] != 'administratively down')| (df['link_status'] != 'Enabled')].fillna("")

def get_vlan_if_relevants(df):
	relevant_cols = ['int_number', 'interface', 'intvrf', 'subnet' ]
	return df[relevant_cols]

# --------------------------------------------- 


def get_patterns(df, line_pattern_style_separation_on, line_pattern_style_shift_no):
	if not line_pattern_style_separation_on: return None
	uniq_medias = df[line_pattern_style_separation_on].unique()
	media_pattern = {}
	for m in uniq_medias:
		for n in range(1, 10000, line_pattern_style_shift_no):
			if n in media_pattern.values(): continue
			media_pattern[m] = n
			break
	return media_pattern

def update_pattern(df, patterns, line_pattern_style_separation_on):
	if not line_pattern_style_separation_on: return df
	df['pattern'] = df[line_pattern_style_separation_on].apply(lambda x: patterns[x])
	return df

# --------------------------------------------- 

def series_item_0_value(s):
	for x in s:
		return x

def get_vlans_info(vlan_members, vlan_df):
	vlan_members = nt.LST.remove_empty_members(vlan_members.split(","))
	s = ''
	if len(vlan_members) == 0: return s
	for vlan in vlan_members:
		vlan = int(vlan)
		df = vlan_df[vlan_df['int_number'] == vlan]
		s += series_item_0_value(df['interface']) + " "
		s += series_item_0_value(df['intvrf']) + " "
		s += series_item_0_value(df['subnet']) + "\n"
	return s

def update_vlans_info(int_df, vlan_df):
	int_df['vlan_info'] = int_df['vlan_members'].apply(lambda x: get_vlans_info(x, vlan_df))
	return int_df


# --------------------------------------------- 

def drop_empty(df, column):
	return df[df[column] != ""]