from django.shortcuts import render
from .keywordtool import get_keywords

def keyword_tool_view(request):
    long_tail_keywords = []
    lsi_keywords = []
    keyword = ""

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        if keyword:
            long_tail_keywords, lsi_keywords = get_keywords(keyword)

    return render(request, 'keywordtool/index.html', {
        'keyword': keyword,
        'long_tail_keywords': long_tail_keywords,
        'lsi_keywords': lsi_keywords
    })
