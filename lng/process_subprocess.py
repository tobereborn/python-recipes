# -*- coding: utf-8 -*-
import subprocess


def main():
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=max\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code: ', p.returncode)


if __name__ == '__main__':
    main()
