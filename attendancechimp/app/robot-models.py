"""
AttendanceChimp models.

Six entities: User, StudentProfile, Course, Enrollment, Lecture, QRCodeUpload.

Setup note: because User extends AbstractUser, add this to settings.py
before running the first migration:
    AUTH_USER_MODEL = "app.User"
"""

"""
Model Used: Sonnet 5.5 High
Prompt: AttendanceChimp is an app I'm building for a course. Build models.py 
based on the following specifications. AttendanceChimp tracks class attendance 
via QR codes:
• Users: students and instructors (two roles).
• Courses: each has one instructor. Students can enroll in multiple courses.
• Lectures: individual class meetings, each associated with a course.
• QR Code Uploads: photos uploaded by students, each associated with a student 
and a
lecture.
Design requirements: simple to use, supports attendance analytics, robust to 
cheating.
Note that you should also have a Django class for Enrollment, since we need a 
way to link the StudentProfile table to the Course table. I have attached the 
entity relations diagram I made for this project. Output should be saved at 
C:\Users\aadik\1Local_DS_Master\Data_136\hw_0\attendancechimp\app\robot-models.
py on my computer. 
Note: don't overcomplicate things, try to keep it simple and readable while 
accomplishing the attendancechimp specifications. To be clear, I just want one 
file called robot-models.py with all the relevant entities (6 total).
"""

import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_qr_token():
    """Random, unguessable string that gets encoded into a lecture's QR code."""
    return secrets.token_urlsafe(16)


class User(AbstractUser):
    """One user table for everyone; `role` says whether they're a student or instructor."""

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "instructor", "Instructor"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    def __str__(self):
        return f"{self.username} ({self.role})"


class StudentProfile(models.Model):
    """Extra info for students. Enrollments and uploads hang off this table."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    student_id = models.CharField(max_length=20, unique=True)  # e.g. university ID

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.student_id})"


class Course(models.Model):
    """A course has exactly one instructor."""

    code = models.CharField(max_length=20)  # e.g. "DATA136"
    name = models.CharField(max_length=200)
    term = models.CharField(max_length=20)  # e.g. "Fall 2026"
    instructor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # don't silently delete a course if its instructor is removed
        related_name="courses_taught",
        limit_choices_to={"role": User.Role.INSTRUCTOR},
    )

    class Meta:
        unique_together = ("code", "term")

    def __str__(self):
        return f"{self.code} - {self.name} ({self.term})"


class Enrollment(models.Model):
    """Links a student to a course (many-to-many through table)."""

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")  # can't enroll twice

    def __str__(self):
        return f"{self.student} in {self.course}"


class Lecture(models.Model):
    """A single class meeting. Its QR code encodes `qr_token`."""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lectures"
    )
    title = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()  # uploads only count between start and end
    # Anti-cheating: secret per-lecture token shown only in the QR code in the room.
    qr_token = models.CharField(
        max_length=64, unique=True, default=generate_qr_token, editable=False
    )

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.course.code} - {self.title or self.start_time.strftime('%Y-%m-%d')}"


class QRCodeUpload(models.Model):
    """A student's photo of the lecture QR code; serves as the attendance record."""

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="uploads"
    )
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="uploads"
    )
    image = models.ImageField(upload_to="qr_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)  # server-set, can't be faked

    # Anti-cheating fields (filled in by the upload view):
    decoded_token = models.CharField(max_length=64, blank=True)  # token read from the photo
    image_hash = models.CharField(max_length=64, unique=True)  # SHA-256; blocks reusing one photo
    is_valid = models.BooleanField(default=False)  # token matches lecture AND within time window

    class Meta:
        unique_together = ("student", "lecture")  # one attendance record per student per lecture

    def __str__(self):
        return f"{self.student} -> {self.lecture} ({'valid' if self.is_valid else 'invalid'})"
