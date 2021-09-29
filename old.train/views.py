from django.shortcuts import render #, HttpResponse
#from compute.settings import DATA_PATH  #, API_SERVER, TEMP_PATH

def showresult(request):
    folder_index = int(request.GET.get('index',1))
    next_val = int(request.GET.get('next',0))
    next_index = folder_index + next_val
    #print ("Index: ", index, " Next: ", next)
    #picpath = '/data/device//dca6320b6bd5/input/' + str(next_index) + '/'
    #picpath = '/data/device//b827eb841738/input/' + str(next_index) + '/'
    picpath = '/data/device//b827eb05abc2/input/' + str(next_index) + '/'

    mycontext = {
        'index': next_index,
        'path': picpath,
        'pic1': picpath + "image8.jpg",
        'pic2': picpath + "image0.jpg",
        'pic3': picpath + "image9.jpg",
        'pic4': picpath + "mask.png",
        'pic5': picpath + "nndepth.png",
        'pic6': picpath + "nnkdata.png",
        'pic7': picpath + "nnkunwrap.png",
        'pic8': picpath + "unwrap1.png"
    }

    return render (request, 'showresult.html', context=mycontext)
