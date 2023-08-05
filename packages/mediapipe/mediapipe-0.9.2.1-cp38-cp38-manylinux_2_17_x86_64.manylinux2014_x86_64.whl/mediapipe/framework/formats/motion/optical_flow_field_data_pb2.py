# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/motion/optical_flow_field_data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/formats/motion/optical_flow_field_data.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n@mediapipe/framework/formats/motion/optical_flow_field_data.proto\x12\tmediapipe\"U\n\x14OpticalFlowFieldData\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\x0e\n\x02\x64x\x18\x03 \x03(\x02\x42\x02\x10\x01\x12\x0e\n\x02\x64y\x18\x04 \x03(\x02\x42\x02\x10\x01')
)




_OPTICALFLOWFIELDDATA = _descriptor.Descriptor(
  name='OpticalFlowFieldData',
  full_name='mediapipe.OpticalFlowFieldData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='mediapipe.OpticalFlowFieldData.width', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='mediapipe.OpticalFlowFieldData.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dx', full_name='mediapipe.OpticalFlowFieldData.dx', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\020\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dy', full_name='mediapipe.OpticalFlowFieldData.dy', index=3,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\020\001'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=164,
)

DESCRIPTOR.message_types_by_name['OpticalFlowFieldData'] = _OPTICALFLOWFIELDDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OpticalFlowFieldData = _reflection.GeneratedProtocolMessageType('OpticalFlowFieldData', (_message.Message,), dict(
  DESCRIPTOR = _OPTICALFLOWFIELDDATA,
  __module__ = 'mediapipe.framework.formats.motion.optical_flow_field_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.OpticalFlowFieldData)
  ))
_sym_db.RegisterMessage(OpticalFlowFieldData)


_OPTICALFLOWFIELDDATA.fields_by_name['dx']._options = None
_OPTICALFLOWFIELDDATA.fields_by_name['dy']._options = None
# @@protoc_insertion_point(module_scope)
