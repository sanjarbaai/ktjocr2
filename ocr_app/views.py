from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from ocr.ocr import read_document
from ocr.utils.pdf_reader import extract_pages

from .models import PDFFile, OCRResult
from .forms import PDFUploadForm

import json


@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.save(commit=False)
            pdf_file.user = request.user
            pdf_file.save()
            return redirect('view_pdf', pdf_id=pdf_file.id)
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf/upload_pdf.html', {'form': form})


@login_required
def view_pdf(request, pdf_id):
    pdf_file = get_object_or_404(PDFFile, id=pdf_id, user=request.user)
    pages = extract_pages(pdf_file.file.path)
    if not pages:
        return render(request, 'error/error.html', {'message': 'An error occurred while processing the PDF.'})

    box_names = ["09029", "04021", "02016", "01207", "01707", "09015"]
    context = {
        'pdf_file': pdf_file,
        'pages': pages,
        'box_names': box_names,
    }
    return render(request, 'view_pdf/view_pdf.html', context)


@csrf_exempt
@login_required
@require_POST
def receive_box_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        box_images = data.get('box_images')
        pdf_id = data.get('pdf_id')
        pdf_file = get_object_or_404(PDFFile, id=pdf_id, user=request.user)

        documents = read_document(box_images, pdf_file)
                
        request.session['documents'] = json.dumps(documents)
        request.session['pdf_id'] = pdf_id
        
        return JsonResponse({
            'success': True,
            'pdf_id': pdf_file.id
        })
    return JsonResponse({'success': False})


@login_required
def ocr_results(request, pdf_id):
    pdf_file = get_object_or_404(PDFFile, id=pdf_id, user=request.user)

    documents_json = request.session.get('documents', '[]')
    print(documents_json)
    documents = [json.loads(doc) for doc in json.loads(documents_json)]

    context = {
        'pdf_file': pdf_file,
        'documents': documents
    }

    return render(request, 'results/results.html', context)

