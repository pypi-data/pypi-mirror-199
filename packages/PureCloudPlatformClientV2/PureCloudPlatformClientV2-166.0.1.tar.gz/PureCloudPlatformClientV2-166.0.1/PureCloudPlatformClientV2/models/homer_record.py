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

class HomerRecord(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        HomerRecord - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'date': 'datetime',
            'milli_ts': 'str',
            'micro_ts': 'str',
            'method': 'str',
            'reply_reason': 'str',
            'ruri': 'str',
            'ruri_user': 'str',
            'ruri_domain': 'str',
            'from_user': 'str',
            'from_domain': 'str',
            'from_tag': 'str',
            'to_user': 'str',
            'to_domain': 'str',
            'to_tag': 'str',
            'pid_user': 'str',
            'contact_user': 'str',
            'auth_user': 'str',
            'callid': 'str',
            'callid_aleg': 'str',
            'via1': 'str',
            'via1_branch': 'str',
            'cseq': 'str',
            'diversion': 'str',
            'reason': 'str',
            'content_type': 'str',
            'auth': 'str',
            'user_agent': 'str',
            'source_ip': 'str',
            'source_port': 'str',
            'destination_ip': 'str',
            'destination_port': 'str',
            'contact_ip': 'str',
            'contact_port': 'str',
            'originator_ip': 'str',
            'originator_port': 'str',
            'correlation_id': 'str',
            'proto': 'str',
            'family': 'str',
            'rtp_stat': 'str',
            'type': 'str',
            'node': 'str',
            'trans': 'str',
            'dbnode': 'str',
            'msg': 'str',
            'source_alias': 'str',
            'destination_alias': 'str',
            'conversation_id': 'str',
            'participant_id': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'date': 'date',
            'milli_ts': 'milliTs',
            'micro_ts': 'microTs',
            'method': 'method',
            'reply_reason': 'replyReason',
            'ruri': 'ruri',
            'ruri_user': 'ruriUser',
            'ruri_domain': 'ruriDomain',
            'from_user': 'fromUser',
            'from_domain': 'fromDomain',
            'from_tag': 'fromTag',
            'to_user': 'toUser',
            'to_domain': 'toDomain',
            'to_tag': 'toTag',
            'pid_user': 'pidUser',
            'contact_user': 'contactUser',
            'auth_user': 'authUser',
            'callid': 'callid',
            'callid_aleg': 'callidAleg',
            'via1': 'via1',
            'via1_branch': 'via1Branch',
            'cseq': 'cseq',
            'diversion': 'diversion',
            'reason': 'reason',
            'content_type': 'contentType',
            'auth': 'auth',
            'user_agent': 'userAgent',
            'source_ip': 'sourceIp',
            'source_port': 'sourcePort',
            'destination_ip': 'destinationIp',
            'destination_port': 'destinationPort',
            'contact_ip': 'contactIp',
            'contact_port': 'contactPort',
            'originator_ip': 'originatorIp',
            'originator_port': 'originatorPort',
            'correlation_id': 'correlationId',
            'proto': 'proto',
            'family': 'family',
            'rtp_stat': 'rtpStat',
            'type': 'type',
            'node': 'node',
            'trans': 'trans',
            'dbnode': 'dbnode',
            'msg': 'msg',
            'source_alias': 'sourceAlias',
            'destination_alias': 'destinationAlias',
            'conversation_id': 'conversationId',
            'participant_id': 'participantId',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._date = None
        self._milli_ts = None
        self._micro_ts = None
        self._method = None
        self._reply_reason = None
        self._ruri = None
        self._ruri_user = None
        self._ruri_domain = None
        self._from_user = None
        self._from_domain = None
        self._from_tag = None
        self._to_user = None
        self._to_domain = None
        self._to_tag = None
        self._pid_user = None
        self._contact_user = None
        self._auth_user = None
        self._callid = None
        self._callid_aleg = None
        self._via1 = None
        self._via1_branch = None
        self._cseq = None
        self._diversion = None
        self._reason = None
        self._content_type = None
        self._auth = None
        self._user_agent = None
        self._source_ip = None
        self._source_port = None
        self._destination_ip = None
        self._destination_port = None
        self._contact_ip = None
        self._contact_port = None
        self._originator_ip = None
        self._originator_port = None
        self._correlation_id = None
        self._proto = None
        self._family = None
        self._rtp_stat = None
        self._type = None
        self._node = None
        self._trans = None
        self._dbnode = None
        self._msg = None
        self._source_alias = None
        self._destination_alias = None
        self._conversation_id = None
        self._participant_id = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this HomerRecord.
        The globally unique identifier for the object.

        :return: The id of this HomerRecord.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this HomerRecord.
        The globally unique identifier for the object.

        :param id: The id of this HomerRecord.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this HomerRecord.


        :return: The name of this HomerRecord.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this HomerRecord.


        :param name: The name of this HomerRecord.
        :type: str
        """
        

        self._name = name

    @property
    def date(self):
        """
        Gets the date of this HomerRecord.
        metadata associated to the SIP calls. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date of this HomerRecord.
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """
        Sets the date of this HomerRecord.
        metadata associated to the SIP calls. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date: The date of this HomerRecord.
        :type: datetime
        """
        

        self._date = date

    @property
    def milli_ts(self):
        """
        Gets the milli_ts of this HomerRecord.
        metadata associated to the SIP calls

        :return: The milli_ts of this HomerRecord.
        :rtype: str
        """
        return self._milli_ts

    @milli_ts.setter
    def milli_ts(self, milli_ts):
        """
        Sets the milli_ts of this HomerRecord.
        metadata associated to the SIP calls

        :param milli_ts: The milli_ts of this HomerRecord.
        :type: str
        """
        

        self._milli_ts = milli_ts

    @property
    def micro_ts(self):
        """
        Gets the micro_ts of this HomerRecord.
        metadata associated to the SIP calls

        :return: The micro_ts of this HomerRecord.
        :rtype: str
        """
        return self._micro_ts

    @micro_ts.setter
    def micro_ts(self, micro_ts):
        """
        Sets the micro_ts of this HomerRecord.
        metadata associated to the SIP calls

        :param micro_ts: The micro_ts of this HomerRecord.
        :type: str
        """
        

        self._micro_ts = micro_ts

    @property
    def method(self):
        """
        Gets the method of this HomerRecord.
        metadata associated to the SIP calls

        :return: The method of this HomerRecord.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this HomerRecord.
        metadata associated to the SIP calls

        :param method: The method of this HomerRecord.
        :type: str
        """
        

        self._method = method

    @property
    def reply_reason(self):
        """
        Gets the reply_reason of this HomerRecord.
        metadata associated to the SIP calls

        :return: The reply_reason of this HomerRecord.
        :rtype: str
        """
        return self._reply_reason

    @reply_reason.setter
    def reply_reason(self, reply_reason):
        """
        Sets the reply_reason of this HomerRecord.
        metadata associated to the SIP calls

        :param reply_reason: The reply_reason of this HomerRecord.
        :type: str
        """
        

        self._reply_reason = reply_reason

    @property
    def ruri(self):
        """
        Gets the ruri of this HomerRecord.
        metadata associated to the SIP calls

        :return: The ruri of this HomerRecord.
        :rtype: str
        """
        return self._ruri

    @ruri.setter
    def ruri(self, ruri):
        """
        Sets the ruri of this HomerRecord.
        metadata associated to the SIP calls

        :param ruri: The ruri of this HomerRecord.
        :type: str
        """
        

        self._ruri = ruri

    @property
    def ruri_user(self):
        """
        Gets the ruri_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The ruri_user of this HomerRecord.
        :rtype: str
        """
        return self._ruri_user

    @ruri_user.setter
    def ruri_user(self, ruri_user):
        """
        Sets the ruri_user of this HomerRecord.
        metadata associated to the SIP calls

        :param ruri_user: The ruri_user of this HomerRecord.
        :type: str
        """
        

        self._ruri_user = ruri_user

    @property
    def ruri_domain(self):
        """
        Gets the ruri_domain of this HomerRecord.
        metadata associated to the SIP calls

        :return: The ruri_domain of this HomerRecord.
        :rtype: str
        """
        return self._ruri_domain

    @ruri_domain.setter
    def ruri_domain(self, ruri_domain):
        """
        Sets the ruri_domain of this HomerRecord.
        metadata associated to the SIP calls

        :param ruri_domain: The ruri_domain of this HomerRecord.
        :type: str
        """
        

        self._ruri_domain = ruri_domain

    @property
    def from_user(self):
        """
        Gets the from_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The from_user of this HomerRecord.
        :rtype: str
        """
        return self._from_user

    @from_user.setter
    def from_user(self, from_user):
        """
        Sets the from_user of this HomerRecord.
        metadata associated to the SIP calls

        :param from_user: The from_user of this HomerRecord.
        :type: str
        """
        

        self._from_user = from_user

    @property
    def from_domain(self):
        """
        Gets the from_domain of this HomerRecord.
        metadata associated to the SIP calls

        :return: The from_domain of this HomerRecord.
        :rtype: str
        """
        return self._from_domain

    @from_domain.setter
    def from_domain(self, from_domain):
        """
        Sets the from_domain of this HomerRecord.
        metadata associated to the SIP calls

        :param from_domain: The from_domain of this HomerRecord.
        :type: str
        """
        

        self._from_domain = from_domain

    @property
    def from_tag(self):
        """
        Gets the from_tag of this HomerRecord.
        metadata associated to the SIP calls

        :return: The from_tag of this HomerRecord.
        :rtype: str
        """
        return self._from_tag

    @from_tag.setter
    def from_tag(self, from_tag):
        """
        Sets the from_tag of this HomerRecord.
        metadata associated to the SIP calls

        :param from_tag: The from_tag of this HomerRecord.
        :type: str
        """
        

        self._from_tag = from_tag

    @property
    def to_user(self):
        """
        Gets the to_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The to_user of this HomerRecord.
        :rtype: str
        """
        return self._to_user

    @to_user.setter
    def to_user(self, to_user):
        """
        Sets the to_user of this HomerRecord.
        metadata associated to the SIP calls

        :param to_user: The to_user of this HomerRecord.
        :type: str
        """
        

        self._to_user = to_user

    @property
    def to_domain(self):
        """
        Gets the to_domain of this HomerRecord.
        metadata associated to the SIP calls

        :return: The to_domain of this HomerRecord.
        :rtype: str
        """
        return self._to_domain

    @to_domain.setter
    def to_domain(self, to_domain):
        """
        Sets the to_domain of this HomerRecord.
        metadata associated to the SIP calls

        :param to_domain: The to_domain of this HomerRecord.
        :type: str
        """
        

        self._to_domain = to_domain

    @property
    def to_tag(self):
        """
        Gets the to_tag of this HomerRecord.
        metadata associated to the SIP calls

        :return: The to_tag of this HomerRecord.
        :rtype: str
        """
        return self._to_tag

    @to_tag.setter
    def to_tag(self, to_tag):
        """
        Sets the to_tag of this HomerRecord.
        metadata associated to the SIP calls

        :param to_tag: The to_tag of this HomerRecord.
        :type: str
        """
        

        self._to_tag = to_tag

    @property
    def pid_user(self):
        """
        Gets the pid_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The pid_user of this HomerRecord.
        :rtype: str
        """
        return self._pid_user

    @pid_user.setter
    def pid_user(self, pid_user):
        """
        Sets the pid_user of this HomerRecord.
        metadata associated to the SIP calls

        :param pid_user: The pid_user of this HomerRecord.
        :type: str
        """
        

        self._pid_user = pid_user

    @property
    def contact_user(self):
        """
        Gets the contact_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The contact_user of this HomerRecord.
        :rtype: str
        """
        return self._contact_user

    @contact_user.setter
    def contact_user(self, contact_user):
        """
        Sets the contact_user of this HomerRecord.
        metadata associated to the SIP calls

        :param contact_user: The contact_user of this HomerRecord.
        :type: str
        """
        

        self._contact_user = contact_user

    @property
    def auth_user(self):
        """
        Gets the auth_user of this HomerRecord.
        metadata associated to the SIP calls

        :return: The auth_user of this HomerRecord.
        :rtype: str
        """
        return self._auth_user

    @auth_user.setter
    def auth_user(self, auth_user):
        """
        Sets the auth_user of this HomerRecord.
        metadata associated to the SIP calls

        :param auth_user: The auth_user of this HomerRecord.
        :type: str
        """
        

        self._auth_user = auth_user

    @property
    def callid(self):
        """
        Gets the callid of this HomerRecord.
        metadata associated to the SIP calls

        :return: The callid of this HomerRecord.
        :rtype: str
        """
        return self._callid

    @callid.setter
    def callid(self, callid):
        """
        Sets the callid of this HomerRecord.
        metadata associated to the SIP calls

        :param callid: The callid of this HomerRecord.
        :type: str
        """
        

        self._callid = callid

    @property
    def callid_aleg(self):
        """
        Gets the callid_aleg of this HomerRecord.
        metadata associated to the SIP calls

        :return: The callid_aleg of this HomerRecord.
        :rtype: str
        """
        return self._callid_aleg

    @callid_aleg.setter
    def callid_aleg(self, callid_aleg):
        """
        Sets the callid_aleg of this HomerRecord.
        metadata associated to the SIP calls

        :param callid_aleg: The callid_aleg of this HomerRecord.
        :type: str
        """
        

        self._callid_aleg = callid_aleg

    @property
    def via1(self):
        """
        Gets the via1 of this HomerRecord.
        metadata associated to the SIP calls

        :return: The via1 of this HomerRecord.
        :rtype: str
        """
        return self._via1

    @via1.setter
    def via1(self, via1):
        """
        Sets the via1 of this HomerRecord.
        metadata associated to the SIP calls

        :param via1: The via1 of this HomerRecord.
        :type: str
        """
        

        self._via1 = via1

    @property
    def via1_branch(self):
        """
        Gets the via1_branch of this HomerRecord.
        metadata associated to the SIP calls

        :return: The via1_branch of this HomerRecord.
        :rtype: str
        """
        return self._via1_branch

    @via1_branch.setter
    def via1_branch(self, via1_branch):
        """
        Sets the via1_branch of this HomerRecord.
        metadata associated to the SIP calls

        :param via1_branch: The via1_branch of this HomerRecord.
        :type: str
        """
        

        self._via1_branch = via1_branch

    @property
    def cseq(self):
        """
        Gets the cseq of this HomerRecord.
        metadata associated to the SIP calls

        :return: The cseq of this HomerRecord.
        :rtype: str
        """
        return self._cseq

    @cseq.setter
    def cseq(self, cseq):
        """
        Sets the cseq of this HomerRecord.
        metadata associated to the SIP calls

        :param cseq: The cseq of this HomerRecord.
        :type: str
        """
        

        self._cseq = cseq

    @property
    def diversion(self):
        """
        Gets the diversion of this HomerRecord.
        metadata associated to the SIP calls

        :return: The diversion of this HomerRecord.
        :rtype: str
        """
        return self._diversion

    @diversion.setter
    def diversion(self, diversion):
        """
        Sets the diversion of this HomerRecord.
        metadata associated to the SIP calls

        :param diversion: The diversion of this HomerRecord.
        :type: str
        """
        

        self._diversion = diversion

    @property
    def reason(self):
        """
        Gets the reason of this HomerRecord.
        metadata associated to the SIP calls

        :return: The reason of this HomerRecord.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this HomerRecord.
        metadata associated to the SIP calls

        :param reason: The reason of this HomerRecord.
        :type: str
        """
        

        self._reason = reason

    @property
    def content_type(self):
        """
        Gets the content_type of this HomerRecord.
        metadata associated to the SIP calls

        :return: The content_type of this HomerRecord.
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Sets the content_type of this HomerRecord.
        metadata associated to the SIP calls

        :param content_type: The content_type of this HomerRecord.
        :type: str
        """
        

        self._content_type = content_type

    @property
    def auth(self):
        """
        Gets the auth of this HomerRecord.
        metadata associated to the SIP calls

        :return: The auth of this HomerRecord.
        :rtype: str
        """
        return self._auth

    @auth.setter
    def auth(self, auth):
        """
        Sets the auth of this HomerRecord.
        metadata associated to the SIP calls

        :param auth: The auth of this HomerRecord.
        :type: str
        """
        

        self._auth = auth

    @property
    def user_agent(self):
        """
        Gets the user_agent of this HomerRecord.
        metadata associated to the SIP calls

        :return: The user_agent of this HomerRecord.
        :rtype: str
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        """
        Sets the user_agent of this HomerRecord.
        metadata associated to the SIP calls

        :param user_agent: The user_agent of this HomerRecord.
        :type: str
        """
        

        self._user_agent = user_agent

    @property
    def source_ip(self):
        """
        Gets the source_ip of this HomerRecord.
        metadata associated to the SIP calls

        :return: The source_ip of this HomerRecord.
        :rtype: str
        """
        return self._source_ip

    @source_ip.setter
    def source_ip(self, source_ip):
        """
        Sets the source_ip of this HomerRecord.
        metadata associated to the SIP calls

        :param source_ip: The source_ip of this HomerRecord.
        :type: str
        """
        

        self._source_ip = source_ip

    @property
    def source_port(self):
        """
        Gets the source_port of this HomerRecord.
        metadata associated to the SIP calls

        :return: The source_port of this HomerRecord.
        :rtype: str
        """
        return self._source_port

    @source_port.setter
    def source_port(self, source_port):
        """
        Sets the source_port of this HomerRecord.
        metadata associated to the SIP calls

        :param source_port: The source_port of this HomerRecord.
        :type: str
        """
        

        self._source_port = source_port

    @property
    def destination_ip(self):
        """
        Gets the destination_ip of this HomerRecord.
        metadata associated to the SIP calls

        :return: The destination_ip of this HomerRecord.
        :rtype: str
        """
        return self._destination_ip

    @destination_ip.setter
    def destination_ip(self, destination_ip):
        """
        Sets the destination_ip of this HomerRecord.
        metadata associated to the SIP calls

        :param destination_ip: The destination_ip of this HomerRecord.
        :type: str
        """
        

        self._destination_ip = destination_ip

    @property
    def destination_port(self):
        """
        Gets the destination_port of this HomerRecord.
        metadata associated to the SIP calls

        :return: The destination_port of this HomerRecord.
        :rtype: str
        """
        return self._destination_port

    @destination_port.setter
    def destination_port(self, destination_port):
        """
        Sets the destination_port of this HomerRecord.
        metadata associated to the SIP calls

        :param destination_port: The destination_port of this HomerRecord.
        :type: str
        """
        

        self._destination_port = destination_port

    @property
    def contact_ip(self):
        """
        Gets the contact_ip of this HomerRecord.
        metadata associated to the SIP calls

        :return: The contact_ip of this HomerRecord.
        :rtype: str
        """
        return self._contact_ip

    @contact_ip.setter
    def contact_ip(self, contact_ip):
        """
        Sets the contact_ip of this HomerRecord.
        metadata associated to the SIP calls

        :param contact_ip: The contact_ip of this HomerRecord.
        :type: str
        """
        

        self._contact_ip = contact_ip

    @property
    def contact_port(self):
        """
        Gets the contact_port of this HomerRecord.
        metadata associated to the SIP calls

        :return: The contact_port of this HomerRecord.
        :rtype: str
        """
        return self._contact_port

    @contact_port.setter
    def contact_port(self, contact_port):
        """
        Sets the contact_port of this HomerRecord.
        metadata associated to the SIP calls

        :param contact_port: The contact_port of this HomerRecord.
        :type: str
        """
        

        self._contact_port = contact_port

    @property
    def originator_ip(self):
        """
        Gets the originator_ip of this HomerRecord.
        metadata associated to the SIP calls

        :return: The originator_ip of this HomerRecord.
        :rtype: str
        """
        return self._originator_ip

    @originator_ip.setter
    def originator_ip(self, originator_ip):
        """
        Sets the originator_ip of this HomerRecord.
        metadata associated to the SIP calls

        :param originator_ip: The originator_ip of this HomerRecord.
        :type: str
        """
        

        self._originator_ip = originator_ip

    @property
    def originator_port(self):
        """
        Gets the originator_port of this HomerRecord.
        metadata associated to the SIP calls

        :return: The originator_port of this HomerRecord.
        :rtype: str
        """
        return self._originator_port

    @originator_port.setter
    def originator_port(self, originator_port):
        """
        Sets the originator_port of this HomerRecord.
        metadata associated to the SIP calls

        :param originator_port: The originator_port of this HomerRecord.
        :type: str
        """
        

        self._originator_port = originator_port

    @property
    def correlation_id(self):
        """
        Gets the correlation_id of this HomerRecord.
        metadata associated to the SIP calls

        :return: The correlation_id of this HomerRecord.
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """
        Sets the correlation_id of this HomerRecord.
        metadata associated to the SIP calls

        :param correlation_id: The correlation_id of this HomerRecord.
        :type: str
        """
        

        self._correlation_id = correlation_id

    @property
    def proto(self):
        """
        Gets the proto of this HomerRecord.
        metadata associated to the SIP calls

        :return: The proto of this HomerRecord.
        :rtype: str
        """
        return self._proto

    @proto.setter
    def proto(self, proto):
        """
        Sets the proto of this HomerRecord.
        metadata associated to the SIP calls

        :param proto: The proto of this HomerRecord.
        :type: str
        """
        

        self._proto = proto

    @property
    def family(self):
        """
        Gets the family of this HomerRecord.
        metadata associated to the SIP calls

        :return: The family of this HomerRecord.
        :rtype: str
        """
        return self._family

    @family.setter
    def family(self, family):
        """
        Sets the family of this HomerRecord.
        metadata associated to the SIP calls

        :param family: The family of this HomerRecord.
        :type: str
        """
        

        self._family = family

    @property
    def rtp_stat(self):
        """
        Gets the rtp_stat of this HomerRecord.
        metadata associated to the SIP calls

        :return: The rtp_stat of this HomerRecord.
        :rtype: str
        """
        return self._rtp_stat

    @rtp_stat.setter
    def rtp_stat(self, rtp_stat):
        """
        Sets the rtp_stat of this HomerRecord.
        metadata associated to the SIP calls

        :param rtp_stat: The rtp_stat of this HomerRecord.
        :type: str
        """
        

        self._rtp_stat = rtp_stat

    @property
    def type(self):
        """
        Gets the type of this HomerRecord.
        metadata associated to the SIP calls

        :return: The type of this HomerRecord.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this HomerRecord.
        metadata associated to the SIP calls

        :param type: The type of this HomerRecord.
        :type: str
        """
        

        self._type = type

    @property
    def node(self):
        """
        Gets the node of this HomerRecord.
        metadata associated to the SIP calls

        :return: The node of this HomerRecord.
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node):
        """
        Sets the node of this HomerRecord.
        metadata associated to the SIP calls

        :param node: The node of this HomerRecord.
        :type: str
        """
        

        self._node = node

    @property
    def trans(self):
        """
        Gets the trans of this HomerRecord.
        metadata associated to the SIP calls

        :return: The trans of this HomerRecord.
        :rtype: str
        """
        return self._trans

    @trans.setter
    def trans(self, trans):
        """
        Sets the trans of this HomerRecord.
        metadata associated to the SIP calls

        :param trans: The trans of this HomerRecord.
        :type: str
        """
        

        self._trans = trans

    @property
    def dbnode(self):
        """
        Gets the dbnode of this HomerRecord.
        metadata associated to the SIP calls

        :return: The dbnode of this HomerRecord.
        :rtype: str
        """
        return self._dbnode

    @dbnode.setter
    def dbnode(self, dbnode):
        """
        Sets the dbnode of this HomerRecord.
        metadata associated to the SIP calls

        :param dbnode: The dbnode of this HomerRecord.
        :type: str
        """
        

        self._dbnode = dbnode

    @property
    def msg(self):
        """
        Gets the msg of this HomerRecord.
        metadata associated to the SIP calls

        :return: The msg of this HomerRecord.
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """
        Sets the msg of this HomerRecord.
        metadata associated to the SIP calls

        :param msg: The msg of this HomerRecord.
        :type: str
        """
        

        self._msg = msg

    @property
    def source_alias(self):
        """
        Gets the source_alias of this HomerRecord.
        metadata associated to the SIP calls

        :return: The source_alias of this HomerRecord.
        :rtype: str
        """
        return self._source_alias

    @source_alias.setter
    def source_alias(self, source_alias):
        """
        Sets the source_alias of this HomerRecord.
        metadata associated to the SIP calls

        :param source_alias: The source_alias of this HomerRecord.
        :type: str
        """
        

        self._source_alias = source_alias

    @property
    def destination_alias(self):
        """
        Gets the destination_alias of this HomerRecord.
        metadata associated to the SIP calls

        :return: The destination_alias of this HomerRecord.
        :rtype: str
        """
        return self._destination_alias

    @destination_alias.setter
    def destination_alias(self, destination_alias):
        """
        Sets the destination_alias of this HomerRecord.
        metadata associated to the SIP calls

        :param destination_alias: The destination_alias of this HomerRecord.
        :type: str
        """
        

        self._destination_alias = destination_alias

    @property
    def conversation_id(self):
        """
        Gets the conversation_id of this HomerRecord.
        metadata associated to the SIP calls

        :return: The conversation_id of this HomerRecord.
        :rtype: str
        """
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, conversation_id):
        """
        Sets the conversation_id of this HomerRecord.
        metadata associated to the SIP calls

        :param conversation_id: The conversation_id of this HomerRecord.
        :type: str
        """
        

        self._conversation_id = conversation_id

    @property
    def participant_id(self):
        """
        Gets the participant_id of this HomerRecord.
        metadata associated to the SIP calls

        :return: The participant_id of this HomerRecord.
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """
        Sets the participant_id of this HomerRecord.
        metadata associated to the SIP calls

        :param participant_id: The participant_id of this HomerRecord.
        :type: str
        """
        

        self._participant_id = participant_id

    @property
    def self_uri(self):
        """
        Gets the self_uri of this HomerRecord.
        The URI for this object

        :return: The self_uri of this HomerRecord.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this HomerRecord.
        The URI for this object

        :param self_uri: The self_uri of this HomerRecord.
        :type: str
        """
        

        self._self_uri = self_uri

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

