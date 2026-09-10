import numpy as np
import librosa
import warnings
import matplotlib.pyplot as plt
from scipy.io import wavfile
from collections import deque
from scipy.spatial.distance import cdist
from scipy.signal import convolve2d, find_peaks


# ======================================================================
# SSM SCORING AND NOVELTY FUNCTIONS
# ======================================================================

def build_ssm_continuous(beat_features: np.ndarray, metric: str):
    """
    Computes pairwise similarity between beats before binarization
    allowing different distance metrics and adaptive thresholding later.
    """
    X = np.asarray(beat_features.T, dtype=np.float32, order="C")
    # correlation
    if metric == "correlation":
        Xc = X - X.mean(axis=1, keepdims=True)
        denom = np.linalg.norm(Xc, axis=1, keepdims=True) + 1e-8
        Xc = Xc / denom
        S = np.clip(Xc @ Xc.T, -1.0, 1.0)
        S = (S + 1.0) / 2.0
    else:
        D = cdist(X, X, metric=metric).astype(np.float32)
        S = 1.0 - D / (D.max() + 1e-8)
        S = np.clip(S, 0.0, 1.0)
    np.fill_diagonal(S, 0.0)
    return S


def binarize_ssm(S: np.ndarray, threshold: float):
    '''
    Convert a continuous SSM by Binarizing.
    '''
    B = (S > float(threshold))
    np.fill_diagonal(B, 0)
    return B
# -----------------------------
# Foote novelty calculation(Jonathan Foote (2000) Automatic Audio Segmentation Using a Measure of Audio Novelty)
# -----------------------------
def compute_foote_novelty(S: np.ndarray, L: int = 32):
    """
    Compute the Foote novelty curve and detect peaks
    """
    S = np.asarray(S, float)
    g = np.ones((L, L)); h = -np.ones((L, L))
    K = np.block([[g, h], [h, g]])
    C = convolve2d(S, K, mode='same', boundary='symm')
    novelty = np.clip(np.diag(C), 0, None)
    thr = 0.5 * np.median(novelty)
    pk, _ = find_peaks(novelty, distance=8, height=thr)
    return novelty, pk


def novelty_score_continuous(novelty: np.ndarray, pk: np.ndarray, min_dist: int = 8) -> float:
    """
    Compute a  novelty score  that bases:
    - Peak strength:energy of peaks
    - temporal dispersion of peaks
    """
    heights = novelty[pk]
    strength = float(np.sum(heights)) / (np.sum(novelty) + 1e-8)
    strength = float(np.clip(strength, 0.0, 1.0))
    bins_total = max(1, int(np.ceil(len(novelty) / min_dist)))
    bins_cov = len(np.unique(pk // min_dist))
    coverage = float(bins_cov) / bins_total
    coverage = float(np.clip(coverage, 0.0, 1.0))
    return 0.5 * strength + 0.5 * coverage


def score_ssm(S: np.ndarray, B: np.ndarray):
    """
        Based on:
        - strong off diagonal bands(from:https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S2_SSM.html#:~:text=If%20the%20feature%20sequence%20contains,correspond%20to%20path%2Dlike%20structures.),
        - reasonable sparsity (from:Self-Similarity-Based and Novelty-based loss for music structure analysis, Audio-based music structure analysis),
        - Jonathan Foote (2000) Automatic Audio Segmentation Using a Measure of Audio Novelty
        - Paulus et al. (2010) Audio-based music structure analysis
        Calculate:
              1)  diagonal contrast:structural repetition clarity
              2) Sparsity:avoid degenerate density
              3) Foote-style novelty peaks :segmentation readiness

    """
    S = np.asarray(S, float)
    B = (B > 0).astype(int)
    n = S.shape[0]

    # the mean value with the kth diagonal of matrix S. Citation：https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S2_SSM.html#:~:text=If%20the%20feature%20sequence%20contains,correspond%20to%20path%2Dlike%20structures.
  # 1) Near vs. far diagonal contrast
    def diag_mean(k):
        d = np.diag(S, k=k)
        return d.mean() if d.size else 0.0
    #Near diagonals, which shows detail repetition
    near = np.mean([diag_mean(k) for k in (-3, -2, -1, 1, 2, 3)])
    #Far diagonals, showing global difference
    far  = np.mean([diag_mean(k) for k in (-40, -20, 20, 40) if abs(k) < n])
    # contrast, if contrast are bigger, have more novelty
    contrast = max(near - far, 0.0)

    # 2) Sparsity moderation,which prevent all-bright or all-dark SSMs
    density = float(B.mean())
    if density <= 0 or density >= 0.8:
        dens_score = 0.0
    else:
        dens_score = 1.0 - abs(density - 0.10) / 0.10  # peak at 0.10

    # 3) Footenovelty peaks ((segmentation readiness)) Jonathan Foote (2000) Automatic Audio Segmentation Using a Measure of Audio Novelty
    ## checkerboard kernel size
    L = 32
    novelty, pk = compute_foote_novelty(S, L=L)
    seg_score = novelty_score_continuous(novelty, pk, min_dist=8)

    # Weighted combination ()
    score = (
        0.3 * contrast +
        0.2 * dens_score +
        0.5 * seg_score
    )

    # Penalize degenerate SSMs (flat, too dense, or too sparse)
    if np.std(S) < 0.02 or density > 0.9 or density < 0.001:
        score -= 1.5

    return float(score)


def _load_and_preprocess(audio_path: str):
    """Loads, converts to mono, and normalizes the audio file."""
    try:
        audio_data, sample_rate = librosa.load(audio_path, sr=None, mono=True)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        raise
    # Normalize audio
    if np.max(np.abs(audio_data)) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data))
    return audio_data, sample_rate


