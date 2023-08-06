#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nicolvisser.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Int, Bool, Float
from ._frontend import module_name, module_version
from traittypes import Array
import torchaudio
import numpy as np

#TODO: Perform mel spectrogram calculation here and make sxx optional

class SpectrogramPlayer(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('SpectrogramPlayerModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('SpectrogramPlayerView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    wav_file_path = Unicode('blank').tag(sync=True)
    src = Unicode('blank').tag(sync=True)
    sxx = Array([[1.0,0.0],[0.0,1.0]]).tag(sync=True)
    width = Int(900).tag(sync=True)
    spec_height = Int(300).tag(sync=True)
    nav_height = Int(50).tag(sync=True)
    navigator = Bool(True).tag(sync=True)
    settings = Bool(True).tag(sync=True)
    colormap = Unicode('viridis').tag(sync=True)
    transparent = Bool(False).tag(sync=True)
    dark = Bool(False).tag(sync=True)
    n_fft=Int(2048).tag(sync=True)
    win_length=Int(400).tag(sync=True)
    hop_length=Int(160).tag(sync=True)
    f_min=Int(50).tag(sync=True)
    n_mels=Int(80).tag(sync=True)
    power=Float(1.0).tag(sync=True)
    top_db=Int(80).tag(sync=True)
    annotations=Array([[]]).tag(sync=True)
    annotations2=Array([[]]).tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calc_src()
        self.calc_sxx()

    def calc_src(self):
        import base64
        with open(self.wav_file_path, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode('ascii')
        src = f"data:audio/wav;base64,{b64}"
        self.src = src

    def calc_sxx(self):
        waveform, sample_rate = torchaudio.load(self.wav_file_path)
        transform_wav_to_mel_spec = torchaudio.transforms.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=self.n_fft,
            win_length=self.win_length,
            hop_length=self.hop_length,
            f_min=self.f_min,
            n_mels=self.n_mels,
            power=self.power
        )
        transform_amp_to_db = torchaudio.transforms.AmplitudeToDB(stype='magnitude', top_db=self.top_db)
        mel_spec = transform_amp_to_db(transform_wav_to_mel_spec(waveform)).squeeze().numpy()
        mel_spec = ((mel_spec-mel_spec.min())/(mel_spec.max() - mel_spec.min())*255).astype(np.uint8)
        self.sxx = mel_spec
