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
            if isinstance(other, float) or isinstance(other, int):
                r = int(self.r * other)
                g = int(self.g * other)
                b = int(self.b * other)

                frame = Gradient.Frame(r, g, b, False)
                return frame

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

        def __eq__(self, other):
            return self.r + self.g + self.b == other.r + other.g + other.b

        def __ge__(self, other):
            return self > other or self == other

        def __le__(self, other):
            return self < other or self == other

        def __gt__(self, other):
            return self.r + self.g + self.b >= other.r + other.g + other.b

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
        """Creates and adds a frame"""
        self.add_frame(Gradient.Frame(r, g, b))

    def add_frame(self, frame: Frame):
        """Add a frame (color) to frames list"""
        self.frames.append(frame)

    def smooth(self, length: int):
        """Helps get the gradient you want"""
        if len(self.frames) > length:
            return self.frames[:length]

        if len(self.frames) > 1:
            smoothed = []

            transitions_count = len(self.frames)
            frames_in_transition = int(length / (transitions_count - 1) + 0.5)  # math.ceil
            for transition_index in range(transitions_count - 1):
                frame_slice = self.frames[transition_index:transition_index+2]

                min_frame = min(frame_slice)
                max_frame = max(frame_slice)
                difference = max_frame ^ min_frame
                frame_to_add = min_frame

                for x in range(frames_in_transition):
                    transition_level = x / (frames_in_transition - 1) if frames_in_transition > 1 else 0
                    if frame_slice.index(min_frame) == 1:
                        frame_to_add = max_frame
                        transition_level *= -1

                    smoothed.append(frame_to_add + difference * transition_level)
            return smoothed

        return self.frames

    def apply(self, text: str, style: int = 0):
        """Applies a gradient to text"""
        result = ''
        colors = self.smooth(len(text))
        for char_index in range(len(text)):
            color = colors[char_index % len(colors)]
            if style == 0:
                result += f'<c{color}>{text[char_index]}'
            elif style == 1:
                result += f'<font color="#{color}">{text[char_index]}</font>'

        if style == 0:
            result += '</c>'
        return result


if __name__ == '__main__':
    gradient = Gradient()
    gradient.create_frame()
    gradient.create_frame(255, 255, 255)
    print(gradient.apply('f' * 1000, 1))  # You can put here any string
