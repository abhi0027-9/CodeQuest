from django.urls import path
from .views import *


urlpatterns = [
    path('',MainHome.as_view(),name='main'),
    path('login/',LoginView.as_view(),name='login'),
    path('home/',Home.as_view(),name='fhome'),
    path('students/',StudentsList.as_view(),name='students'),
    path('materials/',MaterialsView.as_view(),name='mat'),
    path('language/',LanguagesView.as_view(),name='lang'),
    path('questions/',QuestionsView.as_view(),name='ques'),
    path('add-student/',AddStudent.as_view(),name='add-stu'),
    path('edit-student/<int:pk>/',StudentPUTView.as_view(),name='edit-stu'),
    path('remove-student/<int:pk>/',remove_student,name='del-stu'),
    path('add-notes/', add_notes, name='add_notes'),
    path('add-files/', add_files, name='add_files'),
    path('add-lang/', add_lang, name='add_lang'),
    path('delete-note/<int:note_id>/', delete_note, name='delete_note'),
    path('delete-file/<int:file_id>/', delete_file, name='delete_file'),
    path('delete-lang/<int:lang_id>/', delete_lang, name='delete_lang'),
    path('delete-ques/<int:que_id>/<int:pk>/', delete_ques, name='delete_ques'),

    path('questions/<int:lang_id>/',questions_view, name='questions_view'),
    path('add-question/', add_question, name='add_question'),
    path('student-results/<int:pk>/',student_results, name='student_results'),
    path('student-detail/<int:pk>/',student_results_by_user, name='student_detail'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]
