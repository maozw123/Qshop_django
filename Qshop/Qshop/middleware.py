from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from Qshop.settings import ERROR_PATH
# from Seller.views import sendDing
import time

class MiddleWareTest(MiddlewareMixin):
    def process_request(self,request):
        request_ip=request.META["REMOTE_ADDR"]
        if request_ip=="10.10.14.240":
            return HttpResponse('非法ip')
        print("我是process_request")
    def prcoess_view(self,request,callback,callback_args,callback_kwargs):
        """

        :param request: 请求
        :param callback: 对应视图函数，访问那个视图就是那个视图函数
        :param callback_args: 视图函数的参数  元祖类型
        :param callback_kwargs: 视图函数的参数  字典类型
        :return:
        """
        print('我是process_view')
        # print(callback)
    # def process_exception(self,request,exception):
    #     """
    #
    #     :param request:
    #     :param exception:
    #     :return:
    #     """
    #     if exception:
    #         with open(ERROR_PATH,"a") as f:
    #             now=time.strftime("%Y-%m-%d %H:%M:%s",time.localtime())
    #             content="[%s]:%s\n"%(now,exception)
    #             f.write(content)
    #             sendDing.delay(content)
    #         return HttpResponse("代码错了，错误如下：<br> %s"%exception)
    def process_template_response(self,request,response):
        """

        :param request:
        :param response:
        :return:
        """
        print("我是process_template_response")
        return HttpResponse('123')
    def process_response(self,request,response):
        """
        process_reponse和process_template_response必须有返回值
        :param request:
        :param response:
        :return:
        """
        print('我是process_response')
        return response