# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/text/text_classifier/proto/text_classifier_graph_options.proto

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
from mediapipe.tasks.cc.components.processors.proto import classifier_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_components_dot_processors_dot_proto_dot_classifier__options__pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/text/text_classifier/proto/text_classifier_graph_options.proto',
  package='mediapipe.tasks.text.text_classifier.proto',
  syntax='proto2',
  serialized_pb=_b('\nQmediapipe/tasks/cc/text/text_classifier/proto/text_classifier_graph_options.proto\x12*mediapipe.tasks.text.text_classifier.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\x1aGmediapipe/tasks/cc/components/processors/proto/classifier_options.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\"\xae\x02\n\x1aTextClassifierGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12Z\n\x12\x63lassifier_options\x18\x02 \x01(\x0b\x32>.mediapipe.tasks.components.processors.proto.ClassifierOptions2u\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xa5\x9f\xd1\xdc\x01 \x01(\x0b\x32\x46.mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptionsBW\n4com.google.mediapipe.tasks.text.textclassifier.protoB\x1fTextClassifierGraphOptionsProto')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,mediapipe_dot_framework_dot_calculator__options__pb2.DESCRIPTOR,mediapipe_dot_tasks_dot_cc_dot_components_dot_processors_dot_proto_dot_classifier__options__pb2.DESCRIPTOR,mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TEXTCLASSIFIERGRAPHOPTIONS = _descriptor.Descriptor(
  name='TextClassifierGraphOptions',
  full_name='mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_options', full_name='mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptions.base_options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='classifier_options', full_name='mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptions.classifier_options', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptions.ext', index=0,
      number=462704549, type=11, cpp_type=10, label=1,
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
  serialized_start=337,
  serialized_end=639,
)

_TEXTCLASSIFIERGRAPHOPTIONS.fields_by_name['base_options'].message_type = mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2._BASEOPTIONS
_TEXTCLASSIFIERGRAPHOPTIONS.fields_by_name['classifier_options'].message_type = mediapipe_dot_tasks_dot_cc_dot_components_dot_processors_dot_proto_dot_classifier__options__pb2._CLASSIFIEROPTIONS
DESCRIPTOR.message_types_by_name['TextClassifierGraphOptions'] = _TEXTCLASSIFIERGRAPHOPTIONS

TextClassifierGraphOptions = _reflection.GeneratedProtocolMessageType('TextClassifierGraphOptions', (_message.Message,), dict(
  DESCRIPTOR = _TEXTCLASSIFIERGRAPHOPTIONS,
  __module__ = 'mediapipe.tasks.cc.text.text_classifier.proto.text_classifier_graph_options_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.text.text_classifier.proto.TextClassifierGraphOptions)
  ))
_sym_db.RegisterMessage(TextClassifierGraphOptions)

_TEXTCLASSIFIERGRAPHOPTIONS.extensions_by_name['ext'].message_type = _TEXTCLASSIFIERGRAPHOPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TEXTCLASSIFIERGRAPHOPTIONS.extensions_by_name['ext'])

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n4com.google.mediapipe.tasks.text.textclassifier.protoB\037TextClassifierGraphOptionsProto'))
# @@protoc_insertion_point(module_scope)
