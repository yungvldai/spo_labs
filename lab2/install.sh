#! /bin/bash

git clone https://github.com/cjdelisle/cjdns
cd cjdns
./do
./cjdroute --genconf > cjdroute.conf
IP="63.141.230.133:10000"
CONF="{
	\"password\":\"null\",
	\"authType\":1,
	\"trust\":9001,
	\"publicKey\":\"3cwqg8zrlcfhchv0mz9pjtclh01pqrg2rd6d3yzk3u02lnt9v490.k\"
}"
echo "Found node:"
echo "$IP: ""$CONF"
cat cjdroute.conf > conf.json
jsmin conf.json > min.json
RULE=".interfaces.UDPInterface[0].connectTo = {\"$IP\": $CONF}"
jq "$RULE" min.json >> cjdroute.conf
echo "Type \"cjdroute < cjdroute.conf\""
sudo mv cjdroute /usr/local/bin
NOW_PATH=$(pwd)
printf "./run.sh" > ../run.sh
chmod a=rwx ../run.sh
cd ..
