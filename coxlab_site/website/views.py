from mimetypes import guess_type

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django_mongodb_engine.storage import GridFSStorage

from gridfs.errors import NoFile
from models import gridfs_storage

from website.models import Video, Comment, Author
import numpy as np
import cv2

import forms

if settings.DEBUG:

    def serve_from_gridfs(request, path):
        # Serving GridFS files through Django is inefficient and
        # insecure. NEVER USE IN PRODUCTION!
        try:
            gridfile = gridfs_storage.open(path)
        except NoFile:
            raise Http404
        else:
            return HttpResponse(gridfile, mimetype=guess_type(path)[0])

class IndexView(generic.ListView):
    template_name = 'website/index.html'
    context_object_name = 'index'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Video.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:10]    

class VideoListView(generic.ListView):
    template_name = 'website/video_list.html'
    context_object_name = 'video_list'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Video.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:10]   


class RecordView(generic.ListView):
    template_name = 'website/video_recorder_new.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Video.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:10]   


class VideoView(generic.DetailView):
    model = Video
    template_name = 'website/video_detail.html'


class CreateUser(generic.DetailView):
    pass

class LoginUser(generic.DetailView):
    pass



def post_comment(request, video_id):
    p = Video.objects.get(pk=video_id)
    text = request.GET.get('comment')
    author = Author(name=request.GET.get('name'), email=request.GET.get('email'))
    comment = Comment(author=author, comment_text=text)
    p.comments.append(comment)
    p.save()

    return HttpResponseRedirect(reverse('website:video_detail', args=(p.id,)))

def record_and_save_video(request):
    
    cap = cv2.VideoCapture(0)
    cap.open(0)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
    h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
    # video recorder
    fourcc = cv2.cv.CV_FOURCC(*'XVID')  # cv2.VideoWriter_fourcc() does not exist
    out = cv2.VideoWriter("output.avi", fourcc, 25, (w, h))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret==True:
            frame = cv2.flip(frame,0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()



# def upload_video(request):
#     video_file = request.GET.('video')


