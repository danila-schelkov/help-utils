class Gradient:
	class Frame:
		def __init__(self, r: int = 0, g: int = 0, b: int = 0, check_borders: bool = True):
			if check_borders:
				if r > 255:
					r = 255
				elif r < 0:
					r = 0
				if g > 255:
					g = 255
				elif g < 0:
					g = 0
				if b > 255:
					b = 255
				elif b < 0:
					b = 0
			
			self.r = r
			self.g = g
			self.b = b
		
		def __mul__(self, other):
			if isinstance(other, float or int):
				r = int(self.r * other)
				g = int(self.g * other)
				b = int(self.b * other)
				
				return Gradient.Frame(r, g, b, False)
			
		def __add__(self, other):
			r = self.r + other.r
			g = self.g + other.g
			b = self.b + other.b
			
			return Gradient.Frame(r, g, b)
		
		def __sub__(self, other):
			r = self.r - other.r
			g = self.g - other.g
			b = self.b - other.b
			
			return Gradient.Frame(r, g, b)
			
		def __gt__(self, other):
			if (self.r + self.g + self.b > other.r + other.g + other.b):
				return True
			return False
		
		def __lt__(self, other):
			return not (self > other)
		
		def __xor__(self, other):
			r = self.r - other.r
			g = self.g - other.g
			b = self.b - other.b
			
			return Gradient.Frame(r, g, b, False)
		
		def __or__(self, other):
			r = max(self.r, other.r) - min(self.r, other.r)
			g = max(self.g, other.g) - min(self.g, other.g)
			b = max(self.b, other.b) - min(self.b, other.b)
			
			return Gradient.Frame(r, g, b)
		
		def __bytes__(self):
			return self.r.to_bytes(1, 'big') + self.g.to_bytes(1, 'big') + self.b.to_bytes(1, 'big')
		
		def __str__(self):
			return self.__bytes__().hex()
		
		def __repr__(self):
			return str(self)
		
	def __init__(self):
		self.frames = []
		
	def create_frame(self, r: int = 0, g: int = 0, b: int = 0):
		"""Creates and add frame"""
		self.add_frame(Gradient.Frame(r, g, b))
	
	def add_frame(self, frame: Frame):
		"""Add a frame (color) to frames list"""
		self.frames.append(frame)
	
	def smooth(self, length: int):
		"""Help get needed gradient"""
		if len(self.frames) > length:
			return self.frames[:length]
		
		if len(self.frames) > 1:
			smoothed = []
			
			t_count = len(self.frames)-1
			frames_in_transition = length // t_count
			for transition_index in range(t_count):
				frame_slice = self.frames[transition_index:transition_index+2]
				difference = max(frame_slice) ^ min(frame_slice)
				for x in range(frames_in_transition):
					transition_level = x / (frames_in_transition - 1)
					smoothed.append(min(frame_slice) + difference * transition_level)
			return smoothed
		
		return self.frames
	
	def apply(self, text: str, style: int = 0):
		"""Applies a gradient to text"""
		result = ''
		colors = self.smooth(len(text))
		for char_index in range(len(text)):
			color = colors[char_index % len(colors)]
			if style == 0:
				result += f'<c{color}>'
			result += text[char_index]
		
		if style == 0:
			result += '</c>'
		return result

if __name__ == '__main__':
	gradient = Gradient()
	gradient.create_frame()
	gradient.create_frame(255, 255, 255)
	print(gradient.apply('test'))  # You can put here any string
