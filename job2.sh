declare -i old=$(sudo cat ../1\ Activate\ Logstash/old_requests)
while :
do
  declare -i all=$(sudo cat /root/MLSecOps/logstash/output/web-server-logs.csv | wc -l)
  new=$[ $all - $old ]
  if [ $new -ge 200 ]
  then 
     sudo echo $all > ../1\ Activate\ Logstash/old_requests
     break
  fi
  sleep 2
done