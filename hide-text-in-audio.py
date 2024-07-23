import wave

def help():
  print("\033[92mHide Your Secret Message in Audio Wave File.\033[0m")

def em_audio(af, string, output):
  print("Please wait...")
  waveaudio = wave.open(af, mode='rb')
  frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
  string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
  bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
  for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
  frame_modified = bytes(frame_bytes)
  with wave.open(output, 'wb') as fd:
    fd.setparams(waveaudio.getparams())
    fd.writeframes(frame_modified)
  waveaudio.close()
  print("Done...")

def ex_msg(af):
    print ("Please wait...")
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    msg = string.split("###")[0]
    print("Your Secret Message is: \033[1;91m"+msg+"\033[0m")
    waveaudio.close()

def main():
  help()
  af = input("Enter the path to the audio file: ")
  string = input("Enter your secret message: ")
  output = input("Enter the output file path and name: ")
  try:
    em_audio(af, string, output)
    ex_msg(output)
  except:
    print("Something went wrong!! try again")



if __name__ == "__main__":
  main()