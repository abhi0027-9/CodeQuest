from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
import tempfile
import sys
from io import StringIO
from faculty.models import *
from django.utils import timezone
import subprocess
import re
from .python_groq import *
from django.http import JsonResponse
from django.contrib import messages
from faculty.forms import *
from django.contrib.auth import update_session_auth_hash

class UserHomeView(TemplateView):
    template_name = 'userhome.html'


def Python_Compiler(request):
    if request.method == "POST":
        codeareadata = request.POST.get('codearea', '')  
        output = None 
        result = None 
        try:
            original_stdout = sys.stdout
            output_buffer = StringIO()
            sys.stdout = output_buffer
            exec(codeareadata, globals(), locals())
            output = output_buffer.getvalue()
            result = check_outputcode_with_groq(codeareadata.strip(), output)
        except Exception as e:
            output = str(e)
            result = check_error(output, codeareadata)
        finally:
            sys.stdout = original_stdout
    else:
        codeareadata = ''
        output = ''
        result = ''
    return render(request, 'compiler_python.html', {"code": codeareadata, "output": output,'result':result})



def challenge_languages(request):
    languages = Language.objects.all()
    return render(request, 'challenges_lang.html', {'languages': languages})


def view_challenges(request, lang_id):
    language = Language.objects.get(id=lang_id)
    challenges = Questions.objects.filter(lang=language)
    solved_questions = Result.objects.filter(user=request.user,is_correct=True,question__lang=language).select_related('question')   
    solved_ids = {result.question_id for result in solved_questions}   
    for challenge in challenges:
        challenge.is_solved = challenge.id in solved_ids
        
    return render(request, 'challenges.html', {'challenges': challenges, 'language': language})

import builtins

def solve_challenge(request, challenge_id):
    challenge = Questions.objects.get(id=challenge_id)
    
    if request.method == "POST":
        code = request.POST.get('codearea', '')
        user_input = request.POST.get('user_input', '')
        
        if code == '':
            return redirect('solve_challenge', challenge_id)
        
        try:
            output = None
            original_stdout = sys.stdout
            original_stdin = sys.stdin
            
            # Handle input
            input_lines = user_input.strip().split('\n')
            input_line_index = 0
            
            def mock_input(prompt=''):
                nonlocal input_line_index
                print(prompt, end='')
                if input_line_index < len(input_lines):
                    result = input_lines[input_line_index]
                    input_line_index += 1
                    print(result)  # Echo the input as if user typed it
                    return result
                return ''  # Return empty string if no more input
            
            # Set up output capture
            output_buffer = StringIO()
            sys.stdout = output_buffer
            
            # Replace built-in input with our mock
            builtins.input = mock_input
            
            # Execute the code
            exec(code, globals(), locals())
            
            # Get captured output
            output = output_buffer.getvalue()
            
            # Check if the solution is correct
            result = check_output_with_groq(code.strip(), challenge)
            
        except Exception as e:
            output = str(e)
            result = check_error_with_groq(output, challenge, code)
        finally:
            # Restore standard I/O
            sys.stdout = original_stdout
            builtins.input = original_stdin
        
        # Analyze the code and provide feedback
        feedback = analyze_code_with_groq(code, output.strip(), challenge)
        
        # Extract score from feedback
        match = re.search(r"Score:\s*(\d+)", feedback)
        score = int(match.group(1)) if match else 0
        
        # Determine if the solution is correct
        if score >= 4:
            is_correct = 1 
        else: 
            is_correct = 0
        
        # Save the result
        results, created = Result.objects.get_or_create(
            question=challenge,
            user=request.user,
            defaults={"is_correct": is_correct, "score": score, "feedback": feedback},
        )
        
        if not created:  
            results.is_correct = is_correct
            results.score = score
            results.feedback = feedback
            results.attempt_time = timezone.now()
            results.save()
        
        return render(request, 'solve_challenge.html', {
            "challenge": challenge,
            "code": code,
            "user_input": user_input,
            "output": output,
            "feedback": feedback,
            "result": result,
            "score": score
        }) 
    
    return render(request, 'solve_challenge.html', {
        "challenge": challenge,
        "code": "",
        "user_input": "",
        "output": "",
        "feedback": "",
        "result": "",
        "score": 0
    })



