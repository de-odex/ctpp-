import requests

beatmap_id = 1088204
parameters = {
	"k": "7ec7168b3a0b7bec07fe66e7bbe259a15bafc287",
	"b": beatmap_id
}
response = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameters)
data = response.json()
print(data[0]["difficultyrating"])
