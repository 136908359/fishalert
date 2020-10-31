
class Config(object):


    listenPort = 5000
    listenHost = '0.0.0.0'

    #连接mysql
    mysql_host = '192.168.4.103'
    mysql_port = 21410
    mysql_user = 'bptest'
    mysql_password = 'bptest'
    mysql_database = 'fishalert'

    #连接mongodb
    mongo_host = '192.168.0.102'
    mongo_port = 27017


    #默认告警模板与媒介
    sendWechat = "nat.zhu,"
    sendMail = "136908359@qq.com,"
    sendDingtalk = "https://oapi.dingtalk.com/robot/send?access_token=223dce65a3640d336875de3ccb6c58fa684e1609ff68a4d131d9083bf368380c"
    secretDingtalk = "SEC569eda34d01d5a1c1ad182c63d875392a9a5382187192d8c8c7ca8adae2c7a4b"
    atDingtalk = "" 
    sendPhone = "18207420715,"
    
    template = '告警主题: {alertname}\n告警值: {value}\n告警类型: {alertType}\n告警时间: {alertAt}\n告警来源: {alertSource}'
    #prometheus_template = '告警主题: {alertname}\n告警类型: {alertType}\n告警时间: {alertAt}\n告警来源: {alertSource}'