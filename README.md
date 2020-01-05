# one-chain

See makefile to see how to launch container

To launch stack:
```
❯ make stack
docker network create --driver overlay --attachable net-blockchain
l606ueujbzd5876ucwqjoxvw7
docker stack deploy --compose-file docker-compose.yml  onechain
Creating service onechain_blockchain
```

Clean up stack and network
```
❯ make stack-clean
docker stack rm onechain
Removing service onechain_blockchain
docker network rm net-blockchain
net-blockchain
```

# Curl or use postman or use browser
```
~/projects/one-chain/python master*
❯ curl http://localhost:8080/chain
```

[Postman Workspace](https://app.getpostman.com/join-team?invite_code=30583f7d07d91ef4e362855e92dba978)
