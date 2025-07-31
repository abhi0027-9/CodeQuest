from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,FormView,CreateView,View
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as auth_logout
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# Create your views here.



def custom_logout(request):
    auth_logout(request)
    return redirect('log')

class MainHome(TemplateView):
    template_name='mainhome.html'

class Home(TemplateView):
    template_name='faculty_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()[:4]
        return context

class AddStudent(CreateView):
    template_name='addstudent.html'
    model=Student 
    form_class=StudentForm 
    success_url=reverse_lazy('students')



class StudentsList(TemplateView):
    template_name='students_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context
    

class LoginView(FormView):
    template_name="login.html"
    form_class=LogForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data you might need
        return context
    def post(self,request,*args,**kwargs):
        form=LogForm(data=request.POST)
        if form.is_valid():  
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(request,email=email,password=password)
            if user: 
                login(request,user)
                if request.user.is_superuser == 1:
                    return redirect('fhome')
                else:
                    return redirect('uhome')
            else:
                return render(request,'login.html',{"form":form})
        else:
            return render(request,'login.html',{"form":form})  

def remove_student(req,pk):
    try:
        stu= get_object_or_404(CustomUser,id=pk)
        stu.delete()
        stu.save()
        return redirect('students')
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
class StudentPUTView(View): 
    template_name = 'student_edit.html'
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        student = get_object_or_404(Student, id=id)
        form = StudentForm(instance=student)
        
        context = {
            'form': form,
            'student': student,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        stu = get_object_or_404(Student, id=id)
        form = StudentForm(request.POST, request.FILES, instance=stu)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Student Updated Successfully!")
            return redirect('students')  # Ensure correct URL name
        else:
            messages.error(request, "Failed. Please correct the errors below!")
            context = {
                'form': form,
                'student': stu,
            }
            return render(request, self.template_name, context)
        

class AddMaterialsText(CreateView):
    template_name='materials_text.html'
    model= StudyMaterialNotes 
    form_class= StudyNotesForm
    success_url = reverse_lazy('add-cls')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['note']=StudyMaterialNotes.objects.all()
        context['file']=StudyMaterialFile.objects.all()
        return context
    

class MaterialsView(TemplateView):
    template_name = 'materials.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['note']=StudyMaterialNotes.objects.all()
        context['file']=StudyMaterialFile.objects.all()
        return context

class LanguagesView(TemplateView):
    template_name = 'languages.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['lang']=Language.objects.all()
        return context
    

def add_notes(request):
    """View for adding new notes"""
    print(request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        
        try:
            StudyMaterialNotes.objects.create(
                name=name,
                text=text,
                user=request.user
            )
            messages.success(request, 'Note added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding note: {str(e)}')
            
    return redirect('mat')


def add_files(request):
    """View for adding new files"""
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        try:
            StudyMaterialFile.objects.create(
                name=name,
                file=file,
                user=request.user
            )
            print("worked")
            messages.success(request, 'File uploaded successfully!')
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
    return redirect('mat')


def delete_note(request, note_id):
    """View for deleting notes"""
    try:
        note = StudyMaterialNotes.objects.get(id=note_id)
        note.delete()
        messages.success(request, 'Note deleted successfully!')
    except StudyMaterialNotes.DoesNotExist:
        messages.error(request, 'Note not found!')
    except Exception as e:
        messages.error(request, f'Error deleting note: {str(e)}')
        
    return redirect('mat')

def delete_file(request, file_id):
    """View for deleting files"""
    try:
        file = StudyMaterialFile.objects.get(id=file_id)
        file.delete()
        messages.success(request, 'File deleted successfully!')
    except StudyMaterialFile.DoesNotExist:
        messages.error(request, 'File not found!')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        
    return redirect('mat')

def add_lang(request):
    """View for adding new notes"""
    print(request.user)
    if request.method == 'POST':
        name = request.POST.get('lang')

        
        try:
            Language.objects.create(
                lang=name,

            )
            messages.success(request, 'Language added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding note: {str(e)}')
            
    return redirect('lang')

def delete_lang(request,lang_id):
    """View for deleting files"""
    try:
        file = Language.objects.get(id=lang_id)
        file.delete()
        messages.success(request, 'Language deleted successfully!')
    except Language.DoesNotExist:
        messages.error(request, 'Language not found!')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        
    return redirect('lang')


class QuestionsView(TemplateView):
    template_name = 'question_types.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['lang']=Language.objects.all()
        return context
    

def questions_view(request, lang_id):
    language = Language.objects.get(id=lang_id)
    questions = Questions.objects.filter(lang=language)
    context = {
        'questions': questions,
        'language': language
    }
    return render(request, 'questions.html', context)


def add_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        lang_id = request.POST.get('lang_id')
        try:
            language = Language.objects.get(id=lang_id)
            Questions.objects.create(
                question=question,
                user=request.user,
                lang=language
            )
            messages.success(request, 'Question added successfully!')
        except Exception as e:
            messages.error(request, 'Error adding question.')
    return redirect('questions_view', lang_id=lang_id)


def delete_ques(request,que_id,pk):
    """View for deleting files"""
    try:
        que = Questions.objects.get(id=que_id)
        que.delete()
        messages.success(request, 'Question deleted successfully!')
    except Questions.DoesNotExist:
        messages.error(request, 'Question not found!')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        
    return redirect('questions_view',lang_id=pk)


def student_results(request,pk):
    results = Result.objects.filter(question=pk)
    context = {
        'results': results
    }
    return render(request, 'student_detail.html', context)

def student_results_by_user(request,pk):
    results = Result.objects.filter(user=pk)
    context = {
        'results': results
    }
    return render(request, 'student_detail.html', context)



class ForgotPasswordView(FormView):
    template_name = "forgot_password.html"
    form_class = PasswordResetForm  
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email) 
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('uid')
            reset_url = self.request.build_absolute_uri(
                reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail(
                'Password Reset for CodeQuest',
                f'Please click the following link to reset your password: {reset_url}',
                'jipsongeorge753@gmail.com',  
                [email],
                fail_silently=False,
            )
            messages.success(self.request, "Password reset link has been sent to your email.")
            return redirect('login')
        except User.DoesNotExist:
            messages.success(self.request, "Password reset link has been sent to your email if the account exists.")
            return redirect('login')

from django.utils.http import urlsafe_base64_decode


class ResetPasswordConfirmView(FormView):
    template_name = "reset_password.html"
    form_class = SetPasswordForm
    
    def dispatch(self, request, *args, **kwargs):
        self.uid = kwargs.get('uidb64')
        self.token = kwargs.get('token')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.uid
        context['token'] = self.token
        return context
    def form_valid(self, form):
        try:
            from django.utils.http import urlsafe_base64_decode
            uid = urlsafe_base64_decode(self.uid).decode()
            user = CustomUser.objects.get(pk=uid)
            if default_token_generator.check_token(user, self.token):
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(self.request, "Your password has been reset successfully. You can now login.")
                return redirect('login')
            else:
                messages.error(self.request, "The reset link is invalid or has expired.")
                return redirect('forgot_password')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(self.request, "The reset link is invalid or has expired.")
            return redirect('forgot_password')