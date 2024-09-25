import requests, random, os
from time import sleep

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print('  - 🎲 Waitting..', time_format,'senconds',  end='\r')
        sleep(1)
        seconds -= 1

class Blum:
    def __init__(self) -> None:
        self.total_accounts = 0
        self.index = 0  
        self.game_url = 'https://game-domain.blum.codes/api/v1'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': BLUM_BEARER_TOKEN,
            'lang': 'en',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="127", "Not;A=Brand";v="24", "Microsoft Edge";v="127", "Microsoft Edge WebView2";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        }



    def _send_request(
            self,
            session: requests.Session,
            method: str,
            url: str,
            headers: dict,
            proxies: dict,
            json_data: dict = {},
            params: dict = {},

        ):
        response = session.request(method=method, url=url, headers=headers,proxies=proxies, json=json_data, params=params, timeout=30)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                if url == 'https://game-domain.blum.codes/api/v1/daily-reward': pass
                if url == 'https://game-domain.blum.codes/api/v1/game/claim': pass
                else: print(f"it return not json: {url}\n {response.text}")
                return response.text
        else:
            print(f"ERROR: {url}\n {response.text}")
            return False        
    def post_request(self, session: requests.Session, url: str, headers: dict = None, proxies: dict={}, json_data: dict = None, params: dict = None):
        return self._send_request(session, 'POST', url, headers, proxies, json_data, params)

    def get_request(self, session: requests.Session, url: str, headers: dict = None, proxies: dict = {}, json_data: dict = None, params: dict = None):
        return self._send_request(session, 'GET', url, headers, proxies, json_data, params)
    

    def _play(self, session: requests.Session):
        url = f'{self.game_url}/game/play'
        return self.post_request(session=session, url=url)

    def _claim(self, session: requests.Session, gameId: str, points: int):
        url = f'{self.game_url}/game/claim'
        json_data = {
            'gameId': gameId,
            'points': points,
        }
        return self.post_request(session=session, url=url, json_data=json_data)

    def get_balance(self, session: requests.Session):
        url = f'{self.game_url}/user/balance'
        return self.get_request(session=session, url=url)


    def start_play_game(self, session: requests.Session):
        number_play = int(input("\n NHẬP SỐ LẦN CHƠI:\n   ➡️  "))
        print('    - OK ')
        total_point = 0
        balance = self.get_balance(session=session)
        if not balance and isinstance(balance, dict):
            print("❌ ERROR: KHÔNG LẤY ĐƯỢC THÔNG TIN BALANCE.")
            return
        sleep(3)
        playPasses = balance.get("playPasses", {})
        if playPasses == 0:
            return "\n\n❌ Không có vé để chơi game rồi..\n❌ Playgame: No"
        number_play if playPasses >= number_play else playPasses
        print(f"\n 🎫 Total Play: {number_play}/{playPasses} vé\n")
        if number_play:
            for _index in range(number_play):
                play = self._play(session=session)
                if play:
                    gameId = play.get("gameId")
                    print(f"  - 🎲 Game: {_index+1}. ID: {gameId}")
                    points = random.randint(130,180)
                    countdown(random.randint(40,50))
                    claim = self._claim(session=session, gameId=gameId, points=points)
                    print(f"  - 🎲 Game: {_index+1}. Claim status: {claim} - Points: +{points}\n")
                    if claim: total_point+=points
                    countdown(random.randint(10,15))
            return f"\n\n✅ [ DONE ] Play Game Earn: {total_point}B"
        return "\n\n❌ Playgame: No"
    

    def start(self):
        session = requests.Session()
        session.headers.update(self.headers)
        print(self.start_play_game(session=session))


if __name__ == "__main__":
        os.system('cls')
        BLUM_BEARER_TOKEN = input("\n\n Nhập BLUM_BEARER_TOKEN:\n   ➡️  ")
        print('    - OK ')
        bot = Blum()
        bot.start()