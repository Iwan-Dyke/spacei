up:
    docker compose up -d

down:
    docker compose down

logs:
    docker compose logs -f

topics:
    docker compose exec redpanda rpk topic create space.raw.celestrak.tle --partitions 3 --replicas 1 --topic-config retention.ms=259200000
    docker compose exec redpanda rpk topic create space.normalized.orbital_elements --partitions 3 --replicas 1 --topic-config retention.ms=259200000
    docker compose exec redpanda rpk topic create space.deadletter --partitions 3 --replicas 1 --topic-config retention.ms=1209600000

topics-list:
    docker compose exec redpanda rpk topic list
