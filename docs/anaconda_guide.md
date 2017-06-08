#1. Install Anaconda3:
sudo wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-4.2.0-Linux-x86_64.sh
   
sudo bash Anaconda3-4.2.0-Linux-x86_64.sh

Assume installation home is located at /opt/anaconda/anaconda3 ###

#2. Env:
sudo vi /etc/profile
   
export PATH="/opt/anaconda/anaconda3/bin:$PATH"
   
source /etc/profile

#3. Mirror:
https://pypi.tuna.tsinghua.edu.cn/simple
http://mirrors.aliyun.com/pypi/simple/
https://pypi.mirrors.ustc.edu.cn/simple/
http://pypi.hustunique.com/
http://pypi.sdutlinux.org/ 
http://pypi.douban.com/simple/
   
#3.1. pypi:
export http_proxy=http://proxy_url:proxy_port
export https_proxy=http://proxy_url:proxy_port
pip install -i https://pypi.douban.com/simple pkg

or 
 
sudo vi ~/.pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=mirrors.aliyun.com

#3.2. conda:

vi ~/.condarc
proxy_servers:
  https: http://proxy.xxx.com:8080
  http: http://proxy.xxx.com:8080

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --set show_channel_urls yes
conda config --set use_pip True
