# RTC SCORE
## AUDIO
* packetLoss (0-100%): The percentage of audio packets lost. 
<!-- use the stat "fractionLost" -->
<!-- included for remote inbound RIA-->
* roundTripTime (milliseconds): The roundTripTime defines the degradation of the experience based on the network delay.
<!--included for remote inbound RIA and remote outbound (ROA6666) audio *DECIDE*-->
* bitrate (0-200000 bps): The bitrate used for the audio transmission.  Higher bitrates provides better quality.  
<!--bitrate in bits per second (same unit as the output we already get)-->
<!-- bytesReceived_in_bits/s included for inbound IT01A6666-->
* bufferDelay (milliseconds): The bufferDelay defines the degradation of the experience based on the delay introudced in reception that in most of the cases will be based on the jitter of the network.
<!-- use the stat "jitterBufferDelay" -->
<!-- included for inbound IT01A6666 -->
* fec (boolean): Defines if opus forward error correction was enabled or not to estimate the impact of packet loss in the quality of the experience.
* dtx (boolean): Defines if opus discontinuous transmission was enabled or not to ignore the bitrate in that case and also include an small additional degradation in the calculations in this case.
<!-- use the stat "[codec]" -->
<!-- inbound IT01A6666-->
<!-- entries are like:
\"opus (111, minptime=10;useinbandfec=1)\",
or
\"opus (111, minptime=10;sprop-stereo=0;stereo=0;usedtx=1;useinbandfec=1)\"
so we need to search for the items "usedtx" and "useinbandfec" which aren't always there but when they are there it means they were in use
-->
## VIDEO
* packetLoss (0-100%): The percentage of video packets lost.
<!-- use the stat "fractionLost" -->
<!-- included for remote inbound RIV-->
* bitrate (0-200000 bps): The bitrate used for the video transmission.  Higher bitrates provides better quality. 
<!--bitrate in bits per second (same unit as the output we already get)-->
<!--we could add sent and recieved together apparently? not sure how best to handle this one *DECIDE*-->
<!-- bytesReceived_in_bits/s included for inbound IT01V-->
* roundTripTime (milliseconds): The roundTripTime defines the degradation of the experience based on the network delay.
<!--included for remote inbound RIV-->
* bufferDelay (milliseconds): The bufferDelay defines the degradation of the experience based on the delay introudced in reception that in most of the cases will be based on the jitter of the network.
<!-- use the stat "jitterBufferDelay" -->
<!-- included for inbound I01V-->
* codec (AV1/ VP8 / VP9 / H264): The more modern codecs can provide better quality for the same amount of bitrate.  The current version of the algorithm considers VP8 and H264 the same and assumes a ~20% improvement of encoding efficiency in case of VP9.
<!-- *EDIT THIS* also include an efficiency improvement for video codec AV1 of 30%-->
<!-- use stat [codec] included inbound IT01V-->
<!-- entries for outbound are like:
"[\"VP9 (98, profile-id=0;useadaptivelayering=true;useadaptivelayering_v2=true)\",
or 
\"AV1 (45, level-idx=5;profile=0;tier=0;useadaptivelayering=true;useadaptivelayering_v2=true)\",
need to search for the first part of the string at each entry could be AV1, VP9, VP8, H264 (this one is oldest I haven't seen it used but could theoretically be there)
also not sure why but there are three different outbount ones with distinct IDs, two of them only have one entry, so I guess we just go with the long one/ the one whose ID matches the other IDs from video outbound stats *DECIDE*
-->
<!--inbound entries are like:
"[\"VP9 (98, profile-id=0)\-->
* width / height (pixels): Resolution of the video being received
<!-- stats frameWidth and frameHeight inbound IT01V
I don't see this being used in the code! so maybe we need to alter a part to include?! *EDIT THIS*-->
* expectedWidth / expectedHeight (pixels): Resolution of the rendering window that is the ideal resolution that we would like to receive to not have to scale the video.  If this parameter is not known the algorithm assumes that the width and height of the received frames matches the expected resolution of the rendering window.
<!--can use SV2-width and SV2-height
or alternatively the second entry in the .txt file is "origin": "https://meet.google.com", that includes an entry like:    
"video": "{width: {ideal: 1280}, height: {ideal: 720}, 
SV2-width and heigh are per second, I haven;t seen any where they change but theoretically they could-->
* frameRate (frames per second): Frames received per second.  They are used to estimate the quality of the video.   A video at 5 fps requires less bitrate than a video at 30 fps for the same quality.
<!-- use the stat "framesPerSecond"
Included for both inbound IT01V -->
* expectedFrameRate (frames per second): Frames per second that are expected to be receive.  This should usually be the frameRate of the source video (typically 30 fps).  If this parameter is not known the algorithm assumes that the frameRate received matches the expected framerate.
<!-- use the stat "SV2-framesPerSecond", of type "media-source" -->