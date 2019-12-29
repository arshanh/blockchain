# one-chain

# Start server in container
~/projects/one-chain/python master*
❯ make
docker run --rm=true -p 8080:80 -d  -t blockchain:2a845dae62f
2c9b8e5797b9fe4264ab5bafa99b25578aec6e06363f0e2c44e1649ae0791476

# Can't reuse port twice
~/projects/one-chain/python master*
❯ make
docker run --rm=true -p 8080:80 -d  -t blockchain:2a845dae62f
4c44840e5cfde6cff72ff9c783326fe12ec18d45713526a47dafe137a9cd3942
docker: Error response from daemon: driver failed programming external connectivity on endpoint competent_yonath (9c613112e7fa713d6b87be07deddab83b14f8fb3da568991c1803154d5e05fc2): Bind for 0.0.0.0:8080 failed: port is already allocated.
make: *** [blockchain] Error 125

# See container running
~/projects/one-chain/python master*
❯ docker ps
CONTAINER ID        IMAGE                    COMMAND                CREATED             STATUS              PORTS                            NAMES
ce607e67ff07        blockchain:2a845dae62f   "python test_app.py"   5 hours ago         Up 5 hours          8080/tcp, 0.0.0.0:8080->80/tcp   optimistic_roentgen

# Stop container
~/projects/one-chain/python master*
❯ docker stop optimistic_roentgen
optimistic_roentgen

# Attach to stdout/stdin/stderr
~/projects/one-chain/python master*
❯ docker attach optimistic_roentgen
172.17.0.1 - - [29/Dec/2019 08:18:50] "GET / HTTP/1.1" 200 -

^C

# Exec shell in container
~/projects/one-chain/python master*
❯ docker exec -it brave_einstein /bin/bash
root@2c9b8e5797b9:/app#
root@2c9b8e5797b9:/app#
root@2c9b8e5797b9:/app#
root@2c9b8e5797b9:/app# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
        RX packets 13  bytes 1038 (1.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@2c9b8e5797b9:/app# ls
requirements.txt  test_app.py
root@2c9b8e5797b9:/app# exit
exit

# Curl or use postman or use browser
~/projects/one-chain/python master*
❯ curl http://localhost:8080/
Hey, we have Flask in a Docker container!%
