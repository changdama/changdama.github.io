#!/usr/bin/env python
# coding: utf-8

# ## Load Test and Validation video in the folders

import os
import numpy as np
import pandas as pd
import librosa
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
import matplotlib.pyplot as plt

test_folder = 'micro_medlydb/test/'
val_folder = 'micro_medlydb/validate/'
test_audio = [librosa.load((test_folder + file), mono=True, sr=22050)[0] for file in os.listdir(test_folder)]
val_audio = [librosa.load((val_folder + file), mono=True, sr=22050)[0] for file in os.listdir(val_folder)]

# ## Compute mean spectral flux and  mean MFCCs of all frames in all files
# ```
# psy code:Create compute features(audio_list):
#             set flux and mfcc features
#             for each audio signal in audio list:
#                compute flux across time frames
#                store
#                compute mfcc
#                store
#             concatenate all flux sequeces across all pieces
#             calculate mean and sd
#             concatenate all mfcc matrices 
#             calculate sd and mfcc coefficient
#             return all flux means, all flux sd, all mfcc means and mfcc sd
# ````
# 
sr = 22050
frame_size = 1024
hop = 512

def compute_all_frames(audio_list):
    all_flux=[]
    all_mfcc=[]

    for y in audio_list:
        prev_spec = None
        flux_seq = []
        window = np.hanning(frame_size)
        for start in range(0, len(y)-frame_size, hop):
            frame = y[start:start+frame_size] * window
            spectrum = np.abs(np.fft.rfft(frame))
            spec_n = spectrum / (np.linalg.norm(spectrum) + 1e-12)
            if prev_spec is not None:
                flux_seq.append(np.linalg.norm(spec_n - prev_spec))
            prev_spec = spec_n
        if flux_seq:
            all_flux.append(np.array(flux_seq))
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=10, hop_length=hop)
        if mfcc.size:
            all_mfcc.append(mfcc)

    all_flux=np.concatenate(all_flux,axis=0)
    all_flux_mean=np.mean(all_flux)
    all_flux_std=np.std(all_flux) + 1e-12

    all_mfcc=np.concatenate(all_mfcc, axis=1)
    all_mfcc_mean=np.mean(all_mfcc, axis=1)
    all_mfcc_std = np.std(all_mfcc, axis=1) + 1e-12
    return all_flux_mean, all_flux_std, all_mfcc_mean, all_mfcc_std


all_flux_mean, all_flux_std, all_mfcc_mean, all_mfcc_std=compute_all_frames(val_audio)


# ## Extract Text and Validation Audio Features
# ```
# psy code: Create get feature function:
#               initialize centroids, rolloffs, spreads, flatness, and fluxes
#         for each frame in audio
#              apply window
#              calculate spectrum and bins
#              calculate centroid, rolloff, spread, and flatness
#              if prev_spec exists:
#             compute flux as distance between current spectrum and previous spectrum
#             else:
#                flux = 0
#                store flux
#                update prev_spec
#                store centroid, rolloff, spread, flatness
#         compute zero crossing rate (zcr) over audio
#         compute MFCCs (10 coefficients)
#         normalize flux sequence using all_flux_mean, and all_flux_std
#         normalize MFCCs using all_mfcc_mean, and all_mfcc_std
#         aggregate by mean:
#                centroid_mean, rolloff_mean, spread_mean, flatness_mean
#                zcr_mean, flux_mean
#                 mfcc_1_mean ... mfcc_10_mean
# 
#     return dictionary of aggregated features
# ```
#              
def get_features(audio, aggregate=True, sr=22050, frame_size=1024, hop=512):
    window = np.hanning(frame_size)
    frame = audio[0:frame_size] * window

    centroids = []
    rolloffs = []
    spreads = []
    flatnesses = []
    fluxes = []
    prev_spec = None

    for start in range(0, len(audio) - frame_size, hop):
        frame = audio[start:start+frame_size] * window
        spectrum = np.abs(np.fft.rfft(frame))
        freqs = np.fft.rfftfreq(frame_size, 1/sr)

        #centroid
        c = np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-12)
        #rolloff
        r_thresh = 0.85 * np.sum(spectrum)
        r_idx = np.searchsorted(np.cumsum(spectrum), r_thresh)
        r = freqs[min(r_idx, len(freqs) - 1)]
        #spread
        s = np.sqrt(np.sum(((freqs - c)**2) * spectrum) / (np.sum(spectrum) + 1e-12))
        #flatness
        f = np.exp(np.mean(np.log(spectrum + 1e-12))) / (np.mean(spectrum) + 1e-12)

        #flux
        if prev_spec is None:
            fluxes.append(0.0)
        else:
            mag_n = spectrum / (np.linalg.norm(spectrum) + 1e-12)
            prev_n = prev_spec / (np.linalg.norm(prev_spec) + 1e-12)
            fluxes.append(np.linalg.norm(mag_n - prev_n))
        prev_spec = spectrum

        centroids.append(c)
        rolloffs.append(r)
        spreads.append(s)
        flatnesses.append(f)
    #zcr
    zcrs = librosa.feature.zero_crossing_rate(y=audio, frame_length=frame_size, hop_length=hop, center=False)[0]

    #mfcc
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=10, hop_length=hop)
    fluxes = np.array(fluxes, dtype=float)
    flux_n=(fluxes-all_flux_mean)/(all_flux_std+1e-12)
    mfcc_n= (mfcc - all_mfcc_mean[:, None]) / (all_mfcc_std[:, None] + 1e-12)

    features = {
     "centroid_mean": np.mean(centroids),
     "rolloff_mean": np.mean(rolloffs),
     "spread_mean": np.mean(spreads),
     "flatness_mean": np.mean(flatnesses),
     "zcr_mean": np.mean(zcrs[:len(centroids)]),
     "flux_mean": np.mean(flux_n),
    }
    mfcc_means = mfcc_n.mean(axis=1)
    for i in range(10):
        features[f"mfcc_{i+1}_mean"] = mfcc_means[i]

    return features


