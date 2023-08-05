# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class OrganizationMemberBulkAddAPI200Response(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'failed_list': 'list[str]',
        'member_list': 'list[ResponseOrganizationMember]'
    }

    attribute_map = {
        'failed_list': 'failed_list',
        'member_list': 'member_list'
    }

    def __init__(self, failed_list=None, member_list=None, local_vars_configuration=None):  # noqa: E501
        """OrganizationMemberBulkAddAPI200Response - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._failed_list = None
        self._member_list = None
        self.discriminator = None

        self.failed_list = failed_list
        self.member_list = member_list

    @property
    def failed_list(self):
        """Gets the failed_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501


        :return: The failed_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501
        :rtype: list[str]
        """
        return self._failed_list

    @failed_list.setter
    def failed_list(self, failed_list):
        """Sets the failed_list of this OrganizationMemberBulkAddAPI200Response.


        :param failed_list: The failed_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501
        :type failed_list: list[str]
        """
        if self.local_vars_configuration.client_side_validation and failed_list is None:  # noqa: E501
            raise ValueError("Invalid value for `failed_list`, must not be `None`")  # noqa: E501

        self._failed_list = failed_list

    @property
    def member_list(self):
        """Gets the member_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501


        :return: The member_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501
        :rtype: list[ResponseOrganizationMember]
        """
        return self._member_list

    @member_list.setter
    def member_list(self, member_list):
        """Sets the member_list of this OrganizationMemberBulkAddAPI200Response.


        :param member_list: The member_list of this OrganizationMemberBulkAddAPI200Response.  # noqa: E501
        :type member_list: list[ResponseOrganizationMember]
        """
        if self.local_vars_configuration.client_side_validation and member_list is None:  # noqa: E501
            raise ValueError("Invalid value for `member_list`, must not be `None`")  # noqa: E501

        self._member_list = member_list

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrganizationMemberBulkAddAPI200Response):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationMemberBulkAddAPI200Response):
            return True

        return self.to_dict() != other.to_dict()
