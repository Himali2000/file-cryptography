from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.http.response import HttpResponseRedirect
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from .forms import InputForm
from .models import Cryptdb
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

'''def handler404(request, exception):
        data = {}
        return render(request,'filecryptography/404.html', data)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
'''

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def upload_file(request):
    if request.method == 'POST':
        save_the_form = InputForm(request.POST, request.FILES)
        if save_the_form.is_valid():
            save_the_form.save()
            return HttpResponseRedirect('/success/url')
    else:
        form = InputForm()
    return render(request, 'home.html', {'form': form})

class MainpageView(CreateView):
    model = Cryptdb
    form_class = InputForm
    success_url = 'download'
    template_name = 'home.html'

class DownloadpageView(ListView):
    model = Cryptdb
    template_name = 'download.html'

    def get(self, request):
        form = InputForm()
        
        var = Cryptdb.objects.all().order_by('-id')[:1].get()
        
        # Open last uploaded file's data in bytes mode
        with open(var.inputfile.path, "rb") as f:
            file_data = f.read()
        
        # Choose between encryption or decryption
        if var.function == 'ENCRYPT':

            # Get filename and make new filename
            enc_name = var.inputfile.name
            enc_file_name = "ENC" + enc_name[7:]
        
            # One-Tap Key
            if var.type == 'OTK':
                thekey = Fernet.generate_key()
                key_obj = Fernet(thekey)
                encript = key_obj.encrypt(file_data)
            
            # AES CBC and AES CFB
            if var.type == 'AESCBC' or var.type == 'AESCFB':
                thekey = get_random_bytes(32)
                
                if var.type == 'AESCBC':
                    aesobj = AES.new(thekey, AES.MODE_CBC)
                    encript = aesobj.encrypt(pad(file_data, AES.block_size))
                
                else:
                    aesobj = AES.new(thekey, AES.MODE_CFB)
                    encript = aesobj.encrypt(file_data)

                ivstring = b64encode(aesobj.iv).decode('utf-8')
                var.ivfile.save('theivfile', ContentFile(ivstring))

            # Base 64
            if var.type == 'BASESF':
                thekey = 'NULL'
                encript = base64.b64encode(file_data)

            # Save the key and encrypted file in DB fields
            var.keyfile.save('thekeyfile', ContentFile(thekey))
            var.encryptedfile.save(enc_file_name, ContentFile(encript))
        
        else:
            # From latest file name make new filename
            dec_name = var.inputfile.name
            find_file = dec_name[10:]
            dec_file_name = "DEC" + find_file
            
            # Search the corresponding encrypted file using the new filename
            to_dec = Cryptdb.objects.all().filter(encryptedfile__contains=find_file).get()

            # Open the key file
            with open(to_dec.keyfile.path, "rb") as f:
                    thekey = f.read()

            # One-Tap Key
            if to_dec.type == 'OTK':
                keyob = Fernet(thekey)
                decript = keyob.decrypt(file_data)
            
            # AES CBC and AES CFB
            if to_dec.type == 'AESCBC' or to_dec.type == 'AESCFB':
                with open(to_dec.ivfile.path, 'rb') as f:
                    iv = f.read()
                ivstring = b64decode(iv)
                
                if to_dec.type == 'AESCBC':
                    aesobj = AES.new(thekey, AES.MODE_CBC, ivstring)
                    decript = unpad(aesobj.decrypt(file_data), AES.block_size)

                else:
                    aesobj = AES.new(thekey, AES.MODE_CFB, iv = ivstring)
                    decript = aesobj.decrypt(file_data)
            
            # Base 64
            if to_dec.type == 'BASESF':
                decript = base64.b64decode(file_data)

            # Save the decrypted file in DB
            var.decryptedfile.save(dec_file_name, ContentFile(decript))

            # Delete the encrypted file
            to_dec.inputfile.delete()
            to_dec.encryptedfile.delete()
            to_dec.delete()

        args = {'form': form, 'var': var}
        return render(request, self.template_name, args)
