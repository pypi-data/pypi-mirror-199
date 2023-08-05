import os
import sys
import urllib.parse
import queue
#from six.moves import queue
import threading
import json
import enum
import io

import time
import datetime
import pyaudio
import ssl
from ws4py.client.threadedclient import WebSocketClient


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

######################### Logging configuration ################################
import logging
import logging.handlers
# create logger
logger = logging.getLogger('client')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logfh = logging.handlers.RotatingFileHandler('server.log', maxBytes=10485760, backupCount=10)
logfh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(u'%(levelname)8s %(asctime)s %(message)s ')
logging._defaultFormatter = logging.Formatter(u"%(message)s")

# add formatter to ch
ch.setFormatter(formatter)
logfh.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(logfh)
######################### Logging configuration ################################


def rate_limited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rate_limited_function(*args,**kargs):
            elapsed = time.perf_counter() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.perf_counter()
            return ret
        return rate_limited_function
    return decorate


class LiveStreamingClient(WebSocketClient):

    def __init__(self, url, speech_requests, protocols=None, extensions=None, heartbeat_freq=None, byterate=32000):
        
        super(LiveStreamingClient, self).__init__(url, protocols, extensions, heartbeat_freq)
        # logger.info("Connect to url: " + url)
        self.final_hyps = []
        self.final_hyps_json = []
        self.byterate = byterate
        self.final_hyp_queue = queue.Queue()
        self.requests = list(speech_requests)

        if not isinstance(self.requests, list) and not isinstance(self.requests[0], StreamingRecognizeRequest):
          raise Exception('StreamingRecognizeRequest', 'The input speech request is not valid list of StreamingRecognizeRequest or not supported by AbaxAI Speech Services')

    @rate_limited(25)
    def send_data(self, data):
        self.send(data, binary=True)

    def opened(self):
        # logger.info("Socket opened! ")
        pass

    def received_message(self, m):
        response = json.loads(str(m)) 
        def send_data_to_ws():
            # logger.info("Start transcribing...")
            for request in self.requests:
                if len(request.data) == 0:
                    break
                self.send_data(request.data)
            # logger.info("Audio sent, now sending EOS")
            self.send("EOS")

        if response['status'] == 0:
            if 'result' in response:
                trans = response['result']['hypotheses'][0]['transcript']
                if response['result']['final']:
                    print("Transcript: {}".format(trans))
                    
                    self.final_hyps.append(trans)
                    self.final_hyps_json.append(trans)
                    
        else:
            # logger.info("Received message from server (status %d)" % response['status'])
            if 'message' in response:
                # logger.info("Message: %s" %  response['message'])
                if response['message'] == 'ready':
                    #print('------------------------')
                    t = threading.Thread(target=send_data_to_ws)
                    t.start()
                else:
                    print(response)

    def get_full_hyp(self, timeout=1):
        self.final_hyp_queue.get(timeout)
        return self.final_hyps_json        

    def closed(self, code, reason=None):
        # logger.debug("Websocket closed() called with code %s and reason: %s" % (code, reason))
        self.final_hyp_queue.put(" ".join(self.final_hyps))


class SpeechClient(WebSocketClient):
    SPEECH_SERVER_URL = "wss://gatewayapi.speechlab.sg/client/ws/speech"
    
    def __init__(self):
        #logger.info("Welcome to Abax.AI Speech Services!")
        pass
  
    def streaming_recognize(self, config, requests):
        encoded_content_type = urllib.parse.urlencode([("content-type", config.getContentType())])
        encoded_token        = urllib.parse.urlencode([("accessToken", config.getAccessToken())])
        encoded_model        = urllib.parse.urlencode([("model", config.getAsrModel())])
        speech_url           = self.SPEECH_SERVER_URL + '?%s' % (encoded_content_type) + '&%s' % (encoded_token) + '&%s' % (encoded_model)

        ws = LiveStreamingClient(speech_url, requests, byterate=32000)
        
        ws.connect()
        responses = ws.get_full_hyp()
        
        return responses


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


class StreamingRecognitionConfig(object):
    def __init__(self, config, accessToken, interim_results=False, outputFormat=None, inverseNormalization=True):
        # Simple validation for access token
        if accessToken.strip() == '':
            raise Exception('AccessToken', 'Please provide the access token to Abax.AI Speech Services')
        else: 
            self._accessToken = accessToken
    
        if isinstance(config, RecognitionConfig):
            self._recognition_config = config     # Type: RecognitionConfig
        else:
            raise Exception('RecognitionConfig', 'Please provide an object of RecognitionConfig type')
            
        self._interim_results = interim_results           # Boolean: False - default, True
        self._outputFormat = outputFormat                 # String: text - default, json
        self._inverseNormalization = inverseNormalization # Boolean: True - default, False
        
    def getContentType(self):
        return self._recognition_config._getContentType()
      
    def getAccessToken(self):
        return self._accessToken
      
    def getAsrModel(self):
        return self._recognition_config._getSelectedModel()


class StreamingRecognizeRequest(object):
    def __init__(self, audio_content):
        #self._chunk = audio_content
        self.data = audio_content
        #logger.info("Set the content to audio chunk with size %s" % len(audio_content))

    def getData(self):
        # return self._chunk
        pass



'''
Revision History 
 - v0.0.1: Intial created
 - v0.0.2: Follow the best practices of Google Cloud Speech to Text and Rev.AI
 
'''
# End
