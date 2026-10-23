"""
models.py — Data model for AttendanceChimp.

AttendanceChimp is an electronic class attendance tool.  Instructors create
courses and lectures; each lecture is assigned a random QR code.  Students
photograph the QR code and upload the image.  The system decodes the QR code,
matches it to a lecture, and records the attendance.

Entities
--------
- InstructorProfile   : extends Django User → instructor-specific data
- StudentProfile  : extends Django User → student-specific data
- Course          : a course taught by one instructor
- Enrollment      : junction table linking students to courses
- Lecture         : a single class meeting (has a QR-code identifier)
- QRCodeUpload    : a student's uploaded QR-code photograph
"""

from django.db import models
from django.contrib.auth.models import User

import logging
import string
import random

logger = logging.getLogger(__name__) # set up tracking, auditing, and debugging
                                                               # allows using logger.warning(), logger.error(), 
                                                               # logger.info(), etc. Better than print() for debuggin... 


# ---------------------------------------------------------------------------
# Helper / API functions
# ---------------------------------------------------------------------------
def qr_generator(length=32):
    '''
    Generates unique QR code string that's exactly 32 characters long.
    Args: None
    Returns (str): 32 character QR code string.
    '''
    chars = string.ascii_letters + string.digits
    elements = [random.choice(chars) for _ in range(length)]
    return "".join(elements)


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------
class InstructorProfile(models.Model):
    '''
    The instructor is a Django User, linking to the Django User table.
    Upon deleting a User (in the Django User table), a user in InstructorProfile
    is also deleted. Contains: instructor_id (PK, int) and user_id (FK, int, 
    links to User).
    '''
    instructor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class StudentProfile(models.Model):
    '''
    The student is a Django User, linking to the Django User table.
    Upon deleting a User (in the Django User table), a user in StudentProfile
    is also deleted. Contains: student_id (PK, int) and user_id (FK, int, links
    to User).
    '''
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------
class Course(models.Model):
    '''
    Course links to the InstructorProfile as a one-to-many relation,
    where one instructor can teach 0 to many courses. Course has attributes 
    including: course_id (PK, int), name (str), instructor_id (FK, int, links 
    to InstructorProfile), meeting_days (str), start_time (time), and end_time
    (time).
    '''
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    meeting_days = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------
class Enrollment(models.Model):
    '''
    Enrollment connects StudentProfile to Course. It contains enroll_id (PK, 
    int), student_id (FK, int, links to StudentProfile) and course_id (FK, int, 
    linking to Course).
    '''
    enroll_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------
class Lecture(models.Model):
    '''
    Lecture contains information about the specific lecture, linking to the
    Course table. Lecture contains: lecture_id (PK, int), course_id (FK, int, links to Course), date (date), and qr_identifier (str, unique). 
    '''
    lecture_id =  models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    qr_identifier = models.CharField(max_length=64, unique=True,
                                     default=qr_generator)
        

# ---------------------------------------------------------------------------
# QR Code Upload
# ---------------------------------------------------------------------------
class QRCodeUpload(models.Model):
    '''
    QRCodeUpload has details for each upload of a QR code for individual
    lectures and students. The class contains: qr_id (PK, int), 
    student_id (FK, int, links to StudentProfile), lecture_id (FK, int, links 
    to Lecture), image (image), and uploaded_at (datetime).
    '''
    qr_id =  models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True,
                                blank=True)
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

