from ui_server import UIServer
from display import Display
from machine import Pin, ADC
import uasyncio as asyncio
import ujson
import gc

userConfig = {
    'league': 'NFL',
    'team': 'Chicago+Bears',
    'display': 'record',
    'animation': 'sound',
    'sports_data': {},
    'audio_level': 0,
    'curLED' : 1,
    'movingRight': True
}

async def updateDisplay():
    team = userConfig['team'].split('+')[-1].upper()
    currentSportsData = userConfig['sports_data']
    print('Updating Display')
    color = userConfig['sports_data']['team_color']
    if color == '000000':
        color = 'ff0000'
    color = (int("0x" + color[0:2]), int("0x" + color[2:4]), int("0x" + color[4:6]))

    alt_color = userConfig['sports_data']['team_color_alt']
    if alt_color == '000000':
        alt_color = 'ff0000'
    alt_color = (int("0x" + alt_color[0:2]), int("0x" + alt_color[2:4]), int("0x" + alt_color[4:6]))

    if userConfig['display'] == 'record':
        topLine = "{:<8}".format(team)[0:8]
        bottomLine = "{:>8}".format(currentSportsData['record'])[0:8]
        await myDisplay.draw_line(topLine, 0, color)
        await myDisplay.draw_line(bottomLine, 1, (10, 10, 10))
    elif userConfig['display'] == 'score':
        topLine = currentSportsData['home_abbrev'] + '-' + currentSportsData['away_abbrev'] + ':'
        bottomLine = currentSportsData['home_score'] + '-' + currentSportsData['away_score'] + ' ' + str(currentSportsData['period'])
        await myDisplay.draw_line("{:<8}".format(topLine)[0:8], 0, color)
        await myDisplay.draw_line("{:>8}".format(bottomLine)[0:8], 1, (10, 10, 10))
    elif userConfig['display'] == 'last_score':
        topLine = currentSportsData['last_home_abbrev'] + '-' + currentSportsData['last_away_abbrev'] + ':'
        bottomLine = currentSportsData['last_home_score'] + '-' + currentSportsData['last_away_score'] + ' F'
        await myDisplay.draw_line("{:<8}".format(topLine)[0:8], 0, color)
        await myDisplay.draw_line("{:>8}".format(bottomLine)[0:8], 1, (10, 10, 10))

async def fetchSportsData():
        sock = socket.socket()

        try:
            serv = socket.getaddrinfo('172.20.10.3', 5000)[0][-1]
            sock.connect(serv)
        except OSError as e:
            print('Cannot connect to 172.20.10.3 on port 5000')
            sock.close()
            return

        reader = asyncio.StreamReader(sock)
        writer = asyncio.StreamWriter(sock, {})
        try:
            writer.write(b"GET /?league=%s&team=%s HTTP/1.0\r\n" % (userConfig['league'], userConfig['team']))
            writer.write(b"Host: 172.20.10.3\r\n")
            writer.write(b"\r\n")
            await writer.drain()

            while True:
                l = await reader.readline()
                if not l or l == b"\r\n":
                    break

            res = await reader.readline()

        except OSError:
            sock.close()
            return

        sock.close()
        userConfig['sports_data'] = ujson.loads(res)

async def configChangeHandler(league=userConfig['league'], team=userConfig['team'], display=userConfig['display'], animation=userConfig['animation']):
    userConfig['league'] = league
    userConfig['team'] = team
    userConfig['display'] = display
    userConfig['animation'] = animation
    await fetchSportsData()
    await updateDisplay()
    return

server = UIServer(configChangeHandler=configChangeHandler)
myDisplay = Display(640, 14)
audio = ADC(Pin(35))
audio.atten(ADC.ATTN_11DB)

async def animationDriver():
    prev_mode = 'sound'
    while True:
        color1 = userConfig['sports_data']['team_color']

        if color1 == '000000':
            color1 = 'ff0000'
        color1 = (int("0x" + color1[0:2]), int("0x" + color1[2:4]), int("0x" + color1[4:6]))

        color2 = userConfig['sports_data']['team_color_alt']

        color2 = userConfig['sports_data']['team_color_alt']
        if color2 == '000000':
            color2 = 'ff0000'
        color2 = (int("0x" + color2[0:2]), int("0x" + color2[2:4]), int("0x" + color2[4:6]))

        if userConfig['animation'] == 'sound':
            audio_value = audio.read()
            userConfig['audio_level'] = (int(min((max(audio_value-2100,0)/10),40)))
            myDisplay.sound_border(color2, userConfig['audio_level'])
            prev_mode = 'sound'

        elif userConfig['animation'] == 'slow':
            myDisplay.bounce_border(color2, userConfig['curLED'], userConfig['movingRight'],prev_mode)
            if userConfig['curLED'] == 0:
                userConfig['movingRight'] = True

            if userConfig['curLED'] == 39:
                userConfig['movingRight'] = False

            if userConfig['movingRight']:
                userConfig['curLED'] += 1
            else:
                userConfig['curLED'] -= 1

            prev_mode = 'slow'


        elif userConfig['animation'] == 'static':
            myDisplay.static_border(color1, color2)
            prev_mode = 'static'


        await asyncio.sleep_ms(50)

async def main():
    myDisplay.clear()
    await fetchSportsData()

    serverTask = asyncio.create_task(server.run())
    animateTask = asyncio.create_task(animationDriver())

    while True:
        gc.collect()
        if userConfig['display'] == 'score':
            await fetchSportsData()
            await updateDisplay()
        await asyncio.sleep(30)

asyncio.run(main())
