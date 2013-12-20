colour-carbon
=============

*colour-carbon is a wrapper around wso2 carbon command line output to add a bit of colour in 256 colour linux terminals*

## Prerequisites

* python 2.x
* 256 colour supported terminal

## Installation

clone colour-carbon git repo.

     me@lap:~$ cd  MY_CHECKOUTS
     me@lap:~/MY_CHECKOUTS$ git clone https://github.com/manuranga/colour-carbon.git
     
go to a carbon product home and run colour carbon from there

    me@lap:~/MY_CHECKOUTS$ cd ~CARBON/wso2as-4.1.0
    me@lap:~CARBON/wso2as-4.1.0$ python ~/MY_CHECKOUTS/colour-carbon/cc.py
    
## Aliases
    
add folowing function to .bashrc for quick access

```sh
rr() {
  python ~/MY_CHECKOUTS/colour-carbon/cc.py $*
}
```

then you will be able to run colour carbon by just typeing rr inside product home

    me@lap:~/MY_CHECKOUTS$ cd ~/CARBON/wso2as-4.1.0
    me@lap:~/CARBON/wso2as-4.1.0$ rr
    
## Screenshots


![Start-up](http://i.imgur.com/KKS6fbd.png "Server start up")
![Exception](http://i.imgur.com/AsfllIT.png "Exception")



## Roadmap

* start runing form any dirctory in product
* auto open browser when server starts up
* adding support to OSGi console mode
* support viewing log files
* adding a config file to change colours ect.
