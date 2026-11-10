HW4:

* On step 2 of HW4 I wasn't sure about errors other than the 200 error, so used AI to help land on using @require\_GET which returns a 405 error for any methods other than GET.
* Upon implementing Step 4 of the HW, we filled in the login.html template. In this template, a successful login would auto redirect to /accounts/profile, which doesn't exist yet (and would return a 404 error). Instead AI helped me come up with LOGIN\_REDIRECT\_URL = '/app/' so that a successful login sends you to your home page instead.

  * Same thing done for LOGOUT\_REDIRECT\_URL = '/app/' so that the user is redirected to the home page after logging out. Made these changes in settings.py.



HW5:

* Used AI for copy-paste type html structure for the new templates (new\_course...new\_qr\_upload)
* Needed help on how to handle days = \[d.capitalize() for d in ("mon", "tue", "wed", "thu", "fri") if request.POST.get(f"day-{d}")].
* Needed help formatting timezone in central time: 



&#x20;   return \[{"username": u.student.user.username,

&#x20;            "upload\_time": timezone.localtime(u.uploaded\_at, cdt)

&#x20;                           .strftime("%Y-%m-%d %H:%M:%S")}

&#x20;           for u in uploads]

* safe=Fale in the views for def dumpUploads was needed because the object is a list instead of a dict so we can tell Django that we should have a list of dicts, where each dict has a student's QR Code upload data.





