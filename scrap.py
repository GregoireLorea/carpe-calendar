import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json

months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "décembre"]
days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
done = set()
current = datetime.now()
lst = []
for i in range(100):
    print(i+1)
    r = requests.get(f"https://louvainfo.be/calendrier/?year={current.year}&month={current.month}&day={current.day}")
    soup = BeautifulSoup(r.text, "html.parser")
    for a_tag in soup.find_all("a"):
        link = a_tag["href"]
        # print(link)
        if "/calendrier/" not in link or "/calendrier/" == link.strip() or "?year=" in link:
            continue
        album = link.split("/")[-2]
        if not album.isnumeric() or album in done:
            continue
        done.add(album)
        r = requests.get(f"https://louvainfo.be{link}")
        soup = BeautifulSoup(r.text, "html.parser")
        div_title = soup.find("div", {"class": "event-box-title"})
        title = div_title.findChildren("h2")[0].text.strip()

        trs = soup.find_all("tr")
        infos = {}
        dates = None
        for tr in trs:
            if dates is not None:
                tds = tr.findChildren("td")
                dates.append((tds[0].text.strip(), tds[1].text.strip()))
            if "Catégorie" in tr.text:
                infos["category"] = tr.findChildren("td")[0].text.strip()
            elif "Prix" in tr.text:
                infos["price"] = tr.findChildren("td")[0].text.strip()
            elif "Lieu" in tr.text:
                infos["place"] = tr.findChildren("td")[0].text.strip()
            elif "Organisateur" in tr.text:
                infos["organizer"] = tr.findChildren("td")[0].text.strip()
            elif "Dates" in tr.text:
                dates = []

        event_meta = soup.find("div", {"id": "event-meta"})
        description = event_meta.findChildren("div")[1].text.strip()
        img = soup.find("a", {"id": "imheader"})["href"]
        formatted_dates = []
        for date in dates:
            if date[1] == "Toute la journée":
                start = "00:00"
                end = "23:59"
            else:
                start, end = date[1].split(" - ")
            day_text, day, month = date[0].split()
            check_date = datetime(current.year, months.index(month)+1, int(day))
            while check_date.weekday() != days.index(day_text):
                check_date += timedelta(days=365)
                if check_date.day != int(day):
                    check_date += timedelta(days=1)
            hour_start, minutes_start = map(int, start.split(":"))
            hour_end, minutes_end = map(int, end.split(":"))

            start_day = check_date + timedelta(hours=hour_start, minutes=minutes_start)
            end_day = check_date + timedelta(hours=hour_end, minutes=minutes_end)
            formatted_dates.append((start_day, end_day))

        lst.append({
            "id": album,
            "name": title,
            "infos": infos,
            "description": description,
            "img_url": img,
            "dates": formatted_dates
        })
    current += timedelta(days=7)
with open("results.json", "w") as f:
    f.write(json.dumps(lst, default=str))