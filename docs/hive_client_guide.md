#1. Install Anaconda:
   Follow anaconda_guide.md to set up python environment

#2. Create drp01 Env:
   sudo conda create -n drp01 python=2.7

#3. OS request:
   sudo apt-get install libsasl2-dev libldap2-dev

#4. Pip Install:
#4.1 pyhs2 client
   optionally, source active drp01
   sudo pip install -i https://pypi.douban.com/simple pyhs2
   optionally, source deactive drp01
#4.2 impyla client
   optionally, source active drp01
   sudo pip install -i https://pypi.douban.com/simple thrift_sasl
   sudo pip install -i https://pypi.douban.com/simple sasl
   sudo pip install -i https://pypi.douban.com/simple impyla
   optionally, source deactive drp01

   