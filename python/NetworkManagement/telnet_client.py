import telnetlib
import socket
import re

#PROMPT_USERNAME = ['sername: ', 'ogin: ']
#PROMPT_USERNAME = ['aa: '.encode(), 'bb: '.encode()]
PROMPT_USERNAME = ['sername: '.encode(), 'ogin: '.encode(), 'sername:'.encode()]
#PROMPT_PASSWORD = ['assword: ']
PROMPT_PASSWORD = ['assword: '.encode(), 'assword:'.encode()]
PROMPT_RAW = ['#', '>', ']', '$']
PROMPT_RAW_B = ['#'.encode(), '>'.encode(), ']'.encode(), '\$'.encode()]
PROMPT_PREFIX_SUFFIX = '[]#<>$'
#USERNAME_SH = 'admin'
#PASSWORD_SH = 'wiscom@sh'
#USERNAME_SH = 'xiangwc'
#PASSWORD_SH = 'QWERasdf1234=-'
USERNAME_SH = 'xiangwenchao'
PASSWORD_SH = 'Check1234'
#USERNAME_FZ = 'xiangwc'
#PASSWORD_FZ = 'QWERasdf1234=-'


class TelnetClient:
    
    def __init__(self, host, port=23, timeout=10):
        self.host_info = dict(host=host, port=port)
        self.timeout = timeout
        self.err_type = None
        self.hostname = ''
        self.err_prompt = ''
    
    def comm_connect(self):
        try:
            self.tn = telnetlib.Telnet(self.host_info['host'], port=23, timeout=3)
            #self.tn = telnetlib.Telnet(Host, port=23, timeout=3)
        except (socket.timeout, OSError, NameError) as e:
            self.tn = None
            self.err_type = str(e)
            return

        self.tn.set_debuglevel(0)
        out = self.tn.expect(PROMPT_USERNAME, timeout=self.timeout)
        if out[0] < 0:
            self.err_type = 'Unrecognized prompt'
            self.err_prompt = out[2]
            self.close()
            return
        self.tn.write((USERNAME_SH + '\n').encode())
        out = self.tn.expect(PROMPT_PASSWORD, timeout=self.timeout)
        if out[0] < 0:
            self.err_type = 'Unrecognized prompt'
            self.err_prompt = out[2]
            self.close()
            return
        self.tn.write((PASSWORD_SH + '\n').encode())
        out = self.tn.expect(PROMPT_RAW_B, timeout=self.timeout)	
        if out[0] < 0:
            self.err_type = 'Wrong username or password'
            self.err_prompt = out[2]
            self.close()
            return
        self.hostname = self.get_raw_name()
        self.raw_prompt = [re.compile(r"{hostname}.*{prompt}".format(hostname=self.hostname[:20], prompt=_).encode()) for _ in PROMPT_RAW]

    def get_raw_name(self):
        self.tn.write('\n'.encode())
        out = self.tn.expect(PROMPT_RAW_B, timeout=self.timeout)	
        if out[0] < 0:
            self.err_prompt = out[2]
        prompt = out[2].decode().split('\r\n')[-1].strip()
        return prompt.strip(PROMPT_PREFIX_SUFFIX)

    def isConnected(self):
        if self.tn is None:
            return False
        self.tn.write('\n'.encode())
        out = self.tn.expect(PROMPT_RAW_B, timeout=self.timeout)	
        return True if out[0] >= 0 else False

    def isEnable(self, cmd):
        return cmd in ['en']

    def send_cmd(self, cmd):
        self.tn.write((cmd+'\n').encode())
        if self.isEnable(cmd):
            out = self.tn.expect(PROMPT_PASSWORD, timeout=self.timeout)
        else:
            #out = self.tn.expect([re.compile('#'.encode())], timeout=self.timeout)
            out = self.tn.expect(self.raw_prompt, timeout=self.timeout+20)
            #out = self.tn.expect(PROMPT_RAW_B, timeout=self.timeout)
        #print('matched index is:%s, out is:%s'%(out[0], out[2].decode()))
        return out[2].decode()

    def close(self):
        self.tn.close()
        self.tn = None

if __name__ == '__main__':
    Host = '172.25.254.148'
    cmds = [
        'conf t',
        'logging source-interface Vlan666',
        'logging 129.25.98.33',
        'logging trap warnings',
        'exit',
        'wr'
    ]
    tc = TelnetClient(Host)
    tc.comm_connect()
    if tc.isConnected():
        print('Success to connect to {hostname}({host})'.format(hostname=tc.hostname, host=Host))
        for cmd in cmds:
            tc.send_cmd(cmd)
        tc.close()
    else: 
        print('Fail to connect to {hostname}({host}), err_type is {err_type}, err_prompt is {err_prompt}'.format(hostname=tc.hostname, host=Host, err_type=tc.err_type, err_prompt=tc.err_prompt))
