from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from students import views
from students.views import EnrollmentApprovalView, GetRegistrationDetailsView

urlpatterns = [
    path('', views.index, name = 'student_index'),
    path('regLinks', views.registration_link, name = 'registration_link'),
    path('student-register/', views.student_register, name='student_register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('enrollment-approval/', EnrollmentApprovalView.as_view(), name='enrollment_approval'),
    path('get_registration_details/', GetRegistrationDetailsView.as_view(), name='get_registration_details'),
    path('enrollment_details/', views.enrollment_details, name='enrollment_details'),
    path('admit_card/', views.get_admit_card, name='get_admit_card'),

    path('courses/<int:cid>/', views.courses, name='courses'),

    path('contact-us/', views.contact_us, name='contact_us'),


]
