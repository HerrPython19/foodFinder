import subprocess, os

running = True
p = subprocess.Popen(["python","evolve.py","-saved"])
p.wait()
print "Done"