def _extract_features(audio_data: np.ndarray, sample_rate: int, feature_set: str, aggregation: str):
    """Extracts beats and beat-synchronized features from the audio."""
    # 1. Beat Tracking
    onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sample_rate, tightness=100)

    # Ensure beats start from frame 0 for complete coverage
    if beats[0] != 0:
        beats = np.insert(beats, 0, 0)

    # 2. Feature Extraction
    if feature_set == 'mfcc':
        features = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    elif feature_set == 'chroma':
        features = librosa.feature.chroma_cqt(y=audio_data, sr=sample_rate)
    elif feature_set == 'spectral':
        features = librosa.feature.spectral_contrast(y=audio_data, sr=sample_rate)
    elif feature_set == 'cqt':
        features = np.abs(librosa.cqt(y=audio_data, sr=sample_rate))
    else:
        raise ValueError(f"Unknown feature_set: '{feature_set}'.")

    # 3. Beat-Synchronize the features using librosa's utility
    beat_synced_C = np.zeros((features.shape[0], len(beats) - 1))
    for i in range(len(beats) - 1):
        start_frame = beats[i]
        end_frame = beats[i + 1]

        if aggregation == 'mean':
            beat_synced_C[:, i] = np.mean(features[:, start_frame:end_frame], axis=1)
        elif aggregation == 'median':
            beat_synced_C[:, i] = np.median(features[:, start_frame:end_frame], axis=1)
        else:
            raise ValueError(f"Unknown aggregation: '{aggregation}'.")

    return beats, beat_synced_C


# Function to compare automatic to manual similarity matrix
# def _build_similarity_matrix(beat_features: np.ndarray, metric: str):
#     """Builds a binarized self-similarity matrix from beat-level features."""
#     # 1. Compute the distance or correlation matrix
#     if metric == 'correlation':
#         # Correlation is a similarity measure from -1 to 1. We scale it to 0-1.
#         corr_matrix = np.corrcoef(beat_features.T)
#         similarity_matrix = (corr_matrix + 1) / 2
#     else:
#         distance_matrix = cdist(beat_features.T, beat_features.T, metric=metric) # cdist(beat_synced_C.T, beat_synced_C.T, metric='cosine')
#         similarity_matrix = 1 - (distance_matrix / np.max(distance_matrix)) # similarity_matrix = 1 - (distance_matrix/max_D)
#
#     # 2. Binarize (map each value to 0 or 1 based on a given threshold) the matrix to get clear jump points
#     threshold = 0.85
#     similarity_matrix = np.where(similarity_matrix > threshold, 1, 0)
#
#     return similarity_matrix


