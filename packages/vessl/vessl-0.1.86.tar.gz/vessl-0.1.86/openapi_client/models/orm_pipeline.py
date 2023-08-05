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


class OrmPipeline(object):
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
        'created_by_id': 'int',
        'created_dt': 'datetime',
        'description': 'str',
        'edges': 'OrmPipelineEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'last_triggered_by': 'str',
        'last_triggered_dt': 'datetime',
        'name': 'str',
        'organization_id': 'int',
        'updated_dt': 'datetime',
        'volume_id': 'int'
    }

    attribute_map = {
        'created_by_id': 'created_by_id',
        'created_dt': 'created_dt',
        'description': 'description',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'last_triggered_by': 'last_triggered_by',
        'last_triggered_dt': 'last_triggered_dt',
        'name': 'name',
        'organization_id': 'organization_id',
        'updated_dt': 'updated_dt',
        'volume_id': 'volume_id'
    }

    def __init__(self, created_by_id=None, created_dt=None, description=None, edges=None, id=None, immutable_slug=None, last_triggered_by=None, last_triggered_dt=None, name=None, organization_id=None, updated_dt=None, volume_id=None, local_vars_configuration=None):  # noqa: E501
        """OrmPipeline - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_by_id = None
        self._created_dt = None
        self._description = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._last_triggered_by = None
        self._last_triggered_dt = None
        self._name = None
        self._organization_id = None
        self._updated_dt = None
        self._volume_id = None
        self.discriminator = None

        if created_by_id is not None:
            self.created_by_id = created_by_id
        if created_dt is not None:
            self.created_dt = created_dt
        if description is not None:
            self.description = description
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        self.last_triggered_by = last_triggered_by
        self.last_triggered_dt = last_triggered_dt
        if name is not None:
            self.name = name
        if organization_id is not None:
            self.organization_id = organization_id
        if updated_dt is not None:
            self.updated_dt = updated_dt
        if volume_id is not None:
            self.volume_id = volume_id

    @property
    def created_by_id(self):
        """Gets the created_by_id of this OrmPipeline.  # noqa: E501


        :return: The created_by_id of this OrmPipeline.  # noqa: E501
        :rtype: int
        """
        return self._created_by_id

    @created_by_id.setter
    def created_by_id(self, created_by_id):
        """Sets the created_by_id of this OrmPipeline.


        :param created_by_id: The created_by_id of this OrmPipeline.  # noqa: E501
        :type created_by_id: int
        """

        self._created_by_id = created_by_id

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmPipeline.  # noqa: E501


        :return: The created_dt of this OrmPipeline.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmPipeline.


        :param created_dt: The created_dt of this OrmPipeline.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def description(self):
        """Gets the description of this OrmPipeline.  # noqa: E501


        :return: The description of this OrmPipeline.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OrmPipeline.


        :param description: The description of this OrmPipeline.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def edges(self):
        """Gets the edges of this OrmPipeline.  # noqa: E501


        :return: The edges of this OrmPipeline.  # noqa: E501
        :rtype: OrmPipelineEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmPipeline.


        :param edges: The edges of this OrmPipeline.  # noqa: E501
        :type edges: OrmPipelineEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmPipeline.  # noqa: E501


        :return: The id of this OrmPipeline.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmPipeline.


        :param id: The id of this OrmPipeline.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this OrmPipeline.  # noqa: E501


        :return: The immutable_slug of this OrmPipeline.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this OrmPipeline.


        :param immutable_slug: The immutable_slug of this OrmPipeline.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def last_triggered_by(self):
        """Gets the last_triggered_by of this OrmPipeline.  # noqa: E501


        :return: The last_triggered_by of this OrmPipeline.  # noqa: E501
        :rtype: str
        """
        return self._last_triggered_by

    @last_triggered_by.setter
    def last_triggered_by(self, last_triggered_by):
        """Sets the last_triggered_by of this OrmPipeline.


        :param last_triggered_by: The last_triggered_by of this OrmPipeline.  # noqa: E501
        :type last_triggered_by: str
        """

        self._last_triggered_by = last_triggered_by

    @property
    def last_triggered_dt(self):
        """Gets the last_triggered_dt of this OrmPipeline.  # noqa: E501


        :return: The last_triggered_dt of this OrmPipeline.  # noqa: E501
        :rtype: datetime
        """
        return self._last_triggered_dt

    @last_triggered_dt.setter
    def last_triggered_dt(self, last_triggered_dt):
        """Sets the last_triggered_dt of this OrmPipeline.


        :param last_triggered_dt: The last_triggered_dt of this OrmPipeline.  # noqa: E501
        :type last_triggered_dt: datetime
        """

        self._last_triggered_dt = last_triggered_dt

    @property
    def name(self):
        """Gets the name of this OrmPipeline.  # noqa: E501


        :return: The name of this OrmPipeline.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrmPipeline.


        :param name: The name of this OrmPipeline.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def organization_id(self):
        """Gets the organization_id of this OrmPipeline.  # noqa: E501


        :return: The organization_id of this OrmPipeline.  # noqa: E501
        :rtype: int
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this OrmPipeline.


        :param organization_id: The organization_id of this OrmPipeline.  # noqa: E501
        :type organization_id: int
        """

        self._organization_id = organization_id

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmPipeline.  # noqa: E501


        :return: The updated_dt of this OrmPipeline.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmPipeline.


        :param updated_dt: The updated_dt of this OrmPipeline.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def volume_id(self):
        """Gets the volume_id of this OrmPipeline.  # noqa: E501


        :return: The volume_id of this OrmPipeline.  # noqa: E501
        :rtype: int
        """
        return self._volume_id

    @volume_id.setter
    def volume_id(self, volume_id):
        """Sets the volume_id of this OrmPipeline.


        :param volume_id: The volume_id of this OrmPipeline.  # noqa: E501
        :type volume_id: int
        """

        self._volume_id = volume_id

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
        if not isinstance(other, OrmPipeline):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmPipeline):
            return True

        return self.to_dict() != other.to_dict()
