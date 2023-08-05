# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/image_to_tensor_calculator.proto
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
from mediapipe.gpu import gpu_origin_pb2 as mediapipe_dot_gpu_dot_gpu__origin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=mediapipe/calculators/tensor/image_to_tensor_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/gpu/gpu_origin.proto\"\xa0\x06\n\x1eImageToTensorCalculatorOptions\x12\x1b\n\x13output_tensor_width\x18\x01 \x01(\x05\x12\x1c\n\x14output_tensor_height\x18\x02 \x01(\x05\x12\x19\n\x11keep_aspect_ratio\x18\x03 \x01(\x08\x12Y\n\x19output_tensor_float_range\x18\x04 \x01(\x0b\x32\x34.mediapipe.ImageToTensorCalculatorOptions.FloatRangeH\x00\x12U\n\x17output_tensor_int_range\x18\x07 \x01(\x0b\x32\x32.mediapipe.ImageToTensorCalculatorOptions.IntRangeH\x00\x12W\n\x18output_tensor_uint_range\x18\x08 \x01(\x0b\x32\x33.mediapipe.ImageToTensorCalculatorOptions.UIntRangeH\x00\x12-\n\ngpu_origin\x18\x05 \x01(\x0e\x32\x19.mediapipe.GpuOrigin.Mode\x12I\n\x0b\x62order_mode\x18\x06 \x01(\x0e\x32\x34.mediapipe.ImageToTensorCalculatorOptions.BorderMode\x1a&\n\nFloatRange\x12\x0b\n\x03min\x18\x01 \x01(\x02\x12\x0b\n\x03max\x18\x02 \x01(\x02\x1a$\n\x08IntRange\x12\x0b\n\x03min\x18\x01 \x01(\x03\x12\x0b\n\x03max\x18\x02 \x01(\x03\x1a%\n\tUIntRange\x12\x0b\n\x03min\x18\x01 \x01(\x04\x12\x0b\n\x03max\x18\x02 \x01(\x04\"K\n\nBorderMode\x12\x16\n\x12\x42ORDER_UNSPECIFIED\x10\x00\x12\x0f\n\x0b\x42ORDER_ZERO\x10\x01\x12\x14\n\x10\x42ORDER_REPLICATE\x10\x02\x32X\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xd3\xea\xb7\x9f\x01 \x01(\x0b\x32).mediapipe.ImageToTensorCalculatorOptionsB\x07\n\x05range')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.image_to_tensor_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_IMAGETOTENSORCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _IMAGETOTENSORCALCULATOROPTIONS._serialized_start=147
  _IMAGETOTENSORCALCULATOROPTIONS._serialized_end=947
  _IMAGETOTENSORCALCULATOROPTIONS_FLOATRANGE._serialized_start=656
  _IMAGETOTENSORCALCULATOROPTIONS_FLOATRANGE._serialized_end=694
  _IMAGETOTENSORCALCULATOROPTIONS_INTRANGE._serialized_start=696
  _IMAGETOTENSORCALCULATOROPTIONS_INTRANGE._serialized_end=732
  _IMAGETOTENSORCALCULATOROPTIONS_UINTRANGE._serialized_start=734
  _IMAGETOTENSORCALCULATOROPTIONS_UINTRANGE._serialized_end=771
  _IMAGETOTENSORCALCULATOROPTIONS_BORDERMODE._serialized_start=773
  _IMAGETOTENSORCALCULATOROPTIONS_BORDERMODE._serialized_end=848
# @@protoc_insertion_point(module_scope)
