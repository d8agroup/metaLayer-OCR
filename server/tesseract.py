import Image
import subprocess
import os

class Tesser_General_Exception(Exception):
	pass

class Tesser_Invalid_Filetype(Tesser_General_Exception):
	pass


class Tesseract:
	def __init__(self, image_id, tesseract_exe, scratch_dir, clean_up):
		self.image_id = image_id
		self.tesseract_exe = tesseract_exe
		self.scratch_dir = scratch_dir		
		self.clean_up = clean_up

	def _call_tesseract(self, input_filename, output_filename):
		"""Calls external tesseract.exe on input file (restrictions on types),
		outputting output_filename+'txt'"""
		args = [self.tesseract_exe, input_filename, output_filename]
		proc = subprocess.Popen(args)
		retcode = proc.wait()
		if retcode!=0:
			self.check_for_errors()
	
	def image_to_string(self, im):
		"""Converts im to file, applies tesseract, and fetches resulting text.
		If cleanup=True, delete scratch files after operation."""
		image_name = "%s.bmp" % self.image_id
		scratch_image_name = os.path.join(self.scratch_dir, image_name)
		scratch_text_name_root = os.path.join(self.scratch_dir, self.image_id)
		try:
			self.image_to_scratch(im, scratch_image_name)
			self._call_tesseract(scratch_image_name, scratch_text_name_root)
			text = self.retrieve_text(scratch_text_name_root)
		finally:
			if self.clean_up:
				self.perform_cleanup(scratch_image_name, scratch_text_name_root)
		return text
	
	def check_for_errors(self, logfile = "tesseract.log"):
		inf = file(logfile)
		text = inf.read()
		inf.close()
		# All error conditions result in "Error" somewhere in logfile
		if text.find("Error") != -1:
			raise Tesser_General_Exception, text
		
	def image_to_scratch(self, im, scratch_image_name):
		"""Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
		im.save(scratch_image_name, dpi=(200,200))
	
	def	retrieve_text(self, scratch_text_name_root):
		inf = file(scratch_text_name_root + '.txt')
		text = inf.read()
		inf.close()
		return text
	
	def perform_cleanup(self, scratch_image_name, scratch_text_name_root):
		"""Clean up temporary files from disk"""
		for name in (scratch_image_name, scratch_text_name_root + '.txt', "tesseract.log"):
			try:
				os.remove(name)
			except OSError:
				pass	
			
