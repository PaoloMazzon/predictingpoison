Predicting Poison
=================
Code repository for the paper "Predicting Poisoned Images via Image Entropy." The images in this repository
are from the link below, they are all public domain as is this code and and related documents.

Usage
=====
All information relevant to the paper is stored in `processed_images.json`, running

    python entropy.py

will force a rebuild of `processed_images.json`. Otherwise, importing `entropy.py` and running
`get_image_profiles()` will return the Python dictionary containing the contents of `processed_images.json`,
making `processed_images.json` if it does not exist (building the json will take a long time, just use
the json in this repository if available).

References
==========
 + [Saturation Calculation](https://alienryderflex.com/hsp.html)
 + [Public Domain Images](https://www.pexels.com/public-domain-images/)