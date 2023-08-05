# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/audio/mfcc_mel_calculators.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6mediapipe/calculators/audio/mfcc_mel_calculators.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xd5\x01\n\x1cMelSpectrumCalculatorOptions\x12\x19\n\rchannel_count\x18\x01 \x01(\x05:\x02\x32\x30\x12 \n\x13min_frequency_hertz\x18\x02 \x01(\x02:\x03\x31\x32\x35\x12!\n\x13max_frequency_hertz\x18\x03 \x01(\x02:\x04\x33\x38\x30\x30\x32U\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb4\xa0\xbc% \x01(\x0b\x32\'.mediapipe.MelSpectrumCalculatorOptions\"\xc5\x01\n\x15MfccCalculatorOptions\x12\x44\n\x13mel_spectrum_params\x18\x01 \x01(\x0b\x32\'.mediapipe.MelSpectrumCalculatorOptions\x12\x16\n\nmfcc_count\x18\x02 \x01(\r:\x02\x31\x33\x32N\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x89\x9e\xb4% \x01(\x0b\x32 .mediapipe.MfccCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.audio.mfcc_mel_calculators_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_MELSPECTRUMCALCULATOROPTIONS.extensions_by_name['ext'])
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_MFCCCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _MELSPECTRUMCALCULATOROPTIONS._serialized_start=108
  _MELSPECTRUMCALCULATOROPTIONS._serialized_end=321
  _MFCCCALCULATOROPTIONS._serialized_start=324
  _MFCCCALCULATOROPTIONS._serialized_end=521
# @@protoc_insertion_point(module_scope)
