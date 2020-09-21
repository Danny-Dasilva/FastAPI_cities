for i in {1..100}; do curl -X POST "http://localhost:5700/task/run/Joe/$i" -H  "accept: application/json"; done
#for i in {1..1000}; do echo $i; done
