# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class QueueConversationVideoEventTopicVideo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueueConversationVideoEventTopicVideo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'initial_state': 'str',
            'pcSelf': 'QueueConversationVideoEventTopicAddress',
            'id': 'str',
            'context': 'str',
            'audio_muted': 'bool',
            'video_muted': 'bool',
            'sharing_screen': 'bool',
            'peer_count': 'object',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'disconnect_type': 'str',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'msids': 'list[str]',
            'wrapup': 'QueueConversationVideoEventTopicWrapup',
            'after_call_work': 'QueueConversationVideoEventTopicAfterCallWork',
            'after_call_work_required': 'bool'
        }

        self.attribute_map = {
            'state': 'state',
            'initial_state': 'initialState',
            'pcSelf': 'self',
            'id': 'id',
            'context': 'context',
            'audio_muted': 'audioMuted',
            'video_muted': 'videoMuted',
            'sharing_screen': 'sharingScreen',
            'peer_count': 'peerCount',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'disconnect_type': 'disconnectType',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'msids': 'msids',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'after_call_work_required': 'afterCallWorkRequired'
        }

        self._state = None
        self._initial_state = None
        self._pcSelf = None
        self._id = None
        self._context = None
        self._audio_muted = None
        self._video_muted = None
        self._sharing_screen = None
        self._peer_count = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._disconnect_type = None
        self._connected_time = None
        self._disconnected_time = None
        self._msids = None
        self._wrapup = None
        self._after_call_work = None
        self._after_call_work_required = None

    @property
    def state(self):
        """
        Gets the state of this QueueConversationVideoEventTopicVideo.


        :return: The state of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this QueueConversationVideoEventTopicVideo.


        :param state: The state of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        allowed_values = ["alerting", "dialing", "contacting", "offering", "connected", "disconnected", "terminated", "none"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def initial_state(self):
        """
        Gets the initial_state of this QueueConversationVideoEventTopicVideo.


        :return: The initial_state of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._initial_state

    @initial_state.setter
    def initial_state(self, initial_state):
        """
        Sets the initial_state of this QueueConversationVideoEventTopicVideo.


        :param initial_state: The initial_state of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        allowed_values = ["alerting", "dialing", "contacting", "offering", "connected", "disconnected", "terminated", "none"]
        if initial_state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for initial_state -> " + initial_state)
            self._initial_state = "outdated_sdk_version"
        else:
            self._initial_state = initial_state

    @property
    def pcSelf(self):
        """
        Gets the pcSelf of this QueueConversationVideoEventTopicVideo.
        Address and name data for a call endpoint.

        :return: The pcSelf of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicAddress
        """
        return self._pcSelf

    @pcSelf.setter
    def pcSelf(self, pcSelf):
        """
        Sets the pcSelf of this QueueConversationVideoEventTopicVideo.
        Address and name data for a call endpoint.

        :param pcSelf: The pcSelf of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicAddress
        """
        

        self._pcSelf = pcSelf

    @property
    def id(self):
        """
        Gets the id of this QueueConversationVideoEventTopicVideo.
        A globally unique identifier for this communication.

        :return: The id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QueueConversationVideoEventTopicVideo.
        A globally unique identifier for this communication.

        :param id: The id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        

        self._id = id

    @property
    def context(self):
        """
        Gets the context of this QueueConversationVideoEventTopicVideo.
        The room id context (xmpp jid) for the conference session.

        :return: The context of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """
        Sets the context of this QueueConversationVideoEventTopicVideo.
        The room id context (xmpp jid) for the conference session.

        :param context: The context of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        

        self._context = context

    @property
    def audio_muted(self):
        """
        Gets the audio_muted of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant has muted their outgoing audio.

        :return: The audio_muted of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._audio_muted

    @audio_muted.setter
    def audio_muted(self, audio_muted):
        """
        Sets the audio_muted of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant has muted their outgoing audio.

        :param audio_muted: The audio_muted of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        

        self._audio_muted = audio_muted

    @property
    def video_muted(self):
        """
        Gets the video_muted of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant has muted/paused their outgoing video.

        :return: The video_muted of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._video_muted

    @video_muted.setter
    def video_muted(self, video_muted):
        """
        Sets the video_muted of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant has muted/paused their outgoing video.

        :param video_muted: The video_muted of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        

        self._video_muted = video_muted

    @property
    def sharing_screen(self):
        """
        Gets the sharing_screen of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant is sharing their screen to the session.

        :return: The sharing_screen of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._sharing_screen

    @sharing_screen.setter
    def sharing_screen(self, sharing_screen):
        """
        Sets the sharing_screen of this QueueConversationVideoEventTopicVideo.
        Indicates whether this participant is sharing their screen to the session.

        :param sharing_screen: The sharing_screen of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        

        self._sharing_screen = sharing_screen

    @property
    def peer_count(self):
        """
        Gets the peer_count of this QueueConversationVideoEventTopicVideo.
        The number of peer participants from the perspective of the participant in the conference.

        :return: The peer_count of this QueueConversationVideoEventTopicVideo.
        :rtype: object
        """
        return self._peer_count

    @peer_count.setter
    def peer_count(self, peer_count):
        """
        Sets the peer_count of this QueueConversationVideoEventTopicVideo.
        The number of peer participants from the perspective of the participant in the conference.

        :param peer_count: The peer_count of this QueueConversationVideoEventTopicVideo.
        :type: object
        """
        

        self._peer_count = peer_count

    @property
    def provider(self):
        """
        Gets the provider of this QueueConversationVideoEventTopicVideo.
        The media provider controlling the video.

        :return: The provider of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this QueueConversationVideoEventTopicVideo.
        The media provider controlling the video.

        :param provider: The provider of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        

        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this QueueConversationVideoEventTopicVideo.
        The UUID of the script to use.

        :return: The script_id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this QueueConversationVideoEventTopicVideo.
        The UUID of the script to use.

        :param script_id: The script_id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        

        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this QueueConversationVideoEventTopicVideo.
        The id of the peer communication corresponding to a matching leg for this communication.

        :return: The peer_id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this QueueConversationVideoEventTopicVideo.
        The id of the peer communication corresponding to a matching leg for this communication.

        :param peer_id: The peer_id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        

        self._peer_id = peer_id

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this QueueConversationVideoEventTopicVideo.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this QueueConversationVideoEventTopicVideo.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        allowed_values = ["endpoint", "client", "system", "timeout", "transfer", "transfer.conference", "transfer.consult", "transfer.forward", "transfer.noanswer", "transfer.notavailable", "transport.failure", "error", "peer", "other", "spam", "uncallable"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for disconnect_type -> " + disconnect_type)
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def connected_time(self):
        """
        Gets the connected_time of this QueueConversationVideoEventTopicVideo.
        The timestamp when this communication was connected in the cloud clock.

        :return: The connected_time of this QueueConversationVideoEventTopicVideo.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this QueueConversationVideoEventTopicVideo.
        The timestamp when this communication was connected in the cloud clock.

        :param connected_time: The connected_time of this QueueConversationVideoEventTopicVideo.
        :type: datetime
        """
        

        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this QueueConversationVideoEventTopicVideo.
        The timestamp when this communication disconnected from the conversation in the provider clock.

        :return: The disconnected_time of this QueueConversationVideoEventTopicVideo.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this QueueConversationVideoEventTopicVideo.
        The timestamp when this communication disconnected from the conversation in the provider clock.

        :param disconnected_time: The disconnected_time of this QueueConversationVideoEventTopicVideo.
        :type: datetime
        """
        

        self._disconnected_time = disconnected_time

    @property
    def msids(self):
        """
        Gets the msids of this QueueConversationVideoEventTopicVideo.
        List of media stream ids

        :return: The msids of this QueueConversationVideoEventTopicVideo.
        :rtype: list[str]
        """
        return self._msids

    @msids.setter
    def msids(self, msids):
        """
        Sets the msids of this QueueConversationVideoEventTopicVideo.
        List of media stream ids

        :param msids: The msids of this QueueConversationVideoEventTopicVideo.
        :type: list[str]
        """
        

        self._msids = msids

    @property
    def wrapup(self):
        """
        Gets the wrapup of this QueueConversationVideoEventTopicVideo.
        Call wrap up or disposition data.

        :return: The wrapup of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this QueueConversationVideoEventTopicVideo.
        Call wrap up or disposition data.

        :param wrapup: The wrapup of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicWrapup
        """
        

        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this QueueConversationVideoEventTopicVideo.
        A communication's after-call work data.

        :return: The after_call_work of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicAfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this QueueConversationVideoEventTopicVideo.
        A communication's after-call work data.

        :param after_call_work: The after_call_work of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicAfterCallWork
        """
        

        self._after_call_work = after_call_work

    @property
    def after_call_work_required(self):
        """
        Gets the after_call_work_required of this QueueConversationVideoEventTopicVideo.
        Indicates if after-call is required for a communication. Only used when the ACW Setting is Agent Requested.

        :return: The after_call_work_required of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._after_call_work_required

    @after_call_work_required.setter
    def after_call_work_required(self, after_call_work_required):
        """
        Sets the after_call_work_required of this QueueConversationVideoEventTopicVideo.
        Indicates if after-call is required for a communication. Only used when the ACW Setting is Agent Requested.

        :param after_call_work_required: The after_call_work_required of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        

        self._after_call_work_required = after_call_work_required

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

