# insta-captions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![issues](https://img.shields.io/github/issues/DavidCendejas/insta-captions)

[![Build Status](https://github.com/DavidCendejas/insta-captions/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/DavidCendejas/insta-captions/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/DavidCendejas/insta-captions/branch/main/graph/badge.svg?token=Z2HN4RCJGZ)](https://codecov.io/gh/DavidCendejas/insta-captions)

insta-captions is a tool that will allow for the instant transcription and translation of audio files to and from different languages.

## Installation

"pip install insta-captions"

## Overview

`insta-captions` is a library that deals with the conversion of audio into "captions". I have been learning Mandarin, my third language. Part of my learning process, as well as maintenance for Spanish, is to watch videos, shows, and movies in the language I am trying to deepen. Sometimes, however, I need to watch content in English but want to read it in another language, and there is no easy way to do this if captions are not provided by the video maker, which is the crux of this issue.

The main feature that I envision for this project would be for audio to be converted into text of any (supported) language regardless of the language of the input audio. This involves two, albeit involved, steps:

- given an audio file, convert that audio into text of language it is in
- given text of one language, translate into another

## Installation and Running

insta-captions transcriptions are possible with [DeepSpeech](https://github.com/mozilla/DeepSpeech). For installation of DeepSpeech, refer to their [documentation](https://deepspeech.readthedocs.io/en/r0.9/?badge=latest). I use their [pre-trained models](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3) on english and mandarin. These models are included in this repository via Git LFS due to large file size.

Additional libraries used are numpy to convert the buffer of the .wav files into int16 numpy arrays as this is what DeepSpeech speech-to-text accepts.

## How to Use

To get a transcription of an audio file, we have the function *transcribe(wav_files, language)* .
- *wav_files* is a list of strings that contain the paths to the .wav files that you want the function to transcribe. These files must have a sample rate of 16kHz.
- *language* is a string indicating the language that the audio file is in. Currently the only supported languages are "english" and "mandarin".
- This returns a list of strings, one transcription for each file sent.

## make commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make format`: autoformat this library using `black`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make test`: run automated tests with `unittest`
- `make coverage`: run automated tests with `unittest` and collect coverage information