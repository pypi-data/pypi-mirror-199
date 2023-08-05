"""
Client module calling remote ASR 
@Updated: October 01, 2020
@Maintain by: Ly
"""

import os, time
import sys
import json
import enum
import requests
import subprocess
import shutil
import urllib.request

import zipfile

__version__ = "1.0.0"
__author__  = "AISpeechlab - NTU"
__status__  = "Release"
__all__     = ['get_audio_length', 'send_audio', 'check_status', 'get_transcription']


class SpeechClient(object):
    _SPEECH_URL = 'https://gatewayapi.speechlab.sg'

    def __init__(self):
        #logger.info("Welcome to Abax.AI Speech Services!")
        self.request_token = ""
        self.request_header = {'accept': 'application/json', 'Authorization': ""}
        self.request_queue = 'normal'

  
    def recognize(self, config, audiofilepath):
        self.config = config
        self.encoded_content_type = config.getContentType()
        self.request_token  = config.getAccessToken()
        self.request_header = {'accept': 'application/json', 'Authorization': 'Bearer ' + self.request_token}
        self.request_language = config.getAsrModel()

        if not isinstance(self.config, TranscribeConfig):
          raise Exception('TranscribeConfig', 'The input config is not a valid TranscribeConfig or not supported by AbaxAI Speech Services')
        
        audiofile = audiofilepath
        audio_length_in_seconds = self.get_audio_length(audiofile)
        _time_delay = max(60.0, audio_length_in_seconds) # The lowest boundary is 1min. 
        
        speech_id = self.send_audio(audiofile)
        print('... Getting speech id %s ...' % speech_id)
        if (speech_id == None):
            sys.exit("*** You don't have a speech id to process.")
        
        completed = False
        _MAX_TRY = 10
        i = 0
        while (completed != "done") and i < _MAX_TRY:
            time.sleep(_time_delay)
            i += 1
            print('... %02d waiting ASR result ...' % i)
            completed = self.check_status(speech_id)

        if (completed != "done"):
            print('*** Error: ASR did not complete the transcription')
        else:
            print('*** ASR done!')
            print('... Downloading transcription ...')
            self.download_trans(speech_id)
            print('*** Finish downloading transcription!')


    def get_audio_length(self, audiofile):
        ''' Check the audio length of input audio '''
        # cmd: ffmpeg -i file.mkv 2>&1 | grep -o -P "(?<=Duration: ).*?(?=,)"
        p1 = subprocess.Popen(['ffmpeg',  '-i', audiofile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p2 = subprocess.Popen(["grep",  "-o", "-P", "(?<=Duration: ).*?(?=,)"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        
        # print("The audio file length in hh:mm::ss format: " + p2.communicate()[0].decode("utf-8").strip())
        
        cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(audiofile)
        output = subprocess.check_output(
            cmd,
            shell=True, # Let this run in the shell
            stderr=subprocess.STDOUT
        )
        # return round(float(output))  # ugly, but rounds your seconds up or down
        print("The audio file length in seconds: " + str(float(output)))
        return float(output)
        

    def check_status(self, speech_id):
        ''' Check ASR status with given id '''
        try:
            url = self._SPEECH_URL + '/speech/' + speech_id
            res = requests.get(url, headers=self.request_header)
            res = res.json()
            cur_status = res['status']
            print("... Current status: " + cur_status)
            return cur_status
            
        except Exception as ex:
            print('... Error in getting ASR status: ', str(ex))


    def download_trans(self, speech_id):
        try:
            url = self._SPEECH_URL + '/speech/' + speech_id + '/result'
            res = requests.get(url, headers=self.request_header)
            result_link = res.json()['url']
            print("... Downloading transcripts ")

            with urllib.request.urlopen(result_link) as response, open(speech_id + '.zip', 'wb') as out_file:
                content_length = int(response.getheader('Content-Length'))
                shutil.copyfileobj(response, out_file)

            print(f"... File saved. {content_length:,} bytes.")
            with zipfile.ZipFile(speech_id + '.zip', 'r') as zip_ref:
                zip_ref.extractall(speech_id)

            os.remove(speech_id + '.zip')

            return res.ok
        
        except Exception as ex:
            print('... Error in getting ASR status: ', str(ex))


    def get_transcription(self, speech_id, token):
        try:
            self.request_header = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}

            url = self._SPEECH_URL + '/speech/' + speech_id + '/result'
            res = requests.get(url, headers=self.request_header)
            result_link = res.json()['url']

            with urllib.request.urlopen(result_link) as response, open(speech_id + '.zip', 'wb') as out_file:
                content_length = int(response.getheader('Content-Length'))
                shutil.copyfileobj(response, out_file)

            with zipfile.ZipFile(speech_id + '.zip', 'r') as zip_ref:
                zip_ref.extractall(speech_id)

            os.remove(speech_id + '.zip')

            return res.ok
        
        except Exception as ex:
            print('... Error in getting ASR status: ', str(ex))


    def send_audio(self, audio_file):
        ''' Send an audio file to remote ASR server '''
        try:
            url = self._SPEECH_URL + '/speech'
            files = {
                    'file':  open(audio_file, 'rb'),
            }
            data = {
                'lang': self.request_language,
                'queue': self.request_queue # this is important, you must parse correct queue for your account here
            }
            
            res = requests.post(url, files=files, data=data, headers=self.request_header)
            res = res.json()
            
            speech_id=None
            if ('statusCode' in res and res['statusCode'] == 404):
                print('... Error in submitting audio(s): ', str(res), '. \nPlease check your token again.')
            
            elif ('statusCode' in res and res['statusCode'] == 403):
                print('... Error in submitting audio(s): ', str(res), '. \nPlease change your queue information.')

            else: 
                speech_id = res['_id']
            return speech_id
            
        except Exception as ex:
            print('... Exception in submitting audio(s): ', str(ex))


class TranscribeConfig(object):
    def __init__(self, config, accessToken, outputFormat=None, inverseNormalization=True):
        # Simple validation for access token
        if accessToken.strip() == '':
            raise Exception('accessToken', 'Please provide the access token to Abax.AI Speech Services')
        else: 
            self._accessToken = accessToken
    
        if isinstance(config, RecognitionConfig):
            self._recognition_config = config     # Type: RecognitionConfig
        else:
            raise Exception('RecognitionConfig', 'Please provide an object of RecognitionConfig type')
            
        self._outputFormat = outputFormat                 # String: text - default, json
        self._inverseNormalization = inverseNormalization # Boolean: True - default, False
        
    def getContentType(self):
        return self._recognition_config._getContentType()
      
    def getAccessToken(self):
        return self._accessToken
      
    def getAsrModel(self):
        return self._recognition_config._getSelectedModel()


class AudioEncoding(enum.Enum):
    '''Reference https://cloud.google.com/speech-to-text/docs/reference/rest/v1/RecognitionConfig#AudioEncoding'''
    
    ENCODING_UNSPECIFIED = 1 # Not specified.
    LINEAR16 = 2             # Uncompressed 16-bit signed little-endian samples (Linear PCM).
    FLAC = 3                 # FLAC (Free Lossless Audio Codec) is the recommended encoding because it is lossless
    MULAW	= 4                # 8-bit samples that compand 14-bit audio samples using G.711 PCMU/mu-law.
    AMR	= 5                  # Adaptive Multi-Rate Narrowband codec. sampleRateHertz must be 8000.
    AMR_WB = 6               # Adaptive Multi-Rate Wideband codec. sampleRateHertz must be 16000.
    OGG_OPUS = 7             # Opus encoded audio frames in Ogg container (OggOpus). sampleRateHertz must be one of 8000, 12000, 16000, 24000, or 48000.
    SPEEX_WITH_HEADER_BYTE = 8 # Although the use of lossy encodings is not recommended, 
                               # if a very low bitrate encoding is required, OGG_OPUS is highly preferred over Speex encoding.  
                               # Only Speex wideband is supported. sampleRateHertz must be 16000.
    WEBM_OPUS = 9            # Opus encoded audio frames in WebM container (OggOpus). 
                             # sampleRateHertz must be one of 8000, 12000, 16000, 24000, or 48000.
    MP3_EXT = 10             # File extension(s)
    MP4_EXT = 11
    AAC_EXT = 12
    AC3_EXT = 13
    AIFF_EXT = 14
    FLAC_EXT = 15
    OGG_EXT = 16
    OPUS_EXT = 17
    TS_EXT = 18
    WMA_EXT = 19


class RecognitionConfig(object):

    def __init__(self, encoding, sample_rate_hertz, language_code, model):
        self._encoding = encoding                 # AudioEncoding.LINEAR16
        self._sampleRateHertz = sample_rate_hertz # Value in range: 8000 - 48000
        self._languageCode = language_code
        
        self._audioChannelCount = 1
        self._maxAlternatives = 10
        self._enableWordTimeOffsets = False
        self._enableWordConfidence = False
        self._enableAutomaticPunctuation = False
        self._enableSpokenPunctuation = False
        self._diarizationConfig = "default" # LIUM
        self._metadata = "" # unused for now
        self._model = model
        self._useEnhanced = False
        
        self._validateAudioEncoding()
        self._validateNoChannels()
    
    def _validateAudioEncoding(self):
        if not isinstance(self._encoding, AudioEncoding):
          raise Exception('AudioEncoding', 'The input audio encoding is not valid AudioEncoding or not supported by AbaxAI Speech Services')
        
    def _validateNoChannels(self):
        if (self._encoding in [AudioEncoding.LINEAR16, AudioEncoding.FLAC]) and (self._audioChannelCount < 1 or self._audioChannelCount > 8):
          raise Exception('Invalid channel count', 'Valid values for LINEAR16 and FLAC are 1-8')
        if (self._encoding in [AudioEncoding.OGG_OPUS]) and (self._audioChannelCount < 1 or self._audioChannelCount > 254):
          raise Exception('Invalid channel count', 'Valid values for OGG_OPUS are 1-254')
        if (self._encoding in [AudioEncoding.MULAW, AudioEncoding.AMR, AudioEncoding.AMR_WB, AudioEncoding.SPEEX_WITH_HEADER_BYTE]) and (self._audioChannelCount != 1):
          raise Exception('Invalid channel count', 'Valid value for MULAW, AMR, AMR_WB and SPEEX_WITH_HEADER_BYTE is only 1')
        
    def _validateModel(self):
        pass

    def _getContentType(self):
        cfg_content_type = "audio/x-raw, layout=(string)interleaved, rate=(int)%d, format=(string)S16LE, channels=(int)%d" % (self._sampleRateHertz, self._audioChannelCount)
        return cfg_content_type
  
    def _getSelectedModel(self):
        return self._model