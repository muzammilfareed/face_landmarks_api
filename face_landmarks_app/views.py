from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from face_landmarks import main
import os
import cv2
from django.shortcuts import render
import glob

def get_date_time_for_naming():
    (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
    dt_dateTime = "%s%03d" % (dt, int(micro) / 1000)
    return dt_dateTime
url = 'http://0.0.0.0:8000/'
@csrf_exempt
def index(request):
    folder = 'static/input_img/'
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES.get('file')
        # result = glob.glob('static/result/*')
        # for f in result:
        #     os.remove(f)
        date_time = get_date_time_for_naming()
        front_path = date_time + '_' + file.name
        location = FileSystemStorage(location=folder)
        fn = location.save(front_path, file)
        path = os.path.join('static/input_img/', fn)
        flag, json_path, frame_processed = main(path)
        cv2.imwrite(f'static/result/img.jpg', frame_processed)
        img_url =url+'static/result/img.jpg'
        # img_url = url+frame
        # print(json_path)
        if flag == True:
            context = {
                "status": "success",
                "results": json_path,
                'image_path': img_url,
            }
            return JsonResponse(context, safe=False)
        else:
            context = {
                "status": 'invalid input',
            }
            return JsonResponse(context)
    return render(request, 'index.html')