from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from .forms import *
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.conf import settings
import io
from PyPDF2 import PdfReader, PdfWriter
from django.http import FileResponse
import jwt




def encode_text(text):
    encoded_data = jwt.encode(payload={'token':text},
                              key='455@44hj@',
                              algorithm="HS256")

    return encoded_data



def decode_text(token):
    decoded_data = jwt.decode(jwt=token,
                              key='455@44hj@',
                              algorithms=["HS256"])

    return decoded_data





def home(request):

    context={}
    return render(request, 'etest/home3.html',context)

def resgister(request):

    if request.method == "POST":
        form = UserRegisteration(request.POST)
        if form.is_valid():
            try:
                data = form.save()
            except Exception as e:
                if 'UNIQUE constraint failed' in str(e):
                    context = {'form':form,'errors':['This username is already exist!']}
                    return render(request, 'etest/sign_up.html',context)
                else:
                    errors = [str(e)]
                    context = {'form':form,'errors':errors}
                    return render(request, 'etest/sign_up.html',context)

            user_data = AppUser.objects.get(pk = data.pk)
            user = authenticate(request, username=user_data.user, password=user_data.password)
            if user is not None:
                print('user Logined.....')
                login(request, user)
            return redirect('test')
        
        

    user_form = UserRegisteration()
    context = {'form':user_form}
    return render(request, 'etest/sign_up.html',context)

# @login_required(login_url='/')
def test(request):
    context = {}
    return render(request, 'etest/testpage2.html', context)


def logout_button(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/')
def audio_file(request):

    if request.method == "POST":
        form = AudioForm(request.POST,request.FILES)
        user = AppUser.objects.get(id = 1)
        file = request.FILES['audio']
        create_at = datetime.today()


        # audio_file = request.FILES.get('audio')
    
        # audio_content = audio_file.read()
   
        # with open('file.mp3', 'wb') as f:
        #     f.write(audio_content)


        # print("KKKKKKKKKK File created ")

        try:
            new_data = AudioData()
            new_data.user = user
            new_data.audio_file = file
            new_data.create_at = create_at
            new_data.save()

            encoded_token = encode_text(str(request.user.app_user.user))
            print("KKKKKKKKKL: ", encoded_token)

            data = {
                'status' : 200,
                'rank':'A1',
                # 'next_page_token' : encoded_token,
                'data' : []
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                'status' : 404,
                'message':f'Got error while uploading file!!! \n {str(e )}',
                'data' : []
            }
            return JsonResponse(data)



from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
@login_required(login_url='/')
def generate_certificate(request,level):
    # Load the certificate design image
    template_path = settings.STATICFILES_DIRS[0] + '/new_certificate_template.png'  # Replace with the actual path to your certificate design image
    template_image = Image.open(template_path)


    # certificate levels
    # Beginner level (CERF A1)
    # Pre-intermediate level (CERF A2)
    # Intermediate level (CERF B1)
    # Upper-Intermediate level	 (CERF B2)
    # Advanced	level (CERF C1)
    # Proficiency level (CERF C2)

    # Specify the font type, size, and color
    font_path = settings.STATICFILES_DIRS[0] + '/PTSerif_Bold.ttf'  # Replace with the actual path to your font file
    font_size = 40
    font_color = (0, 0, 0)  # Black color

    new_text = str(request.user.app_user.first_name) + " " + str(request.user.app_user.last_name)  # Replace with the new text you want to use
    level_text = str(level)


    
    edited_image = template_image.copy()
    draw = ImageDraw.Draw(edited_image)
    font = ImageFont.truetype(font_path, font_size)

    # Find the position to place the new text
    text_width, text_height = draw.textsize(new_text, font=font)
    position = ((edited_image.width - (text_width-30)) // 2, (edited_image.height - (text_height+250)) // 2)
    # Replace the old text with the new text
    draw.text(position, new_text, font=font, fill=font_color)


    text_width, text_height = draw.textsize(level_text, font=font)
    position = ((edited_image.width - (text_width-30)) // 2, (edited_image.height - (text_height-20)) // 2)
    # Replace the old text with the new text
    draw.text(position, level_text, font=font, fill=font_color)
    

    # Create a response and save the edited image
    response = HttpResponse(content_type='image/png')
    edited_image.save(response, format='PNG')
    edited_image.save(str(settings.STATICFILES_DIRS[0]) + '/Language_test333333.png', format='PNG')

    # Set the filename for the downloaded image
    response['Content-Disposition'] = 'attachment; filename="modified_certificate.png"'

    return response


@login_required(login_url='/')
def result_page(request,token):
    decoded_text = decode_text(token)
    # print("KKKKKKKKK: ", decoded_text['token'])
    if str(decoded_text['token']) == str(request.user.app_user.user):
        return render(request, 'etest/result.html')
    else:
        return HttpResponse("You did not pass the test so you can not download the certificate.")






def question_generator(request):

    if request.method == "GET":
    
        data = {
            'status' : 200,
            'prompt':'Tell us about yourself',
            'data' : []
        }
        return JsonResponse(data)
        