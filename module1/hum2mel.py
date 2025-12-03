import librosa
import pretty_midi
import numpy as np
import scipy.signal
from sklearn.cluster import KMeans
import os

class Hum2Mel:
    def __init__(self, sr=22050):
        self.sr = sr

    def convert(self, wav_path, output_midi_path):
        print(f"Start Audio Analysis and ML Clustering: {wav_path}")
        
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"There is no file: {wav_path}")

        # 1. Feature Extraction (DSP: Signal Processing)
        # We extract the fundamental frequency (f0) from the audio waveform using the pYIN algorithm.
        y, sr = librosa.load(wav_path, sr=self.sr)
        
        # fmin=60 (C2), fmax=1000 (C6)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=60, fmax=1000, sr=sr)
        
        # Noise Removal (discard probabilities below 0.15 – a sensitive threshold)
        f0[voiced_probs < 0.15] = 0
        f0 = np.nan_to_num(f0)

        # Convert to MIDI note numbers
        midi_pitch = np.zeros_like(f0)
        non_zero_idx = f0 > 0
        
        if np.sum(non_zero_idx) == 0:
            print("Voice Detection Failed")
            return None

        # Extract only the pitches from voiced segments
        raw_midi = librosa.hz_to_midi(f0[non_zero_idx])

        # 2. Pitch Quantization (ML: Unsupervised Learning)
        # Pitch correction is performed based on the cluster centers of the data distribution using K-Means clustering.
        
        # Prepare training data (N, 1)
        X = raw_midi.reshape(-1, 1)
        
        # Automatically estimate the number of clusters (K, seminotes)
        pitch_range = raw_midi.max() - raw_midi.min()
        n_clusters = int(pitch_range) + 1
        n_clusters = max(3, min(n_clusters, 30))
        
        print(f"Training K-Means: (Estimated number of notes: {n_clusters})")
        
        # Model Training
        kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
        labels = kmeans.fit_predict(X)
        
        # Compute the centroid of each cluster and map it to the nearest integer pitch
        centers = kmeans.cluster_centers_.flatten()
        rounded_centers = np.round(centers)
        
        # Convert the predictions into refined integer pitches
        refined_midi = rounded_centers[labels]
        
        # Overwrite the original array with the ML predictions
        midi_pitch[non_zero_idx] = refined_midi

        # 3. Post-processing (Smoothing)
        # Smooth out abrupt jumps or jitter (kernel size 5)
        smooth_pitch = scipy.signal.medfilt(midi_pitch, kernel_size=5)

        # 4. MIDI Generation
        pm = pretty_midi.PrettyMIDI()
        inst = pretty_midi.Instrument(program=0) # Piano
        frame_time = 512 / sr
        
        current_note = None
        start_time = 0
        
        for i, pitch in enumerate(smooth_pitch):
            if pitch <= 0:
                if current_note is not None:
                    end_time = i * frame_time
                    # Do not record very short noise (less than 0.03 seconds)
                    if end_time - start_time > 0.03: 
                        inst.notes.append(pretty_midi.Note(100, int(current_note), start_time, end_time))
                    current_note = None
                continue
                
            if pitch != current_note:
                if current_note is not None:
                    end_time = i * frame_time
                    if end_time - start_time > 0.03:
                        inst.notes.append(pretty_midi.Note(100, int(current_note), start_time, end_time))
                current_note = pitch
                start_time = i * frame_time
                
        # Handle the Final Note
        if current_note is not None:
            end_time = len(smooth_pitch) * frame_time
            inst.notes.append(pretty_midi.Note(100, int(current_note), start_time, end_time))

        pm.instruments.append(inst)
        pm.write(output_midi_path)
        
        print(f"Convert Finish: {output_midi_path}")
        
        unique = np.unique([n for n in smooth_pitch if n > 0])
        print(f"Detected Pitches (K-Means results): {unique}")
        
        return output_midi_path

# Module Test
if __name__ == "__main__":
    # Test execution when running this file directly
    converter = Hum2Mel()
    input_file = "./MIR-QBSH/waveFile/year2003/person00001/00014.wav" 
    
    # Check if test file exists before running
    if os.path.exists(input_file):
        converter.convert(input_file, "test_output.mid")
    else:
        print("Test file not found. Please import this module to use.")