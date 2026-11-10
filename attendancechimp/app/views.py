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
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime
import zoneinfo
import json
import io
from decimal import Decimal, InvalidOperation

from .models import (InstructorProfile, StudentProfile, Course, Enrollment,
                     Lecture, QRCodeUpload, create_user_with_profile)
from .models import (is_instructor, is_student, create_course, create_lecture, 
                     create_qr_upload, get_upload_data)

# from .models import(getUploadsForCourse)

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

@require_GET
def new(request):
    '''
    Renders the sign up form. GET only, otherwise fxn returns 405 error.
    '''
    return render(request, 'app/new.html')

@csrf_exempt
@require_POST
def createUser(request):
    '''
    Reads the fields from POST data (only) that include email, user_name,
    password, and is_student. Returns 4xx error for bad inputs.
    '''
    try:
        user = create_user_with_profile(
            request.POST.get("email"),
            request.POST.get("user_name"),
            request.POST.get("password"),
            request.POST.get("is_student") == "1")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    login(request, user)
    return HttpResponse("User created")

# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------

@require_GET
def new_course(request):
    return render(request, 'app/new_course.html')

@require_GET
def new_lecture(request):
    return render(request, 'app/new_lecture.html', 
                  {"courses": Course.objects.all()})

@require_GET
def new_qr_upload(request):
    return render(request, 'app/new_qr_upload.html')

@csrf_exempt
@require_POST
def createCourse(request):
    '''
    Function is POST only and instructors only (401 otherwise). 
    Reads course name, start time, end time, and day to create a Course.
    '''
    if not is_instructor(request.user):
        return HttpResponse("Instructor login required", status=401)

    days = [d.capitalize() for d in ("mon", "tue", "wed", "thu", "fri")
            if request.POST.get(f"day-{d}")]
    try:
        create_course(request.user,
                      request.POST.get("course-name"),
                      request.POST.get("start-time"),
                      request.POST.get("end-time"),
                      days)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    return HttpResponse("Course created")

@csrf_exempt
@require_POST
def createLecture(request):
    '''
    Function is POST and instructors only (401 otherwise). 
    Reads a course name
    and creates a Lecture dated today (CDT) for that course.
    '''
    if not is_instructor(request.user):
        return HttpResponse("Instructor login required", status=401)

    try:
        create_lecture(request.POST.get("choice"), datetime.now(CDT).date())
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    return HttpResponse("Lecture created")


@csrf_exempt
@require_POST
def createQRCodeUpload(request):
    '''
    Function is POST and students only (401 otherwise). 
    Reads the file field imageUpload and creates a QRCodeUpload for the 
    logged-in student.
    '''
    if not is_student(request.user):
        return HttpResponse("Student login required", status=401)

    try:
        create_qr_upload(request.user, request.FILES.get("imageUpload"))
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    return HttpResponse("QR code uploaded")


@require_GET
def dumpUploads(request):
    '''
    Function is GET and instructors only (401 otherwise). 
    Returns a JSON list of
    {"username": ..., "upload_time": ...} for every QR code upload.
    '''
    if not is_instructor(request.user):
        return HttpResponse("Instructor login is required", status=401)

    return JsonResponse(get_upload_data(), safe=False)

# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------



