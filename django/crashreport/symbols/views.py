# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .handler import SymbolsUploadHandler

import os

class UploadSymbolsForm(forms.Form):
    symbols = forms.FileField()
    comment = forms.CharField()

def handle_uploaded_file(f):
    file_path = os.path.join(settings.SYMBOL_UPLOAD_DIR, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_path

@csrf_exempt
@login_required
def upload_symbols(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')

    form = UploadSymbolsForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseNotAllowed('Invalid data')

    path = handle_uploaded_file(request.FILES['symbols'])
    upload = SymbolsUploadHandler()
    upload.process(form.cleaned_data, path)

    # TODO: moggi: maybe report the zipfile.BadZipfile exception

    return HttpResponse("Success")

# vim:set shiftwidth=4 softtabstop=4 expandtab: */
