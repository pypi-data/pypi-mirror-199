
import pandas as pd
from .general import update_vlans_info, drop_empty

# --------------------------------------------- 

class AdevDevices():

	def __init__(self, stencil):
		self.stencil = stencil
		self.devices={}
		self.mandatory_columns = {'hostname', 'stencils', 'device_type'}
		self.optional_columns = {'ip_address', 'device_model', 'serial_number', 'hierarchical_order', 'vlan_members',}

	def add_to_devices(self, **kwargs):
		mandatory_col_maps = {
			'hostname': 'nbr_hostname' ,
		}
		#
		ll = [self.mandatory_columns, self. optional_columns]
		for l in ll: 
			for k in l:
				if k in mandatory_col_maps:
					x = mandatory_col_maps[k]
				else:
					x = k
				#
				if not self.devices.get(k):
					self.devices[k] = []
				try:
					if k == 'stencils':
						self.devices[k].append(self.stencil)
					else:
						self.devices[k].append(kwargs[x])
				except:
					self.devices[k].append("")


	def add_vlan_info(self, vlan_df):
		self.merged_df = update_vlans_info(self.int_df, vlan_df)
		return self.merged_df

	def device_dataframe(self):
		df = pd.DataFrame(self.devices)
		df = drop_empty(df, column='hostname')
		df.drop_duplicates('hostname', inplace=True)
		self.int_df = df
		return df

# --------------------------------------------- 
def device_df_drop_empty_duplicates(devices):
	df = pd.DataFrame(devices)
	df = drop_empty(df, column='hostname')
	df.drop_duplicates('hostname', inplace=True)
	return df


# --------------------------------------------- 
def update_var_df_details_to_table_df(merged_df, DCT_dict, var_func_dict):

	for hostname, DCT in DCT_dict.items():
		for key, value in DCT.__dict__.items():
			if key not in var_func_dict: continue
			if key == 'hostname': continue
			func = var_func_dict[key]
			merged_df[key] = merged_df.apply(lambda x: 
				func(update=True, 
					merged_df_ser_hostname=x['hostname'], 
					merged_df_series_key=x[key], 
					key=key, 
					value=value, 
					hostname=hostname), 
				axis=1)
	
	return merged_df
