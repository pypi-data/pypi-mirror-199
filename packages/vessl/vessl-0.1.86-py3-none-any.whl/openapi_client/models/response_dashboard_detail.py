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


class ResponseDashboardDetail(object):
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
        'chart_fields': 'list[ResponseDashboardChartField]',
        'chart_sections': 'list[ResponseDashboardChartSection]',
        'created_by': 'ResponseSimpleUser',
        'filters': 'list[ResponseDashboardExperimentFilterResponse]',
        'id': 'int',
        'is_main': 'bool',
        'is_private': 'bool',
        'is_starred': 'bool',
        'last_updated_by': 'ResponseSimpleUser',
        'last_updated_dt': 'datetime',
        'name': 'str',
        'sorts': 'list[ResponseDashboardExperimentSortResponse]'
    }

    attribute_map = {
        'chart_fields': 'chart_fields',
        'chart_sections': 'chart_sections',
        'created_by': 'created_by',
        'filters': 'filters',
        'id': 'id',
        'is_main': 'is_main',
        'is_private': 'is_private',
        'is_starred': 'is_starred',
        'last_updated_by': 'last_updated_by',
        'last_updated_dt': 'last_updated_dt',
        'name': 'name',
        'sorts': 'sorts'
    }

    def __init__(self, chart_fields=None, chart_sections=None, created_by=None, filters=None, id=None, is_main=None, is_private=None, is_starred=None, last_updated_by=None, last_updated_dt=None, name=None, sorts=None, local_vars_configuration=None):  # noqa: E501
        """ResponseDashboardDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._chart_fields = None
        self._chart_sections = None
        self._created_by = None
        self._filters = None
        self._id = None
        self._is_main = None
        self._is_private = None
        self._is_starred = None
        self._last_updated_by = None
        self._last_updated_dt = None
        self._name = None
        self._sorts = None
        self.discriminator = None

        self.chart_fields = chart_fields
        self.chart_sections = chart_sections
        if created_by is not None:
            self.created_by = created_by
        self.filters = filters
        self.id = id
        self.is_main = is_main
        self.is_private = is_private
        self.is_starred = is_starred
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        self.last_updated_dt = last_updated_dt
        self.name = name
        self.sorts = sorts

    @property
    def chart_fields(self):
        """Gets the chart_fields of this ResponseDashboardDetail.  # noqa: E501


        :return: The chart_fields of this ResponseDashboardDetail.  # noqa: E501
        :rtype: list[ResponseDashboardChartField]
        """
        return self._chart_fields

    @chart_fields.setter
    def chart_fields(self, chart_fields):
        """Sets the chart_fields of this ResponseDashboardDetail.


        :param chart_fields: The chart_fields of this ResponseDashboardDetail.  # noqa: E501
        :type chart_fields: list[ResponseDashboardChartField]
        """
        if self.local_vars_configuration.client_side_validation and chart_fields is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_fields`, must not be `None`")  # noqa: E501

        self._chart_fields = chart_fields

    @property
    def chart_sections(self):
        """Gets the chart_sections of this ResponseDashboardDetail.  # noqa: E501


        :return: The chart_sections of this ResponseDashboardDetail.  # noqa: E501
        :rtype: list[ResponseDashboardChartSection]
        """
        return self._chart_sections

    @chart_sections.setter
    def chart_sections(self, chart_sections):
        """Sets the chart_sections of this ResponseDashboardDetail.


        :param chart_sections: The chart_sections of this ResponseDashboardDetail.  # noqa: E501
        :type chart_sections: list[ResponseDashboardChartSection]
        """
        if self.local_vars_configuration.client_side_validation and chart_sections is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_sections`, must not be `None`")  # noqa: E501

        self._chart_sections = chart_sections

    @property
    def created_by(self):
        """Gets the created_by of this ResponseDashboardDetail.  # noqa: E501


        :return: The created_by of this ResponseDashboardDetail.  # noqa: E501
        :rtype: ResponseSimpleUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ResponseDashboardDetail.


        :param created_by: The created_by of this ResponseDashboardDetail.  # noqa: E501
        :type created_by: ResponseSimpleUser
        """

        self._created_by = created_by

    @property
    def filters(self):
        """Gets the filters of this ResponseDashboardDetail.  # noqa: E501


        :return: The filters of this ResponseDashboardDetail.  # noqa: E501
        :rtype: list[ResponseDashboardExperimentFilterResponse]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this ResponseDashboardDetail.


        :param filters: The filters of this ResponseDashboardDetail.  # noqa: E501
        :type filters: list[ResponseDashboardExperimentFilterResponse]
        """
        if self.local_vars_configuration.client_side_validation and filters is None:  # noqa: E501
            raise ValueError("Invalid value for `filters`, must not be `None`")  # noqa: E501

        self._filters = filters

    @property
    def id(self):
        """Gets the id of this ResponseDashboardDetail.  # noqa: E501


        :return: The id of this ResponseDashboardDetail.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseDashboardDetail.


        :param id: The id of this ResponseDashboardDetail.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def is_main(self):
        """Gets the is_main of this ResponseDashboardDetail.  # noqa: E501


        :return: The is_main of this ResponseDashboardDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_main

    @is_main.setter
    def is_main(self, is_main):
        """Sets the is_main of this ResponseDashboardDetail.


        :param is_main: The is_main of this ResponseDashboardDetail.  # noqa: E501
        :type is_main: bool
        """
        if self.local_vars_configuration.client_side_validation and is_main is None:  # noqa: E501
            raise ValueError("Invalid value for `is_main`, must not be `None`")  # noqa: E501

        self._is_main = is_main

    @property
    def is_private(self):
        """Gets the is_private of this ResponseDashboardDetail.  # noqa: E501


        :return: The is_private of this ResponseDashboardDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_private

    @is_private.setter
    def is_private(self, is_private):
        """Sets the is_private of this ResponseDashboardDetail.


        :param is_private: The is_private of this ResponseDashboardDetail.  # noqa: E501
        :type is_private: bool
        """
        if self.local_vars_configuration.client_side_validation and is_private is None:  # noqa: E501
            raise ValueError("Invalid value for `is_private`, must not be `None`")  # noqa: E501

        self._is_private = is_private

    @property
    def is_starred(self):
        """Gets the is_starred of this ResponseDashboardDetail.  # noqa: E501


        :return: The is_starred of this ResponseDashboardDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_starred

    @is_starred.setter
    def is_starred(self, is_starred):
        """Sets the is_starred of this ResponseDashboardDetail.


        :param is_starred: The is_starred of this ResponseDashboardDetail.  # noqa: E501
        :type is_starred: bool
        """
        if self.local_vars_configuration.client_side_validation and is_starred is None:  # noqa: E501
            raise ValueError("Invalid value for `is_starred`, must not be `None`")  # noqa: E501

        self._is_starred = is_starred

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ResponseDashboardDetail.  # noqa: E501


        :return: The last_updated_by of this ResponseDashboardDetail.  # noqa: E501
        :rtype: ResponseSimpleUser
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ResponseDashboardDetail.


        :param last_updated_by: The last_updated_by of this ResponseDashboardDetail.  # noqa: E501
        :type last_updated_by: ResponseSimpleUser
        """

        self._last_updated_by = last_updated_by

    @property
    def last_updated_dt(self):
        """Gets the last_updated_dt of this ResponseDashboardDetail.  # noqa: E501


        :return: The last_updated_dt of this ResponseDashboardDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._last_updated_dt

    @last_updated_dt.setter
    def last_updated_dt(self, last_updated_dt):
        """Sets the last_updated_dt of this ResponseDashboardDetail.


        :param last_updated_dt: The last_updated_dt of this ResponseDashboardDetail.  # noqa: E501
        :type last_updated_dt: datetime
        """

        self._last_updated_dt = last_updated_dt

    @property
    def name(self):
        """Gets the name of this ResponseDashboardDetail.  # noqa: E501


        :return: The name of this ResponseDashboardDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseDashboardDetail.


        :param name: The name of this ResponseDashboardDetail.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def sorts(self):
        """Gets the sorts of this ResponseDashboardDetail.  # noqa: E501


        :return: The sorts of this ResponseDashboardDetail.  # noqa: E501
        :rtype: list[ResponseDashboardExperimentSortResponse]
        """
        return self._sorts

    @sorts.setter
    def sorts(self, sorts):
        """Sets the sorts of this ResponseDashboardDetail.


        :param sorts: The sorts of this ResponseDashboardDetail.  # noqa: E501
        :type sorts: list[ResponseDashboardExperimentSortResponse]
        """
        if self.local_vars_configuration.client_side_validation and sorts is None:  # noqa: E501
            raise ValueError("Invalid value for `sorts`, must not be `None`")  # noqa: E501

        self._sorts = sorts

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
        if not isinstance(other, ResponseDashboardDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseDashboardDetail):
            return True

        return self.to_dict() != other.to_dict()
