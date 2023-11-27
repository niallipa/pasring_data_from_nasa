import json
import requests
import os.path

# Чукотка
# point_one_c = [83, -180]  # Первое значение горизонт, второе вертикаль, первая точка up+left
# point_two_c = [41, -167]  # down+right

# Остальная Россия
# point_one_c = [83, 19]
# point_two_c = [41, 180]

# ЮАР
point_one_c = [-21 ,16]
point_two_c = [-36, 34]


def req(longitude, latitude):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"

    params = {
        "start": 1997,
        "end": 2021,
        "latitude": latitude,
        "longitude": longitude,
        "community": "re",
        "parameters": "WD10M,WS10M,WD50M,WS50M,SI_EF_TILTED_SURFACE",
        "format": "json",
        "headers": False
    }

    try:
        r = requests.get(url=url, params=params, timeout=60)
        print(f"{longitude} {latitude} {r.status_code}")
        assert r.status_code == 200
        res = r.json()
        with open("parsing/" + str(params["longitude"]) + "_" + str(params["latitude"]) + ".json", "w") as f:
            json.dump(res, f)
    except Exception:
        print("bad request")
        with open("bad/" + str(params["longitude"]) + "_" + str(params["latitude"]) + ".txt", "w") as f:
            f.write(str(r.status_code))


count = (len(range(point_two_c[0], point_one_c[0] + 1)) * len(range(point_one_c[1], point_two_c[1] + 1)))
idle_count = 0

for i in range(point_two_c[0], point_one_c[0] + 1):
    for j in range(point_one_c[1], point_two_c[1] + 1):
        if os.path.exists("parsing/" + str(j) + "_" + str(i) + ".json"):
            print(os.path.exists("parsing/" + str(j) + "_" + str(i) + ".json"))
        else:
            try:
                req(j, i)
            except Exception:
                print("bad req")
        idle_count += 1
        print(str(idle_count) + "/" + str(count) + " " + str((idle_count/count)*100) + "%")


if __name__ == '__main__':
    print('end')