def _build_similarity_matrix(beat_features: np.ndarray, metric: str):
    """
    Builds a binarized self-similarity matrix from beat-level features by manually calculating the similarity.
    """

    # Transpose features so that each row is a beat's feature vector
    # Shape becomes (num_beats, num_features)
    features_T = beat_features.T
    num_beats = features_T.shape[0]

    # Initialize an empty matrix
    similarity_matrix = np.zeros((num_beats, num_beats))

    # Compute the distance or correlation matrix
    if metric == 'correlation':
        # 1. Correlation Calculation
        # We could either derive from np.corrcoeff (Pearson) or use Cosine similarity; They are mathematically related as discussed in class and in the below source.
        # "Cosine similarity is a dot product of unit vectors. Pearson correlation is cosine similarity between centered vectors."
        # Source: https://stats.stackexchange.com/questions/235673/is-there-any-relationship-among-cosine-similarity-pearson-correlation-and-z-sc
        for i in range(num_beats):
            for j in range(num_beats):
                vec_i = features_T[i]
                vec_j = features_T[j]

                # Mean-center the vectors
                centered_i = vec_i - np.mean(vec_i)
                centered_j = vec_j - np.mean(vec_j)

                # Calculate cosine similarity of centered vectors
                dot_product = np.dot(centered_i, centered_j)
                norm_i = np.linalg.norm(centered_i)
                norm_j = np.linalg.norm(centered_j)

                # Avoid division by zero
                if norm_i == 0 or norm_j == 0:
                    corr = 0.0
                else: # Calculate correlation, as in the slides (similarity.pptx)
                    corr = dot_product / (norm_i * norm_j)

                similarity_matrix[i, j] = corr

        # Correlation is a similarity measure from -1 to 1. Scaling it to 0-1 so the same threshold can be applied for both metric categories
        similarity_matrix = (similarity_matrix + 1) / 2

    else: # Distance based metrics, using Noel's code as reference
        distance_matrix = cdist(beat_features.T, beat_features.T, metric=metric)  # cdist(beat_synced_C.T, beat_synced_C.T, metric='cosine')
        similarity_matrix = 1 - (distance_matrix / np.max(distance_matrix)) # similarity_matrix = 1 - (distance_matrix/max_D)

    # Binarize the matrix using a threshold
    threshold = 0.85
    similarity_matrix = np.where(similarity_matrix > threshold, 1, 0)

    return similarity_matrix


def _generate_traversal_path(
        similarity_matrix: np.ndarray,
        beats: np.ndarray,
        sample_rate: int,
        duration_sec: float,
        base_jump_probability: float,
        novelty_curve: np.ndarray | None
):
    """
    Generates a beat sequence using with dynamic jump probability.
    """
    num_beats = similarity_matrix.shape[0]
    beat_times = librosa.frames_to_time(beats, sr=sample_rate)

    # --- 1. Create dynamic jump probabilities from the novelty curve ---
    if novelty_curve is not None and len(novelty_curve) > 0:
        # Get novelty value at the start of each beat
        beat_frame_indices = beats[:num_beats]
        beat_frame_indices = np.clip(beat_frame_indices, 0, len(novelty_curve) - 1)
        beat_novelty = novelty_curve[beat_frame_indices]

        # Normalize novelty to [0, 1]
        max_novelty = np.max(beat_novelty)
        normalized_novelty = beat_novelty / max_novelty if max_novelty > 0 else np.zeros_like(beat_novelty)

        # higher novelty means a higher chance of jumping
        max_jump_probability = 0.50
        dynamic_probs = base_jump_probability + (max_jump_probability - base_jump_probability) * normalized_novelty
    else:
        # Fallback to a fixed probability if no novelty curve is provided
        dynamic_probs = np.full(num_beats, base_jump_probability)

    # --- 2. Generate path with stateful traversal logic ---
    path = []
    current_beat = 0
    current_duration = 0.0

    # Don't allow jumps to the exact same beat
    np.fill_diagonal(similarity_matrix, 0)

    while current_duration < duration_sec:
        path.append(current_beat)

        # Add duration of the current beat segment to the total
        if current_beat + 1 < len(beat_times):
            current_duration += beat_times[current_beat + 1] - beat_times[current_beat]

        # Decide whether to jump based on the dynamic probability
        if np.random.random() < dynamic_probs[current_beat]:
            similar_positions = np.where(similarity_matrix[current_beat, :] == 1)[0]
            if len(similar_positions) > 0:
                # Jump to a random similar beat and continue from there
                current_beat = np.random.choice(similar_positions)
                continue  # Skip the sequential increment below

        # If no jump occurred, proceed to the next beat in sequence
        current_beat += 1
        if current_beat >= num_beats:  # Wrap around if the song ends
            current_beat = 0

    return path


