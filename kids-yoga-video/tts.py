import ctypes, wave, espeakng_loader as e
L=ctypes.CDLL(e.get_library_path())
SR=L.espeak_Initialize(1,0,e.get_data_path().encode(),0)
buf=bytearray()
CB=ctypes.CFUNCTYPE(ctypes.c_int,ctypes.POINTER(ctypes.c_short),ctypes.c_int,ctypes.c_void_p)
def cb(w,n,ev):
    if n>0: buf.extend(ctypes.string_at(w,n*2))
    return 0
_cb=CB(cb);L.espeak_SetSynthCallback(_cb)
L.espeak_SetVoiceByName(b"en-us+f5")
L.espeak_SetParameter(1,158,0)  # rate
L.espeak_SetParameter(3,80,0);L.espeak_SetParameter(4,70,0)   # pitch high
def say(text,path):
    buf.clear();t=text.encode()
    L.espeak_Synth(t,len(t)+1,0,0,0,0x1000,None,None);L.espeak_Synchronize()
    with wave.open(path,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(bytes(buf))
    return len(buf)/2/SR
if __name__=='__main__':print(say("Hello kids! Let's do yoga together!","t.wav"),SR)
