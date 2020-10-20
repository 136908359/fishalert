
class Config(object):


    listenPort = 5000
    listenHost = '0.0.0.0'

    #连接数据库
    host = '192.168.4.103'
    port = 21410
    user = 'bptest'
    password = 'bptest'
    database = 'fishalert'

    #默认告警模板与媒介
    sendway = 'wechat'
    sentto = 'nat.zhu'
    template = '主题: {{alertname}}\n告警值: {{value}}\n告警规则: {{rule}}\n告警时间: {{alerttime}}\n告警来源: {{source}}'