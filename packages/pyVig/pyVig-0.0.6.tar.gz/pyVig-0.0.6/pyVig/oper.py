
import pandas as pd
import nettoolkit as nt
from .devices import AdevDevices
from .cablings import ADevCablings
from .general import *

# --------------------------------------------- 
# Data Frame Generator
# --------------------------------------------- 
class DFGen():

	def __init__(self, files):
		self.files = files
		self.default_stencil = None
		self.default_x_spacing = 3.5
		self.default_y_spacing = 2
		self.line_pattern_style_separation_on = None
		self.line_pattern_style_shift_no = 2
		self.func_dict = {}
		self.blank_dfs()

	def blank_dfs(self):
		self.devices_merged_df = pd.DataFrame({'hostname':[]})
		self.cabling_merged_df = pd.DataFrame({'a_device':[]})

	def update_attributes(self, **kwargs):
		for k, v in kwargs.items():
			if v:
				self.__dict__[k] = v

	def update_functions(self, **kwargs):
		for k, v in kwargs.items():
			self.func_dict[k] = v

	def iterate_over_files(self):
		for file in self.files:
			DCT = DF_ConverT(file, self.default_stencil, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
			DCT.convert(self.func_dict)
			self.update_devices_df(DCT, file)
			self.update_cabling_df(DCT, file)
		self.calculate_cordinates()

	def update_devices_df(self, DCT, file):
		ddf = DCT.update_devices()
		self.devices_merged_df = self.devices_merged_df.merge(ddf, how='outer', validate='many_to_many')

	def update_cabling_df(self, DCT, file):
		cdf = DCT.update_cablings(**self.__dict__)
		self.cabling_merged_df = self.cabling_merged_df.merge(cdf, how='outer', validate='many_to_many')

	def calculate_cordinates(self):
		CXY = CalculateXY(self.devices_merged_df, self.default_x_spacing, self.default_y_spacing)
		CXY.calc()
		self.df_dict = {'Devices': CXY.df, 'Cablings': self.cabling_merged_df }



# --------------------------------------------- 
# Data Frame Converter
# --------------------------------------------- 
class DF_ConverT():

	def __init__(self, file, 
		default_stencil, 
		line_pattern_style_separation_on, 
		line_pattern_style_shift_no,
		):
		self.file = file
		self.full_df = nt.read_xl(file)
		file = file.split("/")[-1].split("\\")[-1]
		# self.hierarchical_order = get_hierarchical_order(file)
		# self.device_type = get_sw_type(file)
		self.self_device = file.split("-clean")[0].split(".")[0]
		#
		self.stencils = default_stencil
		self.line_pattern_style_separation_on = line_pattern_style_separation_on
		self.line_pattern_style_shift_no = line_pattern_style_shift_no


	def convert(self, func_dict):
		# physical
		df = get_physical_if_up(self.full_df['physical'])
		df = get_physical_if_relevants(df)
		# vlan
		vlan_df = get_vlan_if_up(self.full_df['vlan'])
		vlan_df = get_vlan_if_relevants(vlan_df)
		#
		for k, f in func_dict.items():
			df[k] = f(df)
		self.patterns = get_patterns(df, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
		df = update_pattern(df, self.patterns, self.line_pattern_style_separation_on)
		#
		self.u_ph_df = df
		self.vlan_df = vlan_df


	def update_cablings(self, **default_dic):
		self.C = ADevCablings(self.self_device, **default_dic)
		for k, v in self.u_ph_df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.C.add_to_cablings(**kwargs)
		df = self.C.cabling_dataframe()
		return df

	def update_devices(self):
		self.D = AdevDevices(self.stencils)
		for k, v in self.u_ph_df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.D.add_to_devices(**kwargs)
		self.D.device_dataframe()
		self.D.add_vlan_info(self.vlan_df)
		return self.D.merged_df



# --------------------------------------------- 
# Co-ordinate calculator
# --------------------------------------------- 
class CalculateXY():

	def __init__(self, dev_df, default_x_spacing, default_y_spacing):
		self.df = dev_df
		#
		self.spacing_x = default_x_spacing
		self.spacing_y = default_y_spacing
		#


	def calc(self):
		self.sort()
		self.count_of_ho()
		self.update_ys()
		self.update_xs()

	def sort(self):
		self.df.sort_values(by=['hierarchical_order', 'hostname'], inplace=True)

	def count_of_ho(self):
		self.ho_dict = {}
		vc = self.df['hierarchical_order'].value_counts()
		for ho, c in vc.items():
			self.ho_dict[ho] = c

	# -----------------------------------------------
	def calc_ys(self):
		i, y = 0, {}
		for ho in sorted(self.ho_dict):
			for r in range(1, 3):
				if self.ho_dict.get(ho+r):
					c = self.ho_dict[ho+r]
					next_i = c/2 * self.spacing_y
					break
			y[ho] = i
			i = next_i
		y = self.inverse_y(y)
		return y

	def inverse_y(self, y):
		return {k: max(y.values()) - v+2 for k, v in y.items()}

	def get_y(self, ho): return self.y[ho]

	def update_ys(self):
		self.y = self.calc_ys()
		self.df['y-axis'] = self.df['hierarchical_order'].apply(self.get_y)
		return self.df

	# -----------------------------------------------

	def get_x(self, ho): 
		for i, v in enumerate(sorted(self.xs[ho])):
			value = self.xs[ho][v]
			break
		del(self.xs[ho][v])
		return value

	def calc_xs(self):
		xs = {}
		middle = self.full_width/2
		halfspacing = self.spacing_x/2
		for ho in sorted(self.ho_dict):
			if not xs.get(ho):
				xs[ho] = {}
			c = self.ho_dict[ho]
			b = middle - (c/2*self.spacing_x) - halfspacing
			for i, x in enumerate(range(c)):
				pos = x*self.spacing_x + b 
				xs[ho][i] = pos
		# print(xs)
		return xs

	def update_xs(self):
		self.full_width = (max(self.ho_dict.values())+2) * self.spacing_x
		self.xs = self.calc_xs()
		self.df['x-axis'] = self.df['hierarchical_order'].apply(self.get_x)
		return self.df


# --------------------------------------------- 
