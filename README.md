# Lab #3: Microservices & Hazelcast

| Labs | Completion Status |
| -- | -- |
| Lab #1: Microservice Basics | ✅ |
| Lab #2: Hazelcast Basics | ✅ |
| Lab #3: Microservices & Hazelcast | ✅ |

### Run Project
```bash
# Start 3 Instances of Hazelcast Members.
hz start

# Start Facade-Service.
~/facade-service $ sh start-service.sh 8080 

# Start 3 Instances of Logging-Service.
~/logging-service $ sh start-service.sh 8083 
~/logging-service $ sh start-service.sh 8084
~/logging-service $ sh start-service.sh 8085

# Start Message-Service.
~/message-service $ sh start-service.sh 8082
```