import socket

#ERROR HANDELING
MASK_ERRORS = False

#TESSERACT CONFIG
TESSERACT_EXE = 'tesseract'
TESSERACT_SCRATCH = '/tmp/'
TESSERACT_CLEANUP = True

#JSON RESPONSES
JSON_SUCCESS = { 'status':'success' }
JSON_NOIMAGE = { 'status':'failed', 'code':100, 'error':'Required file "image" was not supplied in POST' }
JSON_NOIMAGEID = { 'status':'failed', 'code':101, 'error':'Required field "image_id" was not supplied in POST' }
JSON_NONEIMAGE = { 'status':'failed', 'code':102, 'error':'The file in the "image" POST variable does not appear to be an image' }
JSON_OCRFAILED = { 'status':'failed', 'code':103, 'error':'The OCR engine could not read the image' }

#DEV SPECIFIC CONFIG
if socket.gethostname() == 'matt-griffiths':
    MASK_ERRORS = False
    pass