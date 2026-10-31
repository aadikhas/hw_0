"""
views.py — HTTP request handlers for AttendanceChimp.

Each view corresponds to one URL endpoint.  Views receive an HTTP request,
interact with the database via models.py, and return an HTTP response.
"""

from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseBadRequest, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
import zoneinfo
import json
import io
from decimal import Decimal, InvalidOperation

# from .models import (InstructorProfile, StudentProfile, Course, Enrollment,
#                      Lecture, QRCodeUpload, is_instructor, is_student,
#                      getUploadsForCourse)

CDT = zoneinfo.ZoneInfo("America/Chicago")


# ---------------------------------------------------------------------------
# HW2  — index, time, sum
# ---------------------------------------------------------------------------

def index(request):
    """Render the home page (index.html)."""

    context = {"time": datetime.now(CDT).strftime("%H:%M"),
               "user": request.user}
    return render(request, 'app/index.html', context)

def time_view(request):
    now = datetime.now(CDT)
    return HttpResponse(now.strftime("%H:%M"), content_type="text/plain")

def sum_view(request):
    try:
        total = Decimal(request.GET.get("n1")) + Decimal(request.GET.get("n2"))
        return HttpResponse(f"<p>{total}</p>")
    except (TypeError, InvalidOperation):
        return HttpResponse("<p>n1 and n2 must be numbers</p>", status = 400)

# ---------------------------------------------------------------------------
# HW4  — user creation
# ---------------------------------------------------------------------------
from django.views.decorators.http import require_GET

@require_GET
def new(request):
    '''
    Renders the sign up form. GET only, otherwise fxn returns 405 error.
    '''
    return render(request, 'app/new.html')


# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------



