HW4:

* On step 2 of HW4 I wasn't sure about errors other than the 200 error, so used AI to help land on using @require\_GET which returns a 405 error for any methods other than GET.
* Upon implementing Step 4 of the HW, we filled in the login.html template. In this template, a successful login would auto redirect to /accounts/profile, which doesn't exist yet (and would return a 404 error). Instead AI helped me come up with LOGIN\_REDIRECT\_URL = '/app/' so that a successful login sends you to your home page instead.

  * Same thing done for LOGOUT\_REDIRECT\_URL = '/app/' so that the user is redirected to the home page after logging out. Made these changes in settings.py.



