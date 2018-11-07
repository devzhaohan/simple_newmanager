from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status

from Api.models import News
from Api.models import Member


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

import jwt
import time
import hashlib
import json





@csrf_exempt
def login_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            print(data)

            username = data.get('username')
            password = data.get('password')

            print('username', username)
            print('password', password)

            m2 = hashlib.md5()
            m2.update(password.encode('utf-8'))
            password = m2.hexdigest()
            print(password)

            member = Member.objects.filter(name=username, passwd=password).first()

            if member:

                print('member', member.id)

                token = gen_bearer_token(member.id, 1000*60*60*24)



                print('token', token)

                content = {'username': username, 'token': token}

                print('content', content)

                # 返回自定义请求内容content,200状态码
                return JsonResponse(data=content, status=status.HTTP_200_OK)

            else:
                content = {'type': 0, 'code': 2001, 'msg': 'Fail'}
                return JsonResponse(data=content, status=status.HTTP_200_OK)

    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def create_member_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    # print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # content = {'type': 1, 'msg': 'SUCCESS'}
    # # 返回自定义请求内容content,200状态码
    # return JsonResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            print(data)

            username = data.get('username')
            password = data.get('password')

            # print('username', username)
            # print('password', password)

            m2 = hashlib.md5()
            m2.update(password.encode('utf-8'))
            password = m2.hexdigest()

            create_member = Member(name=username, passwd=password, active='1')
            create_member.save()

            content = {'type': 1, 'msg': 'SUCCESS'}
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])



@csrf_exempt
def modify_member_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            print(data)

            id = data.get('id')
            username = data.get('username')
            password = data.get('password')
            active = data.get('active')

            member_job = News.objects.get(id=id)
            member_job.name = username
            member_job.passwd = password
            member_job.active = active
            member_job.save()

            content = {'type': 1, 'msg': 'SUCCESS', data: {}}
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])

@csrf_exempt
def list_member_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            print(data)

            list = Member.objects.all()

            # 分页器，前面是总共的元素，limit是每页的元素个数
            limit = 10
            paginator = Paginator(list, limit)
            print('页码数量', paginator.num_pages)

            # 从页面获取页数信息，这里是获取？后参数page的value,
            # 可以看到get后的‘page’并不是我们定义的，而是我们获取的
            # 它的值就是个int
            page_num = request.GET.get('page', 1)

            # 显示某‘page’页面的信息

            try:
                page = paginator.page(page_num)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page = paginator.page(paginator.num_pages)

            list_data = serializers.serialize("json", page.object_list)
            print('这里是loaded', list_data)
            print(type(list_data))

            all_dicts = to_json_dict(page.object_list)
            all_jsons = json.dumps(all_dicts, ensure_ascii=False)

            list_json = json.loads(all_jsons)

            page_data = {
                'object_list': list_json,
                # 'count': page.count,
                'number': page.number,
                'has_next': page.has_next(),
                'has_previous': page.has_previous(),
                # 'next_page_number': (page.next_page_number() if page.next_page_number() else 0),
                # 'previous_page_number': page.previous_page_number(),
                'start_index': page.start_index(),
                'end_index': page.end_index(),
            }

            content = {'type': 1, 'msg': 'SUCCESS', 'data': page_data}

            print('content type', type(content))

            # content_data =  serializers.serialize('json', content)

            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


def to_json_dict(objs):
    obj_arr = []
    for o in objs:
        obj_arr.append(o.to_json_dict())
    return obj_arr

@csrf_exempt
def add_news_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}
            print(data)

            test1 = News(n_title='标题3', n_content='内容', n_category='测试', n_is_publish='1')
            test1.save()


            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])

@csrf_exempt
def remove_news_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}

            test1 = News.objects.get(id=1)
            test1.delete()

            print(data)
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])

@csrf_exempt
def modify_news_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    token = request.META.get("HTTP_TOKEN")
    jwt_payload = verify_bearer_token(token)
    print('jwt_payload', jwt_payload)
    if not jwt_payload:
        content = {'type': 0, 'msg': 'token error'}
        return HttpResponse(data=content, status=status.HTTP_200_OK)

    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}

            print(data)

            test1 = News.objects.get(id=2)
            test1.n_title = 'book1'
            test1.n_content = 'xxxxxxx'
            test1.save()


            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def show_news_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}

            print(data)

            list = News.objects.all()
            for i in list:
                print(i.n_title)


            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def list_news_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}
            limit = 4
            print(data)

            list = News.objects.all()

            # 分页器，前面是总共的元素，limit是每页的元素个数
            paginator = Paginator(list, limit)
            print('页码数量', paginator.num_pages)

            # 从页面获取页数信息，这里是获取？后参数page的value,
            # 可以看到get后的‘page’并不是我们定义的，而是我们获取的
            # 它的值就是个int
            page = request.GET.get('page', 1)

            # 显示某‘page’页面的信息
            loaded = paginator.page(page)

            # print('这里是loaded', loaded)
            print('page_range', paginator.page_range)

            pageobject_list = loaded.object_list
            for i in pageobject_list:
                print(i.n_title)

            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


def verify_bearer_token(token):
    #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
    secret = "devzhao"
    payload = jwt.decode(token, secret, audience='devzhao', algorithms=['HS256'])
    if payload:
        return True, token
    return False, token


def gen_bearer_token(uid,expire_millis):
    payload = {
        "iss": "devzhao",
         "iat": int(time.time()),
         "exp": int(time.time())+expire_millis,
         "aud": "devzhao",
         "uid": uid,
         "scopes": ['open']
    }
    secret = "devzhao"
    token = jwt.encode(payload, secret, algorithm='HS256')
    token_str = token.decode()
    return True, token_str