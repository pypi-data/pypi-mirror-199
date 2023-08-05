import os

from autoappanalysis.cmd.VirtualBoxCommand import VirtualBoxCommand

class Vm():
    def __init__(self, name, user, pw):
        self.name = name
        self.user = user
        self.pw = pw    

    def __repr__(self):
        return f"VBoxVM(Name: {self.name}, User: {self.user}, PW: {self.pw})"

    def __processCmd(self, cmd):
        print(" ---CMD---> " + cmd)
        cmdResult = os.popen(cmd).read()
        if("vminfo" not in cmd and "snapshot" not in cmd):
            print(cmdResult) 
        return cmdResult

    def start(self):
        cmd = VirtualBoxCommand.VM_START.substitute(vmName=self.name)
        self.__processCmd(cmd)
    
    def execute(self, path):
        cmd = VirtualBoxCommand.GUEST_CONTROL.substitute(vmName=self.name, user=self.user, pw=self.pw, path=path)
        self.__processCmd(cmd)

    def executeWithParams(self, path, args):
        cmd = VirtualBoxCommand.GUEST_CONTROL_PARAM.substitute(vmName=self.name, user=self.user, pw=self.pw, path=path, args=args)
        self.__processCmd(cmd)