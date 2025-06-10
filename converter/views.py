from django.shortcuts import render
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from pdf2image import convert_from_bytes
from zipfile import ZipFile
from django.http import FileResponse, HttpResponse
import traceback
import io

def index(request):
    return render(request, 'index.html')

def image_to_pdf(request):
    if request.method == "POST":
        files = request.FILES.getlist("image_files")
        if not files:
            return HttpResponse("No files uploaded.", status=400)

        image_list = []
        for f in files:
            image = Image.open(f)
            image = image.convert("RGB")
            image_list.append(image)

        buffer = io.BytesIO()
        image_list[0].save(buffer, format="PDF", save_all=True, append_images=image_list[1:])
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
        return response

    return HttpResponse("Invalid request", status=400)

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from pdf2image import convert_from_bytes
from io import BytesIO
import traceback

def pdf_to_image(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        uploaded_pdf = request.FILES['pdf_file']
        poppler_path = r"C:\poppler-24.08.0\Library\bin"  # ✅ Make sure path is valid

        try:
            print("📄 Received PDF upload")
            # Convert only the first page
            images = convert_from_bytes(uploaded_pdf.read(), fmt='jpeg', first_page=1, last_page=1, poppler_path=poppler_path)
            print("✅ First page converted to JPEG")

            image = images[0]
            img_io = BytesIO()
            image.save(img_io, format='JPEG')
            img_io.seek(0)

            return FileResponse(img_io, as_attachment=True, filename='converted_page.jpeg', content_type='image/jpeg')

        except Exception as e:
            print("❌ Error:", e)
            traceback.print_exc()
            return HttpResponse(f"Conversion error: {e}", status=500)

    return render(request, 'index.html')








def compress_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image = Image.open(image_file)

            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', optimize=True, quality=60)
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='image/jpeg')
            response['Content-Disposition'] = 'attachment; filename="compressed.jpg"'
            return response

    return render(request, 'compress_image.html')