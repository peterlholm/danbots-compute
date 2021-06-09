from django.shortcuts import render #, HttpResponse
#from compute.settings import DATA_PATH  #, API_SERVER, TEMP_PATH

def index(request):
    return render (request, 'home.html')

def showresult(request):
    folder_index = int(request.GET.get('index',1))
    next_val = int(request.GET.get('next',0))
    next_index = folder_index + next_val
    #print ("Index: ", index, " Next: ", next)
    picpath = '/data/device/b827eb841738/input/' + str(next_index) + '/'

    mycontext = {
        'index': next_index,
        'path': picpath,
        'pic1': picpath + "image0.png",
        'pic2': picpath + "image8.png",
        'pic3': picpath + "image9.png",
        'pic4': picpath + "mask.png",
        'pic5': picpath + "nndepth.png",
        'pic6': picpath + "nnkdata.png",
        'pic7': picpath + "nnkunwrap.png",
        'pic8': picpath + "unwrap1.png"
    }

    return render (request, 'showresult.html', context=mycontext)