def _render_audio(audio_data: np.ndarray, sample_rate: int, beats: np.ndarray, path: list):
    """Slices and concatenates audio segments according to the generated path."""
    beat_samples = librosa.frames_to_samples(beats)
    remix_segments = []

    for beat_index in path:
        if beat_index + 1 < len(beat_samples):
            start_sample = beat_samples[beat_index]
            end_sample = beat_samples[beat_index + 1]
            remix_segments.append(audio_data[start_sample:end_sample])

    if not remix_segments:
        return np.array([])

    remix_audio = np.concatenate(remix_segments)
    return remix_audio


# ==============================================================================
# VANILLA GENERATOR FUNCTION
# ==============================================================================

def generate_infinite_jukebox(
        audio_path: str,
        duration_sec: float,
        jump_probability: float,
        feature_set: str = "cqt",
        aggregation: str = "median",
        similarity_metric: str = "cosine",
        output_path: str | None = None,
        novelty_curve: np.ndarray | None = None,
) -> np.ndarray:
    """
    Generate an 'infinite jukebox' remix of the given song.

    Parameters
    ----------
    audio_path : str
        Path to the input audio file.
    duration_sec : float
        Desired remix duration in seconds.
    jump_probability : float
        Base probability of jumping to a non-sequential beat.
    feature_set : str, optional
        Feature type to use (e.g., 'mfcc', 'chroma', 'spectral', 'cqt').
    aggregation : str, optional
        Aggregation method for beat-level features ('mean', 'median', etc.).
    similarity_metric : str, optional
        Distance or similarity measure ('cosine', 'euclidean', 'correlation').
    output_path : str, optional
        If provided, saves the remixed audio to this path.

    Returns
    -------
    np.ndarray
        The remixed audio signal as a 1D NumPy array.
    """
    print(f"--- Starting Jukebox for '{audio_path}' ---")

    # 1. Load Audio
    audio_data, sample_rate = _load_and_preprocess(audio_path)
    print("Step 1: Audio loaded.")

    # 2. Extract Features
    beats, beat_features = _extract_features(audio_data, sample_rate, feature_set, aggregation)
    print(f"Step 2: Features extracted using '{feature_set}' and '{aggregation}'.")

    # 3. Build Similarity Matrix
    similarity_matrix = _build_similarity_matrix(beat_features, similarity_metric)
    print(f"Step 3: Similarity matrix built with '{similarity_metric}' metric.")

    # 4. Generate Traversal Path
    path = _generate_traversal_path(similarity_matrix, beats, sample_rate, duration_sec, jump_probability, novelty_curve)
    print("Step 4: Traversal path generated.")

    # 5. Render Audio
    remix_audio = _render_audio(audio_data, sample_rate, beats, path)
    print("Step 5: Remix audio rendered.")

    # 6. Save output if path is provided
    if output_path and remix_audio.size > 0:
        # Normalize and convert to 16-bit integer for WAV file
        if np.max(np.abs(remix_audio)) > 0:
            remix_audio = remix_audio / np.max(np.abs(remix_audio)) * 0.9
        wav_data = (remix_audio * 32767).astype(np.int16)
        wavfile.write(output_path, sample_rate, wav_data)
        print(f"--- Remix saved to '{output_path}' ---")

    return remix_audio

