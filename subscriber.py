import paho.mqtt.client as mqtt
import ast,psycopg2,logging

logging.basicConfig(filename='/var/log/Meteosubscriber.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.info("Connected with result code "+str(rc))


    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("meteo/meteo")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    param=str(msg.payload.decode('utf-8'))
    #print(param)
    paramvalues=ast.literal_eval(param)
    InsertQuery(paramvalues)
    
    #paramvalues=dict(param)
    #values=dict(str(msg.payload))

def InsertQuery(myDict):
    print("INSERT FUNCTION")
    logging.info('Insert function')
    try:
        connection = psycopg2.connect(user="toto",
                                  password="1toto;2",
                                  host="172.19.128.107",
                                  port="5432",
                                  database="toto")
        #connection = psycopg2.connect(user="toto",password="1toto;2",host="172.19.128.107",port="5432",database="toto")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO meteo  VALUES (default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        print("CONNECT QUERY")
        logging.info("Connect query")
        record_to_insert=(myDict["cur_time"],myDict["humidity"],myDict["pressure"],myDict["temperature"],myDict["uv"],myDict["cloud_coverage"],myDict["cloud_altitude"],myDict["precipitation"],myDict["wind_direction"],myDict["wind_degree"],myDict["wind_speed"],myDict["station_id"])
        print(record_to_insert)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into meteo table")
        logging.info("Record inserted successfully")


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into meteo table", error)
        logging.error("Failed to insert record into meteo table")

    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            logging.info("PostgreSQL connection is closed")

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("/home/toto/ca2.crt")
#client.tls_insecure_set(True)

client.connect("infra", 8883, 100)
#PARIS

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()