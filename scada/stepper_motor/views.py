import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.conf import settings
from stepper_motor import utils, models


def control_mode(request):
        
    return render(
                    request,
                    "stepper_motor/control_mode.html",
                    {
                    }
    )


def data_table(request):
    stepper_motor_data_dict = utils.read_json_file("")

    return render(
                    request,
                    "stepper_motor/data_table.html",
                    {
                        "stepper_motor_data_dict": stepper_motor_data_dict,
                    }
    )