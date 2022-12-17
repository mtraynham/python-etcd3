#!/usr/bin/env sh

set -x;

host="127.0.0.1"
count=1
name_prefix="etcd-"

while getopts ":h:c:n:" opt; do
  case $opt in
    h)
      host="${OPTARG}"
      ;;
    c)
      count="${OPTARG}"
      ;;
    n)
      name_prefix="${OPTARG}"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

terminate() {
    # Send SIGINT kill to all child processes of this script
    # and then exit
    pkill -SIGINT -P $$
    exit
}

# Trap SIGINT calls and if they happen kill all processes started by
# this script with SIGINT
trap terminate INT HUP TERM

STARTING_PORT=2379

# Build cluster string
i=0
endpoints=""
cluster=""
while [ $i -lt "${count}" ]; do
  if [ $i -ne 0 ]; then
    endpoints="${endpoints},"
    cluster="${cluster},"
  fi
  client_port=$((STARTING_PORT + 2 * i))
  peer_port=$((client_port + 1))
  endpoints="${endpoints}http://${host}:${client_port}"
  cluster="${cluster}${name_prefix}${i}=http://${host}:${peer_port}"
  i=$((i + 1))
done

tmp_dir=$(mktemp -d)
echo "Writing data to ${tmp_dir}"

# Start etcd processes in background
i=0
while [ $i -lt "${count}" ]; do
  client_port=$((STARTING_PORT + 2 * i))
  peer_port=$((client_port + 1))
  etcd \
    --name "${name_prefix}${i}" \
    --data-dir "${tmp_dir}/${i}" \
    --listen-client-urls "http://${host}:${client_port}" \
    --advertise-client-urls "http://${host}:${client_port}" \
    --listen-peer-urls "http://${host}:${peer_port}" \
    --initial-advertise-peer-urls "http://${host}:${peer_port}" \
    --initial-cluster "${cluster}" \
    --initial-cluster-token tkn \
    --initial-cluster-state new &
  i=$((i + 1))
done

# Wait for healthy cluster
while true; do
  if ! etcdctl --endpoints "${endpoints}" cluster-health; then
#  if ! etcdctl --endpoints "${endpoints}" endpoint health; then
    echo "Cluster still starting..."
    sleep 2
  else
    break
  fi
done

# Wait for parent process stop
wait
