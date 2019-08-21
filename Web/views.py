from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from spider_models import Spider
from movie_models import Movie
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from config import Config
from .models import MovieForm


# Create your views here.
def index(request):
    # user_list = Users.objects.filter(user_name='WIWU').order_by('user_id')
    # user_list = Users.objects.extra(where="user_name like 'WIWU'").order_by('user_id')
    # request.META["CSRF_COOKIE_USED"] = True
    mymv = Movie()
    row_list = None
    pageinator = None
    tmpl = loader.get_template('index.html')
    form = MovieForm()

    if request.method == 'GET':
        page = request.GET.get('page')
        delete_no = request.GET.get('delete')
        pull = request.GET.get('pull')
        if pull is not None:
            getdatabyspider()
        # print(delete_no)
        if delete_no is not None:
            mymv.DBdelete(delete_no)
        row_list = mymv.DBfetchall()
        # print(row_list)
        pageinator = Paginator(row_list, 10)

        try:
            row_list = pageinator.page(page)
        except PageNotAnInteger:
            row_list = pageinator.page(1)
        except InvalidPage:
            return HttpResponse('NO DATA FOUND')
        except EmptyPage:
            row_list = pageinator.page(pageinator.num_pages)
    elif request.method == 'POST':
        print(request.POST)
        querystring = request.POST.get('querystring', None)
        upNo = request.POST.get('upNo', None)
        print(upNo)
        if querystring is not None:
            form = MovieForm({'querystring': querystring})
            row_list = mymv.DBfetchall(name=querystring, actors=querystring)
        if upNo is not None:
            upName = request.POST.get('upName', None)
            upActors = request.POST.get('upActors', None)
            upTime = request.POST.get('upTime', None)
            upScore = request.POST.get('upScore', None)
            mymv.data = {'no': int(upNo), 'name': upName, 'actors': upActors, 'time': upTime, 'score': upScore}
            print(mymv.data)
            mymv.DBupdate()
            row_list = mymv.DBfetchall()
        pageinator = Paginator(row_list, 10)
        row_list = pageinator.page(1)


    else:
        row_list = mymv.DBfetchall()
        pageinator = Paginator(row_list, 10)
        row_list = pageinator.page(1)


    # print(form)
    cont = {'rows': row_list, 'form': form}
    # print(user_list)
    # print('index.1...')
    # print(tmpl.render(cont))
    return HttpResponse(tmpl.render(cont))


def getdatabyspider():
    print("start pull by spider......")
    i = 1
    for offset in range(0, 100, 10):
        movies = Spider.parse_url(offset=offset)

        for each_movie in movies:
            myMovie = Movie(no=str(i), name=each_movie['name'],
                            actors=each_movie['actors'].replace('主演：', ''),
                            time=each_movie['time'].replace('上映时间：', ''),
                            score=each_movie['score'])
            myMovie.DBupdate()
            i = i + 1
        print("{} records inserted/updated to {}".format(i-1, Config.Database))
