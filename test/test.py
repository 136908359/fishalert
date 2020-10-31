import datetime

testmsg='''
{
            "alertname":"PodMemoryUsage",
            "id":"/kubepods.slice/kubepods-besteffort.slice/kubepods-besteffort-podb6444dd6_a730_4029_98c7_f90b0819df1b.slice",
            "instance":"bluek8s11100node",
            "job":"kubernetes-cadvisor",
            "level":"1",
            "namespace":"id-prod-bluepay",
            "pod":"deployment-nas-1-7b9458674f-7wwtt",
            "type":"pod",
            "description":"kubernetes集群内deployment-nas-1-7b9458674f-7wwtt内存使用率超过80%(当前值: +Inf)",
            "summary":"内存使用率",
            "startsAt":"2020-09-11T08:12:09.994870056Z",
            "endsAt":"0001-01-01T00:00:00Z",
            "generatorURL":"http://prometheus-0:9090/graph?g0.expr=container_memory_rss%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2F+container_spec_memory_limit_bytes%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2A+100+%3E+80&g0.tab=1"
    }
'''

msg1='''
    {
        "labels":{
            "alertname":"PodMemoryUsage",
            "id":"/kubepods.slice/kubepods-besteffort.slice/kubepods-besteffort-podb6444dd6_a730_4029_98c7_f90b0819df1b.slice",
            "instance":"bluek8s11100node",
            "job":"kubernetes-cadvisor",
            "level":"1",
            "namespace":"id-prod-bluepay",
            "pod":"deployment-nas-1-7b9458674f-7wwtt",
            "type":"pod"
        },
        "annotations":{
            "description":"kubernetes集群内deployment-nas-1-7b9458674f-7wwtt内存使用率超过80%(当前值: +Inf)",
            "summary":"内存使用率"
        },
        "startsAt":"2020-09-11T08:12:09.994870056Z",
        "endsAt":"0001-01-01T00:00:00Z",
        "generatorURL":"http://prometheus-0:9090/graph?g0.expr=container_memory_rss%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2F+container_spec_memory_limit_bytes%7Bcontainer%3D%22%22%2Cjob%3D%22kubernetes-cadvisor%22%2Cnamespace%3D%22id-prod-bluepay%22%7D+%2A+100+%3E+80&g0.tab=1"
    }
'''


    
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[%(module)s,%(lineno)d] %(levelname)s "%(message)s"', datefmt='%Y-%m-%d %H:%M:%S', filemode='a')


logger = logging
#loger().warning('warning message')
