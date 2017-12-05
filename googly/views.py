from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.



def place_text_search(request):
	key = "AIzaSyBXdd6MXVCHSKeEyYez9CweEgdH81KCsa4"
	query = request.GET.get('query', 'coded')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	nextpage = request.GET.get('nextpage')
	if nextpage is not None:
		url += "&pagetoken="+nextpage
	response = requests.get(url)
	
	
	context = {
		'response': response.json(),
		'nextpage': nextpage,
	}
	# return JsonResponse(response.json(), safe=False)
	return render(request, "display.html", context)



def place_detail(request):
	key = "AIzaSyBXdd6MXVCHSKeEyYez9CweEgdH81KCsa4"
	place_id = request.GET.get('place_id', '')
	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)
	mapkey = "AIzaSyA-zcY75NDA1wfZW5DY8Bq1qih4JShghKM"
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	context = {
	'response': response.json(),
	'mapkey': mapkey,
	}
	return render(request, "place-detail.html", context)
	# return JsonResponse(response.json(), safe=False)

