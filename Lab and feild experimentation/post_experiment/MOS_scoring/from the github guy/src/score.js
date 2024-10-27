/* Stats object contains these params:
 *
 * packetLoss: 0-100%
 * bitrate: bps
 * roundTripTime: ms
 * bufferDelay: ms
 * codec: opus / vp8 / vp9 / h264 (only used for video) **EDIT THIS --> maybe add AV1 codec
 * fec: boolean (ony used for audio)
 * dtx: boolean (ony used for audio)
 * qp: number (not used yet)
 * keyFrames: number (not used yet)
 * width: number; Resolution of the video received
 * expectedWidth: number; Resolution of the rendering widget
 * height: number; Resolution of the video received
 * expectedHeight: number; Resolution of the rendering widget
 * frameRate: number; FrameRate of the video received
 * expectedFrameRate: number; FrameRate of the video source
 * The stats object is inputted into the following function to calc MOS score:
*/

function score(stats) {

	const scores = {}; //An object to store the MOS scores for audio and video

  	const { audio, video } = normalize(stats); //uses the norm func (below) to fill-in and normalise missing stats

  	if (audio) { //calculate audio score (Audio MOS calculation is based on E-Model algorithm)

		const R0 = 100; //R initially set to 100 as an initial score to decrease from i think?

		// Delay:
		const delay = 20 + audio.bufferDelay + audio.roundTripTime / 2;  // Assumes 20 packetization delay
		
		// Packet Loss:
		const pl = audio.packetLoss; 

		// Equiptment Impairment factor (Ie):
		const Ie = audio.dtx  // Ignore audio bitrate in dtx mode (DTX = Discontinuous Transmission mode)
		? 8                 // if dtx is on, Ie is set to 8
		: audio.bitrate     // elif a bitrate is provided in the audio stats, a log function (next line) is used to calc Ie
		? clamp(55 - 4.6 * Math.log(audio.bitrate), 0, 30) 
		: 6;                // else, defaults to 6

		// Packet-loss robustness Factor:
		const Bpl = audio.fec ? 20 : 10;  //20 if Forward Error Correction (FEC) is on, else 10

		// Impairment due to Packet Loss:
		const Ipl = Ie + (100 - Ie) * (pl / (pl + Bpl)); //calc based on Ie and packet loss

		// Delay Impairment: 
		const Id = delay * 0.03 + (delay > 150 ? 0.1 * (delay - 150) : 0); //Delays greater than 150ms are penalised more (exceeding human reaction time? Assuming 150ms min latency?)
		
		// Calculating R (rating):
		const R = clamp(R0 - Ipl - Id, 0, 100); // rating is calculated as 100 - impairments due to delay and packetloss. bounded between 0 and 100
		
		// Calculating MOS:
		const MOS = 1 + 0.035 * R + (R * (R - 60) * (100 - R) * 7) / 1000000; //non-linear mapping of R(range 0-100) onto MOS (range 1-5)--> these coefficients are the ones fitted through experiments?
		scores.audio = clamp(Math.round(MOS * 100) / 100, 1, 5); //round the MOS score to two decimal places, bound between 1 and 5
	}

  if (video) {  // Calculate video score 

    // Pixels:
    const pixels = video.expectedWidth * video.expectedHeight; //number of pixels as an area of h x w
    //*EDIT THIS* I think this might be supposed to be the actual rather than the expected

    // Increased quality from Codecs:
    const codecFactor = video.codec === 'vp9' ? 1.2 : 1.0; //*EDIT THIS * - add AV1 as a video codec option either more efficient than vp9 or same if we can't find anything
    
    // Delay:
    const delay = video.bufferDelay + video.roundTripTime / 2; //delay is calculated by buffer(internal delay) + one way latency(travel delay)
    
    // These parameters are generated with a logaritmic regression
    // on some very limited test data for now
    // They are based on the bits per pixel per frame (bPPPF)
    if (video.frameRate !== 0) {
      
      //bits per pixel per frame
      const bPPPF = (codecFactor * video.bitrate) / pixels / video.frameRate; 
      
      //base score- transform of bits per pixel per frame
      const base = clamp(0.56 * Math.log(bPPPF) + 5.36, 1, 5); 
      
      //MOS as a function of (base score) - (frame rate underperformance) - (delay)
      const MOS =
        base -
        1.9 * Math.log(video.expectedFrameRate / video.frameRate) -
        delay * 0.002;
      scores.video = clamp(Math.round(MOS * 100) / 100, 1, 5); //round MOS to 2dp in the range 1-5
    
    } else {
      scores.video = 1; //if frameRate == 0: score is set to 1 (lowest)
    }
  }
  return scores;
}

function normalize(stats) {
  return {
    
    audio: stats.audio //check if this exists
      ? {//if it exists, creates a new object defining default values for audio stats
          packetLoss: 0,
          bufferDelay: 50,
          roundTripTime: 50,
          fec: true,
          ...stats.audio, //merges these values with existing values, exisitng values take precedence
        }
      : undefined, //if it doesn't exist then the 'audio property' is set to undef
    
    video: stats.video
      ? { //define default values for video stats
          packetLoss: 0,
          bufferDelay: 0,
          roundTripTime: 50,
          fec: false,
          expectedHeight: stats.video.height || 640,
          expectedWidth: stats.video.width || 480,
          frameRate: stats.video.expectedFrameRate || 30,
          expectedFrameRate: stats.video.frameRate || 30,
          ...stats.video,
        }
      : undefined,
  
  };
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(value, max));
}

module.exports = { score };
