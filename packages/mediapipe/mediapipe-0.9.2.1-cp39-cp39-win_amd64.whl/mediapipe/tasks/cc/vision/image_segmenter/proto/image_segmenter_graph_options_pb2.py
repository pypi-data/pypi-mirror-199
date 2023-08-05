# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_segmenter/proto/image_segmenter_graph_options.proto

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
from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2
from mediapipe.tasks.cc.vision.image_segmenter.proto import segmenter_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__segmenter_dot_proto_dot_segmenter__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/vision/image_segmenter/proto/image_segmenter_graph_options.proto',
  package='mediapipe.tasks.vision.image_segmenter.proto',
  syntax='proto2',
  serialized_pb=_b('\nSmediapipe/tasks/cc/vision/image_segmenter/proto/image_segmenter_graph_options.proto\x12,mediapipe.tasks.vision.image_segmenter.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\x1aGmediapipe/tasks/cc/vision/image_segmenter/proto/segmenter_options.proto\"\xd1\x02\n\x1aImageSegmenterGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12 \n\x14\x64isplay_names_locale\x18\x02 \x01(\t:\x02\x65n\x12Y\n\x11segmenter_options\x18\x03 \x01(\x0b\x32>.mediapipe.tasks.vision.image_segmenter.proto.SegmenterOptions2w\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x9e\xc7\xb8\xda\x01 \x01(\x0b\x32H.mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptionsBY\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\x1fImageSegmenterGraphOptionsProto')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,mediapipe_dot_framework_dot_calculator__options__pb2.DESCRIPTOR,mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2.DESCRIPTOR,mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__segmenter_dot_proto_dot_segmenter__options__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_IMAGESEGMENTERGRAPHOPTIONS = _descriptor.Descriptor(
  name='ImageSegmenterGraphOptions',
  full_name='mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_options', full_name='mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions.base_options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='display_names_locale', full_name='mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions.display_names_locale', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("en").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='segmenter_options', full_name='mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions.segmenter_options', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions.ext', index=0,
      number=458105758, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=341,
  serialized_end=678,
)

_IMAGESEGMENTERGRAPHOPTIONS.fields_by_name['base_options'].message_type = mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2._BASEOPTIONS
_IMAGESEGMENTERGRAPHOPTIONS.fields_by_name['segmenter_options'].message_type = mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__segmenter_dot_proto_dot_segmenter__options__pb2._SEGMENTEROPTIONS
DESCRIPTOR.message_types_by_name['ImageSegmenterGraphOptions'] = _IMAGESEGMENTERGRAPHOPTIONS

ImageSegmenterGraphOptions = _reflection.GeneratedProtocolMessageType('ImageSegmenterGraphOptions', (_message.Message,), dict(
  DESCRIPTOR = _IMAGESEGMENTERGRAPHOPTIONS,
  __module__ = 'mediapipe.tasks.cc.vision.image_segmenter.proto.image_segmenter_graph_options_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptions)
  ))
_sym_db.RegisterMessage(ImageSegmenterGraphOptions)

_IMAGESEGMENTERGRAPHOPTIONS.extensions_by_name['ext'].message_type = _IMAGESEGMENTERGRAPHOPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_IMAGESEGMENTERGRAPHOPTIONS.extensions_by_name['ext'])

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\037ImageSegmenterGraphOptionsProto'))
# @@protoc_insertion_point(module_scope)
