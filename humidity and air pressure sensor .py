import time
from sense_emu import SenseHat
  
from azure.iot.device import IoTHubDeviceClient, Message  
  
CONNECTION_STRING = "  "  
  
TEMPERATURE = 0  
HUMIDITY = 0
pressureLevels = "The pressure is at normal levels."
humidityLevels = "The humidity is at normal levels."
MSG_TXT = '{{\n Air pressure in psi: {pressure} \n Air pressure in bar: {barpressure} \n Humidity level: {humidity}"%"\n {pressureLevels} \n {humidityLevels}\n}}'
sense = SenseHat()

  
def iothub_client_init():  
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
    return client  
  
def iothub_client_telemetry_sample_run():  
  
    try:  
        client = iothub_client_init()  
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )  
        while True:  
            barpressure = sense.pressure
            pressure = barpressure*0.014503 
            humidity = sense.humidity   
            if pressure > 14 and pressure < 15:
                pressureLevels ="The air pressure it at normal levels and the passengers are not in danger."
            elif pressure < 14 and pressure > 10:
                pressureLevels = "The air pressure is at lower than normal levels and some passangers might experience dizziness."
            elif pressure < 10 and pressure > 7.3:
                pressureLevels ="The air pressure is at dangerously and passangers are at risk of uncosciouness."
            elif pressure < 7.3 and pressure > 4:
                pressureLevels ="THE AIR PRESSURE IS AT CRITICALLY LOW LEVELS AND THE PASSANGERS' LIFE IS AT RISK!!"
            elif pressure < 4:
                pressureLevels ="THE AIR PRESSURE IS SUBSTANTIALLY LOW AND THE PLANE HAS LOST CONTROL OF THE AIR STABILISATION"
                
            if humidity > 15 and humidity < 20:
                humidityLevels ="The humidit it at normal levels and the passengers are not in danger."
            elif humidity > 20 and humidity < 40:
                humidityLevels = "The humidity is at higher levels than normal and passangers might experience discomfort."
            elif humidity < 60 and humidity > 40:
                humidityLevels ="The humidity levels are too high!."
            elif humidity > 10 and humidity < 15:
                humidityLevels = "The humidity is lower than normal and some passengers might experience discomfort."
            elif humidity < 10:
                humidityLevels = "The humidity is at very low levels!"
            
            msg_txt_formatted = MSG_TXT.format(pressure=pressure, barpressure=barpressure, humidity=humidity, pressureLevels=pressureLevels, humidityLevels=humidityLevels)  
            message = Message(msg_txt_formatted)

            print( "Sending message: {}\n".format(message) )
            print(pressureLevels)
            print(humidityLevels)
            client.send_message(message)
            print ( "Message successfully sent" )  
            time.sleep(3)  
  
    except KeyboardInterrupt:  
        print ( "IoTHubClient sample stopped" )  
  
if __name__ == '__main__':  
    print ( "IoT Hub Quickstart #1 - Simulated device" )  
    print ( "Press Ctrl-C to exit" )  
    iothub_client_telemetry_sample_run()  