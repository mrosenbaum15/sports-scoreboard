import uasyncio as asyncio
import ui_fetch

class UIServer:

    def __init__(self, configChangeHandler, host='0.0.0.0', port=80, backlog=0, timeout=1):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        self.configChangeHandler = configChangeHandler
        self.html = ui_fetch.get_ui()

    async def run(self):
        print('Awaiting client connection.')
        self.cid = 0
        self.server = await asyncio.start_server(self.run_client, self.host, self.port, self.backlog)
        while True:
            await asyncio.sleep(10)

    async def run_client(self, sreader, swriter):
        self.cid += 1
        print('Got connection from client', self.cid)
        try:
            while True:
                try:
                    res = await asyncio.wait_for(sreader.readline(), self.timeout)
                except asyncio.TimeoutError:
                    res = b''
                if res == b'':
                    raise OSError
                request = str(res)

                if request[2:5] == 'GET':

                    print('Content = %s' % request)
                    params = {}
                    ampersandSplit = request.split(' ')[1][2:].split("&")

                    for element in ampersandSplit:
                        equalSplit = element.split("=")
                        try:
                            params[equalSplit[0]] = equalSplit[1]
                        except:
                            pass


                    if 'league' in params and 'team' in params and 'display' in params and 'animation' in params:
                        await self.configChangeHandler(params['league'], params['team'], params['display'], params['animation'])


                    swriter.write('HTTP/1.1 200 OK\n')
                    swriter.write('Content-Type: text/html\n')
                    swriter.write('Connection: close\n\n')
                    swriter.write(self.html)
                    await swriter.drain()  # Echo back
        except OSError:
            pass
        print('Client {} disconnect.'.format(self.cid))
        await sreader.wait_closed()
        print('Client {} socket closed.'.format(self.cid))

    async def close(self):
        print('Closing server')
        self.server.close()
        await self.server.wait_closed()
        print('Server closed.')
