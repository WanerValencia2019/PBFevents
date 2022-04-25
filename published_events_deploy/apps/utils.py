import base64
import tempfile
import uuid

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_binary_content(base64_image) -> tempfile.TemporaryFile or None:
	if len(base64_image) != 0 and len(base64_image)%4==0:
		encoded_bs4 = base64_image
		encoded_bytes=encoded_bs4.encode('utf-8')
		try: 
			binary = base64.decodebytes(encoded_bytes)
			print(dir(binary))
			fp = tempfile.TemporaryFile()
			fp.write(binary)
			print(fp)
			return fp
		except:
			return None
	return None

