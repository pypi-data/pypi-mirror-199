from dataclasses import dataclass
import subprocess

@dataclass
class GridPanelParameters:
	cols:int
	rows:int
	name:str
	version:str
	copyright:str
	fab_house:str
	panel_name:str = None # = f'PP-{panel_cols}x{panel_rows}'
	spacing:str = '2'
	framing:str = 'railstb'

	def row(self, index:int) -> int:
		return int(index / self.cols)

	def col(self, index:int) -> int:
		return index % self.cols


class _Impl:
	@staticmethod
	def make_kikit_grid_panel_command(parms:GridPanelParameters, pcb_filename:str, panel_filename:str):
		return f'''
	kikit panelize --layout 'grid; rows: {parms.rows}; cols: {parms.cols}; space: {parms.spacing}mm' \
		--copperfill solid \
		--tabs annotation \
		--cuts 'mousebites; drill: 0.5mm; spacing: 0.75mm; offset: -0.0mm' \
		--framing "{parms.framing}; width: 5mm; space: {parms.spacing}mm;" \
		--tooling "3hole; hoffset: 2.5mm; voffset: 2.5mm; size: 1.5mm" \
		--fiducials "3fid; hoffset: 5mm; voffset: 2.5mm; coppersize: 2mm; opening: 1mm;" \
		--text "simple; text: {parms.name} {parms.version} ({parms.panel_name} {parms.fab_house} {{date}}); anchor: mt; voffset: 2.5mm; hjustify: center; vjustify: center;" \
		--text2 "simple; text: {parms.name} (c) {parms.copyright}; anchor: br; hoffset: -30mm; voffset: -2.5mm; hjustify: center; vjustify: center;" \
		--text3 "simple; text: JLCJLCJLCJLC; anchor: bl; hoffset: 20mm; voffset: -2.5mm; vjustify: center; orientation: 0deg" \
		--post "millradius: 1mm" \
		{pcb_filename} {panel_filename}
	'''



class GridPaneliser:
	def __init__(self, parms:GridPanelParameters):
		self._parms = parms

		if not self._parms.panel_name:
			self._parms.panel_name = f'{self._parms.name}-{self._parms.cols}x{self._parms.rows}'


	def run(self, pcb_filename:str, panel_filename:str, verbose=False) -> int:
		kikit_command = _Impl.make_kikit_grid_panel_command(self._parms, pcb_filename=pcb_filename, panel_filename=panel_filename)

		if verbose:
			print(kikit_command)
		
		result = subprocess.run(kikit_command, shell=True)

		if verbose:
			print(f'kikit exit: {result.returncode} stdout: {result.stdout or "N/A"}')

		return result.returncode
