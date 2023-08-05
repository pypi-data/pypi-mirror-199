# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/warp_affine_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.gpu import gpu_origin_pb2 as mediapipe_dot_gpu_dot_gpu__origin__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/image/warp_affine_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\n8mediapipe/calculators/image/warp_affine_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/gpu/gpu_origin.proto\"\xd0\x03\n\x1bWarpAffineCalculatorOptions\x12\x46\n\x0b\x62order_mode\x18\x01 \x01(\x0e\x32\x31.mediapipe.WarpAffineCalculatorOptions.BorderMode\x12-\n\ngpu_origin\x18\x02 \x01(\x0e\x32\x19.mediapipe.GpuOrigin.Mode\x12K\n\rinterpolation\x18\x03 \x01(\x0e\x32\x34.mediapipe.WarpAffineCalculatorOptions.Interpolation\"K\n\nBorderMode\x12\x16\n\x12\x42ORDER_UNSPECIFIED\x10\x00\x12\x0f\n\x0b\x42ORDER_ZERO\x10\x01\x12\x14\n\x10\x42ORDER_REPLICATE\x10\x02\"I\n\rInterpolation\x12\x15\n\x11INTER_UNSPECIFIED\x10\x00\x12\x10\n\x0cINTER_LINEAR\x10\x01\x12\x0f\n\x0bINTER_CUBIC\x10\x02\x32U\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc7\xbb\x98\xb2\x01 \x01(\x0b\x32&.mediapipe.WarpAffineCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,mediapipe_dot_gpu_dot_gpu__origin__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_WARPAFFINECALCULATOROPTIONS_BORDERMODE = _descriptor.EnumDescriptor(
  name='BorderMode',
  full_name='mediapipe.WarpAffineCalculatorOptions.BorderMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BORDER_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BORDER_ZERO', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BORDER_REPLICATE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=369,
  serialized_end=444,
)
_sym_db.RegisterEnumDescriptor(_WARPAFFINECALCULATOROPTIONS_BORDERMODE)

_WARPAFFINECALCULATOROPTIONS_INTERPOLATION = _descriptor.EnumDescriptor(
  name='Interpolation',
  full_name='mediapipe.WarpAffineCalculatorOptions.Interpolation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INTER_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTER_LINEAR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTER_CUBIC', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=446,
  serialized_end=519,
)
_sym_db.RegisterEnumDescriptor(_WARPAFFINECALCULATOROPTIONS_INTERPOLATION)


_WARPAFFINECALCULATOROPTIONS = _descriptor.Descriptor(
  name='WarpAffineCalculatorOptions',
  full_name='mediapipe.WarpAffineCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='border_mode', full_name='mediapipe.WarpAffineCalculatorOptions.border_mode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gpu_origin', full_name='mediapipe.WarpAffineCalculatorOptions.gpu_origin', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interpolation', full_name='mediapipe.WarpAffineCalculatorOptions.interpolation', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.WarpAffineCalculatorOptions.ext', index=0,
      number=373693895, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
    _WARPAFFINECALCULATOROPTIONS_BORDERMODE,
    _WARPAFFINECALCULATOROPTIONS_INTERPOLATION,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=606,
)

_WARPAFFINECALCULATOROPTIONS.fields_by_name['border_mode'].enum_type = _WARPAFFINECALCULATOROPTIONS_BORDERMODE
_WARPAFFINECALCULATOROPTIONS.fields_by_name['gpu_origin'].enum_type = mediapipe_dot_gpu_dot_gpu__origin__pb2._GPUORIGIN_MODE
_WARPAFFINECALCULATOROPTIONS.fields_by_name['interpolation'].enum_type = _WARPAFFINECALCULATOROPTIONS_INTERPOLATION
_WARPAFFINECALCULATOROPTIONS_BORDERMODE.containing_type = _WARPAFFINECALCULATOROPTIONS
_WARPAFFINECALCULATOROPTIONS_INTERPOLATION.containing_type = _WARPAFFINECALCULATOROPTIONS
DESCRIPTOR.message_types_by_name['WarpAffineCalculatorOptions'] = _WARPAFFINECALCULATOROPTIONS

WarpAffineCalculatorOptions = _reflection.GeneratedProtocolMessageType('WarpAffineCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _WARPAFFINECALCULATOROPTIONS,
  __module__ = 'mediapipe.calculators.image.warp_affine_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.WarpAffineCalculatorOptions)
  ))
_sym_db.RegisterMessage(WarpAffineCalculatorOptions)

_WARPAFFINECALCULATOROPTIONS.extensions_by_name['ext'].message_type = _WARPAFFINECALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_WARPAFFINECALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