# ## Aggregate All Features in Dateaframe

label = {3: "flute", 4: "piano", 6: "trumpet", 7: "violin"}

val_features=[]
for fname, clip in zip(os.listdir(val_folder), val_audio):
    dic = get_features(clip, sr=22050)   
    dic["track"] = fname                 
    dic["label_id"] = int(fname.split("-")[3].split("_")[0])       
    dic["label_name"] = label[dic["label_id"]]     
    val_features.append(dic)
val_df = pd.DataFrame(val_features)

test_features=[]
for fname, clip in zip(os.listdir(test_folder), test_audio):
    dic = get_features(clip, sr=22050)   
    dic["track"] = fname                 
    dic["label_id"] = int(fname.split("-")[3].split("_")[0])      
    dic["label_name"] = label[dic["label_id"]]     
    test_features.append(dic)
test_df = pd.DataFrame(test_features)

# ##  Across-feature normalization

norm_val_df= val_df.copy()
norm_test_df = test_df.copy()
feature_cols = [c for c in val_df.columns if c not in ["track", "label_id", "label_name"]]

mu = val_df[feature_cols].mean()
sd = val_df[feature_cols].std() + 1e-12   

norm_val_df[feature_cols]  = (val_df[feature_cols]  - mu) / sd
norm_test_df[feature_cols] = (test_df[feature_cols] - mu) / sd
print(norm_val_df)
print(norm_test_df)
norm_val_df.to_csv("norm_val_df.csv", index=False)
norm_test_df.to_csv("norm_test_df.csv", index=False)


# ## Correlation Matrix , Highly and Weekly Correlation Features

features_df = norm_val_df.drop(columns=["track", "label_id", "label_name"])

correlation = features_df.corr()
correlation_matrix = features_df.corr(method="pearson")
print(correlation_matrix)
correlation_matrix.to_csv("correlation_matrix.csv", index=True)

correlation_values = correlation.abs().unstack()   
correlation_values = correlation_values[correlation_values< 0.9999]  
max_p = correlation_values.idxmax()
min_p = correlation_values.idxmin()


plt.figure(figsize=(10,4))

plt.figure(figsize=(12,10))
sns.heatmap(correlation_matrix , cmap="RdBu", center=0, annot=True)
plt.title("Feature Correlation Matrix")
plt.show()


plt.subplot(1,2,1)
plt.scatter(features_df[max_p[0]], features_df[max_p[1]], alpha=0.6)
plt.xlabel(max_p[0])
plt.ylabel(max_p[1])
plt.title(f"High correlation ({correlation[max_p[0]][max_p[1]]:.2f})")


plt.subplot(1,2,2)
plt.scatter(features_df[min_p[0]], features_df[min_p[1]], alpha=0.6)
plt.xlabel(min_p[0])
plt.ylabel(min_p[1])
plt.title(f"Low correlation ({correlation[min_p[0]][min_p[1]]:.2f})")

plt.tight_layout()
plt.show()

# ## Classification

x_val =norm_val_df.drop(columns=["track", "label_id", "label_name"])
y_val = norm_val_df["label_id"].values

x_test = norm_test_df.drop(columns=["track", "label_id", "label_name"])
y_test = norm_test_df["label_id"].values

for k in [3,5,7,9,11,13,15]:
    knn = KNeighborsClassifier(n_neighbors=k, metric="euclidean")
    knn.fit(x_val, y_val)
    print(f"k={k}  (val accuracy = {knn.score(x_val, y_val):.3f})")

y_pred = knn.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy:", accuracy)

c_matrix=confusion_matrix(y_test, y_pred, labels=[3,4,6,7])
disply = ConfusionMatrixDisplay(confusion_matrix=c_matrix, display_labels=["flute","piano","trumpet","violin"])

disply.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix (kNN)")
plt.show()





