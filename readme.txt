fishalert
一款支持多告警通道、多数据源、灵活配置收敛的统一告警平台

原理：
fishalert接收到alertmsg（告警信息）后，会将告警信息存入mongodb，并且根据当前的告警信息和历史告警信息判断告警发送的与否与方式

应用方式：
启动fishalert后，用户需要将alertmsg以固定的形式发送给fishalert接口，并且在rule配置中配置告警的发送逻辑、聚合方式、唯一性标志, fishalert会根据用户配置的规则发送告警

配置优先级：
rules > alertMsg > 配置文件

alertMsg关键key：
alertname：告警的名称，唯一性标识，必带
value: 告警的值，必带
alertSource：告警的来源，选带
sendWechat：微信告警发送的用户，多个用户以，间隔，选带
sendMail：邮件告警发送的邮箱，多个邮箱以，间隔，选带
sendDingtalk：钉钉告警发送的群组url，不支持多个，选带
secretDingtalk，钉钉告警发送群组的secret，不支持多个，选带
atDingtalk：钉钉告警需要at的对象号码，多个号码以，间隔，选带
sendPhone：语音告警发送的号码，多个号码以，间隔，选带
template：自定义告警内容的模板，支持宏语法，选带


接入方式：
1）prometheus
prometheus的配置文件块加入：
alerting:
      alertmanagers:
      - static_configs:
        - targets: ["{HOST}:{PORT}"]
2）自定义告警
自定义告警内容以POST的方式发送到http://{HOST}:{PORT}即可



