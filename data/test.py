import wave
import struct

def clamp(x):
    if x > 0x7fff:
        return 0x7fff
    elif x < -0x7fff:
        return -0x7fff
    else:
        return x

obj = wave.open("sample2.wav", "r")
channels = obj.getnchannels()
width = obj.getsampwidth()
freq = obj.getframerate()
frames = obj.readframes(obj.getnframes())
N = int(len(frames) / width)
frames = struct.unpack(f"<{N}h", frames)

new_obj = wave.open("new.wav", "w")
new_obj.setnchannels(channels)
new_obj.setsampwidth(width)
new_obj.setframerate(freq)

frames = tuple([clamp(x*1000) for x in frames])

data = struct.pack(f'<{N}h', *frames)
new_obj.writeframesraw(bytes(data))