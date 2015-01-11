import time
import commands
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in("jlayhue","PASSWORD")
from w1thermsensor import W1ThermSensor
import forecastio

roomName = "dining"
plotLabel = "room-temperatures-" + roomName

#Forecast.io stuff
api_key = "API_KEY"
lat = 42.1296
lon = -80.0852

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "000006564543")

zone = 'master bedroom'
dates = []
temps = []
nesttemp = []
nestsetting = []

cnt = 0
while 1:
    timevalue = time.strftime("%Y-%m-%d %H:%M:%S")
    temp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
    print(timevalue + ' - ' + str(temp))

    #Get forecast.io info
    forecast = forecastio.load_forecast(api_key,lat,lon)
    currentForecast = forecast.currently()
    outsideTemp = currentForecast.temperature
    print("Outside Temp: " + str(outsideTemp))

    
    #Get data from Nest
    allData = commands.getstatusoutput('nest.py --user emailaddress --password Password1 show')
    allLines = allData[1].splitlines()
    for line in allLines:
        if line.find("current_temperature") > -1:
            dummy,current_temp = line.split("current_temperature.............:")
            current_temp=current_temp.rstrip()
            current_temp=float(current_temp)
            current_temp=current_temp*9/5 + 32
            print(line)
        elif line.find("target_temperature.") > -1:
            dummy,desired_temp = line.split("target_temperature..............:")
            desired_temp=desired_temp.rstrip()
            desired_temp=float(desired_temp)
            desired_temp=desired_temp*9/5 + 32
            print(line)

    # append all data
    dates.append(timevalue)
    temps.append(temp)
    nesttemp.append(current_temp)
    nestsetting.append(desired_temp)

    # create plot data
    roomTempTrace = Scatter(
        #x=dates,
        #y=temps,
        x=timevalue,
        y=temp,
        name="Room Temp"
    )

    nestTempTrace = Scatter(
        #x=dates,
        #y=nesttemp,
        x=timevalue,
        y=current_temp,
        name="Nest Temp"
    )

    nestSettingTrace = Scatter(
        #x=dates,
        #y=nestsetting,
        x=timevalue,
        y=desired_temp,
        name="Nest Setting"
    )

    outsideTempTrace= Scatter(
        x=timevalue,
        y=outsideTemp,
        name="Outside Temp"
    )
    
    data = Data([roomTempTrace,nestTempTrace,nestSettingTrace,outsideTempTrace])

    layout = Layout(
        title="Room Temps",
        xaxis = XAxis(
            title="Date/Time"
        ),
        yaxis=YAxis(
            title="Temperature(F)"
        )
    )

    fig = Figure(data=data,layout=layout)
    
    plot_url = py.plot(fig,filename=plotLabel,auto_open=False, fileopt='extend')
    time.sleep(300)
    cnt = cnt + 1
    
