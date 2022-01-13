import paho.mqtt.client as mqtt
import ssl,random,time,logging
from datetime import datetime
#checker={"N":0,"NNE":22.5,"NE":45, "ENE":67.5,"E":90,"ESE":112.5,"SE":135, "SSE":157.5,"S":180,"SSO":202.5,"SO":225,"OSO":247.5,"O":270,"ONO":292.5,"NO":315,"NNO":337.5}
logging.basicConfig(filename='/var/log/Meteopublisher.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

checker={0:"N",22.5:"NNE",45:"NE", 67.5:"ENE",90:"E",112.5:"ESE",135:"SE", 157.5:"SSE",180:"S",202.5:"SSO",225:"SO",247.5:"OSO",270:"O",292.5:"ONO",315:"NO",337.5:"NNO"}
checkerKeys=list(checker.keys())
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.info("Connected with result code "+str(rc))


    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")


def on_publish(client, userdata,result):
    print(str(result))
    logging.info(str(result))
    pass
def getDirection(val):
    print(str(checkerKeys))
    resultval=min(checkerKeys, key=lambda x:abs(x-val))
    return checker[resultval]
def ArduinoGetData(stationId):
    data= dict()
    data["cur_time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["humidity"]=random.randint(80,100)
    data["temperature"]=round(random.uniform(-3.0,17.0),2)
    data["pressure"]=round(random.uniform(900.0,1040.0),2)
    data["uv"]=random.randint(0,10)
    data["cloud_coverage"]=random.randint(0,100)
    data["cloud_altitude"]=round(random.uniform(0,3700),2)
    data["precipitation"]=random.randint(0,1)
    data["wind_degree"]=round(random.uniform(0,360),2)
    data["wind_direction"]=getDirection(data["wind_degree"])
    data["wind_speed"]=random.randint(0,8)
    data["station_id"]=stationId
    print(str(data))
    logging.info("Generate data: OK")
    return str(data)

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish=on_publish
client.tls_set("/home/toto/ca2.crt")
#client.tls_insecure_set(True)

client.connect("infra", 8883, 100)
while(True):
    #PARIS
    client.publish("meteo/meteo",ArduinoGetData(1),1)
    #STRASBOURG
    client.publish("meteo/meteo",ArduinoGetData(2),1)
    #REIMS
    client.publish("meteo/meteo",ArduinoGetData(3),1)
    time.sleep(3*60*60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()