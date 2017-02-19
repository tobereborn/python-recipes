#1. Install Anaconda:
   Follow anaconda_guide.md to set up python environment

#2. Create drp01 Env:
   sudo conda create -n drp01 python=2.7

#3. OS request:
   sudo apt-get install libatlas-dev python-dev gfortran pkg-config libfreetype6-dev cython

#4. Pip Install:
   optionally, source active drp01
   
   sudo pip install -i https://pypi.douban.com/simple CPthon
   sudo pip install -i https://pypi.douban.com/simple numpy
   sudo pip install -i https://pypi.douban.com/simple zipline
   sudo pip install -i https://pypi.douban.com/simple matplotlib
   
   optionally, source deactive drp01

   Or, sudo conda install -c quantopian zipline, it may fail due to network issue

#5. Ingest data
   sudo weget https://s3.amazonaws.com/quantopian-public-zipline-data/quandl
   
   source active drp01
   
   run and abort zipline ingest -b quandl
   extract quandl.tar to /home/$USER/.zipline/data/quandl/yyy-mm-dd-xxxxx/
   
   source deactive drp01

#6. Run Algorithm:
    source active drp01
    
    zipline run -f ../lib/python2.7/site-packages/zipline/examples/buyapple.py -b quandl --start 2000-1-1 --end 2014-1-1 -o buyapple_out.pickle
    
    source deactive drp01