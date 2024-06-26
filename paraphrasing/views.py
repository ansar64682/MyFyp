from django.shortcuts import render
from .paraphrase import paraphrase_text

def paraphrase_view(request):
    original_text = None
    paraphrased_text = None

    if request.method == "POST":
        original_text = request.POST.get('text', None)
        if original_text:
            paraphrased_text = paraphrase_text(original_text)

    return render(request, 'paraphrasing/paraphrase.html', {
        'original_text': original_text,
        'paraphrased_text': paraphrased_text
    })

