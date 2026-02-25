import zmq

c = zmq.Context(); s = c.socket(zmq.REP)
s.connect("tcp://broker:5556")

tasks = []
while 1:
    m = s.recv_string()
    parts = m.split(":", 1)
    cmd = parts[0].upper()
    resp = "ERROR"
    if cmd == "ADD" and len(parts) > 1:
        tasks.append(parts[1])
        resp = "OK"
    elif cmd == "REMOVE" and len(parts) > 1:
        a = parts[1]
        if a.isdigit():
            i = int(a)
            if 0 <= i < len(tasks):
                tasks.pop(i); resp = "OK"
            else:
                resp = "ERROR"
        else:
            try:
                tasks.remove(a); resp = "OK"
            except ValueError:
                resp = "ERROR"
    elif cmd == "LIST":
        resp = "\n".join(f"{i}:{t}" for i,t in enumerate(tasks)) or "EMPTY"
    s.send_string(resp)