def compile_php(request, challenge_id):
    challenge = Questions.objects.get(id=challenge_id)
    if request.method == 'POST':
        code = request.POST.get('code', '')

        php_executable = "D:/PHP/php.exe"  # Adjust the path to your PHP installation

        if not code.strip().startswith("<?php"):
            code = "<?php\n" + code

        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".php") as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            result = subprocess.run([php_executable, temp_file_path], capture_output=True, text=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            print(output)
            result = check_output_with_groqphp(code.strip(), challenge)
        except Exception as e:
            output = str(e)
            result = check_error_with_groq_php(output, challenge,code)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  

        feedback = analyze_code_with_groqphp(code, output.strip(), challenge)
        match = re.search(r"Score:\s*(\d+)", feedback)
        score = int(match.group(1)) if match else 5
        if score == 5 or score ==4:
            is_correct = 1
        else:
            is_correct =0
        results, created = Result.objects.get_or_create(
            question=challenge,
            user=request.user,
            defaults={"is_correct": is_correct, "score": score, "feedback": feedback},
)

        if not created:
            results.is_correct = is_correct
            results.score = score
            results.feedback = feedback
            results.attempt_time = timezone.now()
            results.save()
        return render(request, 'php_compiler.html', {'code': code, 'output': output,'challenge':challenge,'result':result,'feedback':feedback})
    return render(request, 'php_compiler.html', {'code': '', 'output': '','challenge':challenge,'feedback':'','result':''})


def solve_challengephp(request, challenge_id):
    challenge = Questions.objects.get(id=challenge_id)
    
    if request.method == "POST":
        code = request.POST.get('codearea','')
        print(code)
        
        if  code=='':
            return redirect('solve_challenge_php',challenge_id)
        
        try:
            with open("temp_script.php", "w") as f:
                f.write(code)
            outputs = subprocess.run(["php", "temp_script.php"], capture_output=True, text=True)
        
            output = outputs.stdout
            result = check_output_with_groqphp(code.strip(), challenge)
        except Exception as e:
            output = str(e)
            result = check_error_with_groq_php(output, challenge,code)

        feedback = analyze_code_with_groqphp(code, output.strip(), challenge)
    
        match = re.search(r"Score:\s*(\d+)", feedback)
        score = int(match.group(1)) if match else 5
        if score == 5 or score ==4:
            is_correct = 1
        else:
            is_correct =0
       
        results, created = Result.objects.get_or_create(
            question=challenge,
            user=request.user,
            defaults={"is_correct": is_correct, "score": score, "feedback": feedback},
        )

        if not created:  
            results.is_correct = is_correct
            results.score = score
            results.feedback = feedback
            results.attempt_time = timezone.now()
            results.save()

        return render(request, 'php_compiler.html', {
            "challenge": challenge,
            "code": code,
            "output": output,
            "feedback": feedback,
            "result": result,
            "score": score
        })
       
    return render(request, 'php_compiler.html', {
        "challenge": challenge,
        "code": "",
        "output": "",
        "feedback": "",
        "result": "",
        "score": 0
    })

from django.db.models import Sum,Count,Q
from django.db.models.functions import Coalesce

class LeaderboardView(TemplateView):
    template_name= 'leaderboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        leaderboard = (
            Result.objects.values('user__student__student_name', 'user__id')
            .annotate(
                points=Coalesce(Sum('score') * 10, 0),  
                challenges_solved=Count('question', filter=Q(is_correct=True))
            )
            .order_by('-points')  # Order by points in descending order
        )

        print("Leaderboard Data:", leaderboard)

        ranked_leaderboard = []
        prev_points = None
        rank = 0
        actual_rank = 0  # This keeps track of the position in the list

        for user in leaderboard:
            actual_rank += 1  # Increment actual position in the list
            if user['points'] != prev_points:
                rank = actual_rank  # Assign new rank if points are different
            user['rank'] = rank  # Assign the computed rank
            ranked_leaderboard.append(user)
            prev_points = user['points']

        context['leaderboard'] = ranked_leaderboard
        return context



@login_required
def community(request):
    discussions = Discussion.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    
    # Handle search
    query = request.GET.get('search')
    if query:
        discussions = discussions.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Handle tag filtering
    tag_filter = request.GET.get('tag')
    if tag_filter:
        discussions = discussions.filter(tags__name=tag_filter)
    
    context = {
        'community': discussions,
        'tags': tags,
    }
    return render(request, 'community.html', context)

@login_required
def create_discussion(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_names = request.POST.getlist('tags')
        
        discussion = Discussion.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        
        # Handle tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            discussion.tags.add(tag)
        
        return redirect('community')
    
    return redirect('community')

@login_required
def like_discussion(request, discussion_id):
    if request.method == 'POST':
        discussion = Discussion.objects.get(id=discussion_id)
        discussion.likes += 1
        discussion.save()
        return redirect('community')
    
    return redirect('community')

@login_required
def add_comment(request, discussion_id):
    if request.method == 'POST':
        discussion = Discussion.objects.get(id=discussion_id)
        content = request.POST.get('content')
        
        comment = Comment.objects.create(
            discussion=discussion,
            author=request.user,
            content=content
        )
        
        return redirect('community')
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    if request.user == discussion.author:  # Ensure only the author can delete
        discussion.delete()
        messages.success(request, "Discussion deleted successfully!")
    else:
        messages.error(request, "You are not allowed to delete this discussion.")

    return redirect('community')


class MaterialsUserView(TemplateView):
    template_name = 'materials_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        videos = StudyMaterialNotes.objects.filter(user=self.request.user)
        for video in videos:
            if "youtube.com" in video.text or "youtu.be" in video.text:
                video.embed_url = self.convert_youtube_url(video.text)  
            else:
                video.embed_url = video.text  # Keep other video URLs as is

        context['videos'] = videos
        context['files'] = StudyMaterialFile.objects.filter(user=self.request.user)
        return context

    def convert_youtube_url(self, url):
        """ Convert YouTube URL to embedded format """
        import re
        if "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
        elif "youtube.com/watch" in url:
            video_id = re.search(r"v=([^&]+)", url)
            video_id = video_id.group(1) if video_id else None
        else:
            return url  # Return original URL if not a YouTube link

        return f"https://www.youtube.com/embed/{video_id}"




class PythonGamesView(TemplateView):
    template_name = 'python_games.html'



class PuzzleView(TemplateView):
    template_name = 'puzzle.html'

class ExploredGameView(TemplateView):
    template_name = 'game1.html'



@login_required
def ChangePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "Your password has been changed successfully!")
            return redirect("login")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, "change_password.html", {"form": form})
