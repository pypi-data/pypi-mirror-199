# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/core/concatenate_vector_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>mediapipe/calculators/core/concatenate_vector_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xaa\x01\n\"ConcatenateVectorCalculatorOptions\x12\'\n\x18only_emit_if_all_present\x18\x01 \x01(\x08:\x05\x66\x61lse2[\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xcf\xb1\xd8{ \x01(\x0b\x32-.mediapipe.ConcatenateVectorCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.core.concatenate_vector_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_CONCATENATEVECTORCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _CONCATENATEVECTORCALCULATOROPTIONS._serialized_start=116
  _CONCATENATEVECTORCALCULATOROPTIONS._serialized_end=286
# @@protoc_insertion_point(module_scope)
