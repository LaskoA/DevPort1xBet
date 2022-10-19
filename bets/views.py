from aiohttp import request
from django.http import HttpResponse
from rest_framework import viewsets

from .models import Scrapedgame


from bs4 import BeautifulSoup

import aiohttp
import asyncio

from .serializer import ScrapedgameSerializer


class GameAPI(viewsets.ModelViewSet):
    queryset = Scrapedgame.objects.all()
    serializer_class = ScrapedgameSerializer


async def main(request):
    async with aiohttp.ClientSession(trust_env=True) as session:

        async with session.get('https://ua1xbet.com/us/live/football', ssl=False) as response:
            print("Status:", response.status)

            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            games = soup.select('.c-events-scoreboard__wrap')
            Scrapedgame.objects.all().delete()
            for game in games:
                home_score = game.select(".c-events-scoreboard__lines .c-events-scoreboard__line")[0].select(
                    "span")
                away_score = game.select(".c-events-scoreboard__lines .c-events-scoreboard__line")[1].select(
                    "span")
                bet = game.select_one(".c-bets")
                homeScore = home_score[1].text
                awayScore = away_score[1].text
                odd1 = bet.select(".c-bets__inner")[0].text
                oddX = bet.select(".c-bets__inner")[1].text
                odd2 = bet.select(".c-bets__inner")[2].text
                active1 = False if "is-locked" in str(bet).split('a class="c-bets__bet c-bets__bet_coef '
                                                                 'c-bets__bet_sm')[1] else True
                activeX = False if "is-locked" in str(bet).split('a class="c-bets__bet c-bets__bet_coef '
                                                                 'c-bets__bet_sm')[2] else True
                active2 = False if "is-locked" in str(bet).split('a class="c-bets__bet c-bets__bet_coef '
                                                                 'c-bets__bet_sm')[3] else True

                home = game.select(".c-events-scoreboard__item .c-events__team")[0].text
                away = game.select(".c-events-scoreboard__item .c-events__team")[1].text
                currentScore = homeScore + ":" + awayScore
                market = [
                    {
                        "title": "1X2 Regular time",
                        "outcomes": [
                            {
                                "active": active1,
                                "odd": odd1,
                                "type": "1",
                            },
                            {
                                "active": activeX,
                                "odd": oddX,
                                "type": "X",
                            },
                            {
                                "active": active2,
                                "odd": odd2,
                                "type": "2",
                            }]}]
                game = Scrapedgame()
                game.home = home
                game.away = away
                game.currentScore = currentScore
                game.market = market
                game.save()
        return HttpResponse("Latest Data Fetched from 1xBet")


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(request))
