from django.shortcuts import render, redirect


def FriendsView(request):
    if request.user.is_anonymous():
        return redirect('social:begin', backend='facebook')
    return render(request, 'index.html', {'user': request.user})
