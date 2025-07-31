from django.urls import path
from .views import *

urlpatterns = [
    path('user-home/',UserHomeView.as_view(),name='uhome'),
    path('compiler-python/',Python_Compiler,name='compiler_python'),
    path('challenges/', challenge_languages, name='challenge_languages'),
    path('leaderboard/', LeaderboardView.as_view(), name='lead'),
    path('challenges/<int:lang_id>/', view_challenges, name='view_challenges'),
    path('challenge/<int:challenge_id>/', solve_challenge, name='solve_challenge'),
    path('challenge-php/<int:challenge_id>/', compile_php, name='solve_challenge_php'),
    path('community/', community, name='community'),
    path('community/create/', create_discussion, name='create_discussion'),
    path('community/like/<int:discussion_id>/', like_discussion, name='like_discussion'),
    path('community/comment/<int:discussion_id>/', add_comment, name='add_comment'),
    path('delete-discussion/<int:discussion_id>/', delete_discussion, name='delete_discussion'),
    path('materials-User/', MaterialsUserView.as_view(), name='materials'),
    path('games/', PythonGamesView.as_view(), name='games'),
    path('module-explorer/', ExploredGameView.as_view(), name='game1'),
    path('puzzle/', PuzzleView.as_view(), name='puzzle'),
    path('change-password/',ChangePasswordView,name='change-password'),

]