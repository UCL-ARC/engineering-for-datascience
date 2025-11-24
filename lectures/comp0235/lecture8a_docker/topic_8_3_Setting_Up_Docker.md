# Setting up Docker

In order to experiment with containers, you will need to install Docker on a system you have access to:

1. Personal Laptop: Docker Desktop is available for Linux, Macintosh and Windows from [The Docker Website](https://www.docker.com/). Download and run the installer.

2. Remote system running Linux (Condenser, AWS Cloud, VM on your laptop) - "Server" guide here [Install Docker Engine](https://docs.docker.com/engine/install/).

## Walk through of installing Docker on a Linux server running Alma Linux 9.2

*(This also applies to Red Hat Enterprise Linux 9.x, CentOS Stream, Rocky Linux 9.x or other RHEL derivative)*

First, become `root`:
```
[ec2-user@ip-10-0-101-165 ~]$ sudo su -
Last login: Tue Jul 25 15:34:37 UTC 2023 on pts/0
[root@ip-10-0-101-165 ~]#
```
Then add the Docker repository to `dnf`: 
```
[root@ip-10-0-101-165 ~]# dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
Adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
```

Then use `dnf` to install Docker. Make sure that the repository GPG fingerprint is "`060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`":
```
[root@ip-10-0-101-165 ~]# dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
Docker CE Stable - x86_64                       178 kB/s |  30 kB     00:00    
Dependencies resolved.
================================================================================
 Package                      Arch   Version             Repository        Size
================================================================================
Installing:
 containerd.io                x86_64 1.6.21-3.1.el9      docker-ce-stable  33 M
 docker-buildx-plugin         x86_64 0.11.2-1.el9        docker-ce-stable  13 M
 docker-ce                    x86_64 3:24.0.5-1.el9      docker-ce-stable  24 M
 docker-ce-cli                x86_64 1:24.0.5-1.el9      docker-ce-stable 7.1 M
 docker-compose-plugin        x86_64 2.20.2-1.el9        docker-ce-stable  13 M
Installing dependencies:
 container-selinux            noarch 3:2.205.0-1.el9_2   appstream         50 k
 docker-ce-rootless-extras    x86_64 24.0.5-1.el9        docker-ce-stable 3.9 M
 fuse-common                  x86_64 3.10.2-5.el9        baseos           8.0 k
 fuse-overlayfs               x86_64 1.11-1.el9_2        appstream         71 k
 fuse3                        x86_64 3.10.2-5.el9        appstream         53 k
 fuse3-libs                   x86_64 3.10.2-5.el9        appstream         91 k
 iptables-libs                x86_64 1.8.8-6.el9_1       baseos           398 k
 iptables-nft                 x86_64 1.8.8-6.el9_1       baseos           185 k
 libibverbs                   x86_64 44.0-2.el9          baseos           377 k
 libnetfilter_conntrack       x86_64 1.0.9-1.el9         baseos            58 k
 libnfnetlink                 x86_64 1.0.1-21.el9        baseos            29 k
 libnftnl                     x86_64 1.2.2-1.el9         baseos            83 k
 libpcap                      x86_64 14:1.10.0-4.el9     baseos           172 k
 libslirp                     x86_64 4.4.0-7.el9         appstream         68 k
 policycoreutils-python-utils noarch 3.5-1.el9           appstream         71 k
 slirp4netns                  x86_64 1.2.0-3.el9         appstream         45 k

Transaction Summary
================================================================================
Install  21 Packages

Total download size: 95 M
Installed size: 377 M
Is this ok [y/N]: y
Downloading Packages:
(1/21): container-selinux-2.205.0-1.el9_2.noarc 997 kB/s |  50 kB     00:00    
(2/21): fuse3-3.10.2-5.el9.x86_64.rpm           851 kB/s |  53 kB     00:00    
(3/21): fuse-overlayfs-1.11-1.el9_2.x86_64.rpm  724 kB/s |  71 kB     00:00    
(4/21): fuse3-libs-3.10.2-5.el9.x86_64.rpm      1.5 MB/s |  91 kB     00:00    
(5/21): libslirp-4.4.0-7.el9.x86_64.rpm         1.4 MB/s |  68 kB     00:00    
(6/21): policycoreutils-python-utils-3.5-1.el9. 3.3 MB/s |  71 kB     00:00    
(7/21): fuse-common-3.10.2-5.el9.x86_64.rpm     588 kB/s | 8.0 kB     00:00    
(8/21): slirp4netns-1.2.0-3.el9.x86_64.rpm      2.1 MB/s |  45 kB     00:00    
(9/21): iptables-nft-1.8.8-6.el9_1.x86_64.rpm   8.2 MB/s | 185 kB     00:00    
(10/21): iptables-libs-1.8.8-6.el9_1.x86_64.rpm 9.7 MB/s | 398 kB     00:00    
(11/21): libnetfilter_conntrack-1.0.9-1.el9.x86 4.1 MB/s |  58 kB     00:00    
(12/21): libnfnetlink-1.0.1-21.el9.x86_64.rpm   6.1 MB/s |  29 kB     00:00    
(13/21): libibverbs-44.0-2.el9.x86_64.rpm       8.2 MB/s | 377 kB     00:00    
(14/21): libnftnl-1.2.2-1.el9.x86_64.rpm        5.2 MB/s |  83 kB     00:00    
(15/21): libpcap-1.10.0-4.el9.x86_64.rpm        1.8 MB/s | 172 kB     00:00    
(16/21): docker-buildx-plugin-0.11.2-1.el9.x86_  24 MB/s |  13 MB     00:00    
(17/21): docker-ce-24.0.5-1.el9.x86_64.rpm       36 MB/s |  24 MB     00:00    
(18/21): docker-ce-cli-24.0.5-1.el9.x86_64.rpm   22 MB/s | 7.1 MB     00:00    
(19/21): containerd.io-1.6.21-3.1.el9.x86_64.rp  31 MB/s |  33 MB     00:01    
(20/21): docker-ce-rootless-extras-24.0.5-1.el9  11 MB/s | 3.9 MB     00:00    
(21/21): docker-compose-plugin-2.20.2-1.el9.x86  33 MB/s |  13 MB     00:00    
--------------------------------------------------------------------------------
Total                                            43 MB/s |  95 MB     00:02     
Docker CE Stable - x86_64                        35 kB/s | 1.6 kB     00:00    
Importing GPG key 0x621E9F35:
 Userid     : "Docker Release (CE rpm) <docker@docker.com>"
 Fingerprint: 060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35
 From       : https://download.docker.com/linux/centos/gpg
Is this ok [y/N]: y
Key imported successfully
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                        1/1 
  Installing       : docker-compose-plugin-2.20.2-1.el9.x86_64             1/21 
  Running scriptlet: docker-compose-plugin-2.20.2-1.el9.x86_64             1/21 
  Installing       : fuse3-libs-3.10.2-5.el9.x86_64                        2/21 
  Installing       : docker-buildx-plugin-0.11.2-1.el9.x86_64              3/21 
  Running scriptlet: docker-buildx-plugin-0.11.2-1.el9.x86_64              3/21 
  Installing       : docker-ce-cli-1:24.0.5-1.el9.x86_64                   4/21 
  Running scriptlet: docker-ce-cli-1:24.0.5-1.el9.x86_64                   4/21 
  Installing       : libnftnl-1.2.2-1.el9.x86_64                           5/21 
  Installing       : libnfnetlink-1.0.1-21.el9.x86_64                      6/21 
  Installing       : libnetfilter_conntrack-1.0.9-1.el9.x86_64             7/21 
  Installing       : libibverbs-44.0-2.el9.x86_64                          8/21 
  Installing       : libpcap-14:1.10.0-4.el9.x86_64                        9/21 
  Installing       : iptables-libs-1.8.8-6.el9_1.x86_64                   10/21 
  Installing       : iptables-nft-1.8.8-6.el9_1.x86_64                    11/21 
  Running scriptlet: iptables-nft-1.8.8-6.el9_1.x86_64                    11/21 
  Installing       : fuse-common-3.10.2-5.el9.x86_64                      12/21 
  Installing       : fuse3-3.10.2-5.el9.x86_64                            13/21 
  Installing       : fuse-overlayfs-1.11-1.el9_2.x86_64                   14/21 
  Running scriptlet: fuse-overlayfs-1.11-1.el9_2.x86_64                   14/21 
  Installing       : policycoreutils-python-utils-3.5-1.el9.noarch        15/21 
  Running scriptlet: container-selinux-3:2.205.0-1.el9_2.noarch           16/21 
  Installing       : container-selinux-3:2.205.0-1.el9_2.noarch           16/21 
  Running scriptlet: container-selinux-3:2.205.0-1.el9_2.noarch           16/21 
  Installing       : containerd.io-1.6.21-3.1.el9.x86_64                  17/21 
  Running scriptlet: containerd.io-1.6.21-3.1.el9.x86_64                  17/21 
  Installing       : libslirp-4.4.0-7.el9.x86_64                          18/21 
  Installing       : slirp4netns-1.2.0-3.el9.x86_64                       19/21 
  Installing       : docker-ce-rootless-extras-24.0.5-1.el9.x86_64        20/21 
  Running scriptlet: docker-ce-rootless-extras-24.0.5-1.el9.x86_64        20/21 
  Installing       : docker-ce-3:24.0.5-1.el9.x86_64                      21/21 
  Running scriptlet: docker-ce-3:24.0.5-1.el9.x86_64                      21/21 
  Running scriptlet: container-selinux-3:2.205.0-1.el9_2.noarch           21/21 
  Running scriptlet: docker-ce-3:24.0.5-1.el9.x86_64                      21/21 
  Verifying        : container-selinux-3:2.205.0-1.el9_2.noarch            1/21 
  Verifying        : fuse-overlayfs-1.11-1.el9_2.x86_64                    2/21 
  Verifying        : fuse3-3.10.2-5.el9.x86_64                             3/21 
  Verifying        : fuse3-libs-3.10.2-5.el9.x86_64                        4/21 
  Verifying        : libslirp-4.4.0-7.el9.x86_64                           5/21 
  Verifying        : policycoreutils-python-utils-3.5-1.el9.noarch         6/21 
  Verifying        : slirp4netns-1.2.0-3.el9.x86_64                        7/21 
  Verifying        : fuse-common-3.10.2-5.el9.x86_64                       8/21 
  Verifying        : iptables-libs-1.8.8-6.el9_1.x86_64                    9/21 
  Verifying        : iptables-nft-1.8.8-6.el9_1.x86_64                    10/21 
  Verifying        : libibverbs-44.0-2.el9.x86_64                         11/21 
  Verifying        : libnetfilter_conntrack-1.0.9-1.el9.x86_64            12/21 
  Verifying        : libnfnetlink-1.0.1-21.el9.x86_64                     13/21 
  Verifying        : libnftnl-1.2.2-1.el9.x86_64                          14/21 
  Verifying        : libpcap-14:1.10.0-4.el9.x86_64                       15/21 
  Verifying        : containerd.io-1.6.21-3.1.el9.x86_64                  16/21 
  Verifying        : docker-buildx-plugin-0.11.2-1.el9.x86_64             17/21 
  Verifying        : docker-ce-3:24.0.5-1.el9.x86_64                      18/21 
  Verifying        : docker-ce-cli-1:24.0.5-1.el9.x86_64                  19/21 
  Verifying        : docker-ce-rootless-extras-24.0.5-1.el9.x86_64        20/21 
  Verifying        : docker-compose-plugin-2.20.2-1.el9.x86_64            21/21 

Installed:
  container-selinux-3:2.205.0-1.el9_2.noarch                                    
  containerd.io-1.6.21-3.1.el9.x86_64                                           
  docker-buildx-plugin-0.11.2-1.el9.x86_64                                      
  docker-ce-3:24.0.5-1.el9.x86_64                                               
  docker-ce-cli-1:24.0.5-1.el9.x86_64                                           
  docker-ce-rootless-extras-24.0.5-1.el9.x86_64                                 
  docker-compose-plugin-2.20.2-1.el9.x86_64                                     
  fuse-common-3.10.2-5.el9.x86_64                                               
  fuse-overlayfs-1.11-1.el9_2.x86_64                                            
  fuse3-3.10.2-5.el9.x86_64                                                     
  fuse3-libs-3.10.2-5.el9.x86_64                                                
  iptables-libs-1.8.8-6.el9_1.x86_64                                            
  iptables-nft-1.8.8-6.el9_1.x86_64                                             
  libibverbs-44.0-2.el9.x86_64                                                  
  libnetfilter_conntrack-1.0.9-1.el9.x86_64                                     
  libnfnetlink-1.0.1-21.el9.x86_64                                              
  libnftnl-1.2.2-1.el9.x86_64                                                   
  libpcap-14:1.10.0-4.el9.x86_64                                                
  libslirp-4.4.0-7.el9.x86_64                                                   
  policycoreutils-python-utils-3.5-1.el9.noarch                                 
  slirp4netns-1.2.0-3.el9.x86_64                                                

Complete!
```
Start Docker:
```
[root@ip-10-0-101-165 ~]# systemctl start docker
```
## Testing Docker (on your laptop or on a Linux server):

First run the "hello-world" example:
```
[root@ip-10-0-101-165 ~]# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
719385e32844: Pull complete 
Digest: sha256:926fac19d22aa2d60f1a276b66a20eb765fbeea2db5dbdaafeb456ad8ce81598
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

```
Now let's try something more adventurous - let's pull an image for a Docker container for the [Julia Programming Language](https://julialang.org/) and run it:
```
[root@ip-10-0-101-165 ~]# docker run -it --rm julia
Unable to find image 'julia:latest' locally
latest: Pulling from library/julia
faef57eae888: Pull complete 
06944e2a3b3e: Pull complete 
86dddcf3e65c: Pull complete 
72cfdb150b09: Pull complete 
Digest: sha256:85ddd1471eee4a65bb3369ffba005c7f4838c5e375b6d66f05536f7c9813d184
Status: Downloaded newer image for julia:latest
               _
   _       _ _(_)_     |  Documentation: https://docs.julialang.org
  (_)     | (_) (_)    |
   _ _   _| |_  __ _   |  Type "?" for help, "]?" for Pkg help.
  | | | | | | |/ _` |  |
  | | |_| | | | (_| |  |  Version 1.9.2 (2023-07-05)
 _/ |\__'_|_|_|\__'_|  |  Official https://julialang.org/ release
|__/                   |

julia> function picalc(numsteps)
         slice = 1.0/numsteps

         sum = 0.0

         @simd for i = 1:numsteps
           x = (i - 0.5) * slice
           sum = sum + (4.0/(1.0 + x^2))
         end

         return sum * slice

       end

picalc (generic function with 1 method)

julia> picalc(1000000)
3.1415926535898793

julia> 
```

*Note* - on RHEL derivatives, you need to tell Systemd to start Docker on boot if you want it to.

```
[root@ip-10-0-101-165 ~]# systemctl enable docker.service
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.
[root@ip-10-0-101-165 ~]# systemctl enable containerd.service
Created symlink /etc/systemd/system/multi-user.target.wants/containerd.service → /usr/lib/systemd/system/containerd.service.
[root@ip-10-0-101-165 ~]#
``` 