# -----------------------------
# AUTO-PARAMETER GENERATOR FUNCTION
# -----------------------------
def auto_infinite_jukebox(
    audio_path: str,
    duration_sec: float = 60.0,
    jump_probability: float = 0.35,
    *,
    feature_sets = ("chroma", "cqt", "mfcc", "spectral"),
    aggregations = ("mean", "median"),
    metrics      = ("cosine", "correlation", "euclidean"),
    thresholds   = (0.75,0.80, 0.85),
    topk_print: int = 5,
    output_path: str | None = "auto_remix.wav",
    return_debug: bool = False,
):
    """
    Grid-search all parameter combinations (feature, aggregation, metric, threshold)
    score each SSM , pick the best.
    """
    y, sr = _load_and_preprocess(audio_path)

    results = []
    print("--- Starting grid search for optimal parameters ---")
    for feat in feature_sets:
        for agg in aggregations:
            beats, beat_feats = _extract_features(y, sr, feat, agg)
            for metric in metrics:
                S = build_ssm_continuous(beat_feats, metric)
                for thr in thresholds:
                    B = binarize_ssm(S, thr)
                    s = score_ssm(S, B)
                    results.append((s, feat, agg, metric, thr, beats, S, B))

    results.sort(key=lambda x: -x[0])
    score, feat, agg, metric, thr, beats, S_best, B_best = results[0]

    print("\n--- Top Parameter Candidates ---")
    for s, f, a, m, t, bts, _, _ in results[:max(1, topk_print)]:
        print(f"  score={s:.3f} | feat={f:<8} agg={a:<6} metric={m:<11} thr={t:<4}")
    print(f"\n--- Selected Best Parameters ---")
    print(f"  Feature: {feat}, Aggregation: {agg}, Metric: {metric}, Threshold: {thr} (Score: {score:.3f})\n")

    # --- Generate the novelty curve from the best SSM ---
    novelty_curve, boundaries = compute_foote_novelty(S_best)

    # --- Call the main generator function ---
    # This delegates all the core logic
    remix_audio = generate_infinite_jukebox(
        audio_path=audio_path,
        duration_sec=duration_sec,
        jump_probability=jump_probability,  # The base probability
        feature_set=feat,
        aggregation=agg,
        similarity_metric=metric,
        output_path=output_path,
        novelty_curve=novelty_curve
    )

    if return_debug:
        return {"S": S_best, "B": B_best, "beats": beats, "feature_set": feat,
                "aggregation": agg, "metric": metric, "threshold": thr, "score": score,
                "novelty": novelty_curve, "boundaries": boundaries}

    return remix_audio


# ======================================================================
# EXECUTION AND PLOTTING
# ======================================================================
if __name__ == '__main__':
    SONG_FILE = "HappierThanEver.mp3"
    SONG_NAME = SONG_FILE.split(".")[0]

    dbg = auto_infinite_jukebox(
        audio_path=SONG_FILE,
        duration_sec=180,
        jump_probability=0.20,  # Low base probability, letting novelty drive jumps
        output_path=SONG_NAME + "_remix.wav",
        return_debug=True,
    )

    # Example of running the script without auto-picking parameters
    # This allows testing specific SSM's and how it affects the audio output
    # generate_infinite_jukebox(
    #     audio_path=SONG_FILE,
    #     duration_sec=180,
    #     jump_probability=0.2,
    #     output_path=SONG_NAME + "_vanillaremix.wav"
    # )

    # Visualization
    if dbg:
        # 1. Continuous SSM
        plt.figure(figsize=(6, 5))
        plt.imshow(dbg["S"], origin="lower", aspect="auto", cmap="magma")
        plt.title(f"Best Continuous SSM ({dbg['feature_set']}, {dbg['metric']})")
        plt.xlabel("Beats")
        plt.ylabel("Beats")
        plt.colorbar(label="Similarity")
        plt.tight_layout()
        plt.show()

        # 2. Novelty Curve and Detected Boundaries
        nov, pk = dbg["novelty"], dbg["boundaries"]
        plt.figure(figsize=(8, 3))
        plt.plot(nov, color="royalblue", label="Novelty Curve")
        plt.vlines(pk, 0, nov.max(), color="crimson", alpha=0.7, linestyle="--", label="Detected Boundaries")
        plt.title("Foote Novelty Curve (Structural Boundaries)")
        plt.xlabel("Beat Index")
        plt.ylabel("Novelty Strength")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()