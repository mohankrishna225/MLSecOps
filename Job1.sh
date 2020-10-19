if ! sudo docker ps | grep logs_for_DoS
then 
  sudo docker run -d --rm -v /root/MLSecOps/logstash/:/usr/share/logstash/mypipeline -v /var/log/httpd/:/logs/httpd/ --name logs_for_DoS logstash:7.7.1 -f /usr/share/logstash/mypipeline/mylogstash.conf
fi

while ! sudo ls /root/MLSecOps/logstash/output/ | grep web-server-logs.csv
do 
  sleep 1
done
sleep 1
sudo echo $(sudo cat /root/MLSecOps/logstash/output/web-server-logs.csv | wc -l) > old_requests