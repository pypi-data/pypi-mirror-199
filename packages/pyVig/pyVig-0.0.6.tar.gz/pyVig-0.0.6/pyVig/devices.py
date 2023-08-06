
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