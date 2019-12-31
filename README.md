# one-chain

See makefile to see how to launch container

To launch swarm:
```
❯ make swarm
docker network create --driver overlay net-blockchain
j9aduhtwnk2r0vg0u3ubyhpyv
docker service create --replicas 5 --endpoint-mode dnsrr --network net-blockchain --name blockchain block-node:d049c353a33
image block-node:d049c353a33 could not be accessed on a registry to record
its digest. Each node will access block-node:d049c353a33 independently,
possibly leading to different nodes running different
versions of the image.

uwmd3xetlo751ce3ltihtvhgm
overall progress: 5 out of 5 tasks
1/5: running   [==================================================>]
2/5: running   [==================================================>]
3/5: running   [==================================================>]
4/5: running   [==================================================>]
5/5: running   [==================================================>]
verify: Service converged
```
To exec shell in one of the containers (first one in the docker ps output)
```
❯ make shell
docker exec -it $(docker ps -a -q --filter ancestor=block-node:latest --format="{{.ID}}" | head -n 1) bash
root@004f4bace643:/app# dig blockchain
```
In container see dns round-robin in action
```
; <<>> DiG 9.11.5-P4-5.1-Debian <<>> blockchain
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 48829
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;blockchain.			IN	A

;; ANSWER SECTION:
blockchain.		600	IN	A	10.0.7.4
blockchain.		600	IN	A	10.0.7.3
blockchain.		600	IN	A	10.0.7.2
blockchain.		600	IN	A	10.0.7.6
blockchain.		600	IN	A	10.0.7.5

;; Query time: 1 msec
;; SERVER: 127.0.0.11#53(127.0.0.11)
;; WHEN: Tue Dec 31 22:00:12 UTC 2019
;; MSG SIZE  rcvd: 158

root@004f4bace643:/app# exit
exit
```
As you can see all node ips of blockchain service are returned if you do a dns query on the service-name

Cleanup service and network

```
❯ make swarm-clean
docker service rm blockchain
blockchain
docker network rm net-blockchain
net-blockchain
```

# Curl or use postman or use browser
```
~/projects/one-chain/python master*
❯ curl http://localhost:8080/chain
```

[Postman Workspace](https://app.getpostman.com/join-team?invite_code=30583f7d07d91ef4e362855e92dba978)
