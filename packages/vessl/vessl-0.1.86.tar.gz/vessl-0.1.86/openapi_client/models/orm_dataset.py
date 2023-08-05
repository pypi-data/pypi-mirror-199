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


class OrmDataset(object):
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
        'created_dt': 'datetime',
        'dataset_organization': 'int',
        'dataset_version_volume': 'int',
        'dataset_volume': 'int',
        'description': 'str',
        'edges': 'OrmDatasetEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'is_example': 'bool',
        'is_public': 'bool',
        'is_sample': 'bool',
        'is_version_enabled': 'bool',
        'name': 'str',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'dataset_organization': 'dataset_organization',
        'dataset_version_volume': 'dataset_version_volume',
        'dataset_volume': 'dataset_volume',
        'description': 'description',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_example': 'is_example',
        'is_public': 'is_public',
        'is_sample': 'is_sample',
        'is_version_enabled': 'is_version_enabled',
        'name': 'name',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, created_dt=None, dataset_organization=None, dataset_version_volume=None, dataset_volume=None, description=None, edges=None, id=None, immutable_slug=None, is_example=None, is_public=None, is_sample=None, is_version_enabled=None, name=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """OrmDataset - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._dataset_organization = None
        self._dataset_version_volume = None
        self._dataset_volume = None
        self._description = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._is_example = None
        self._is_public = None
        self._is_sample = None
        self._is_version_enabled = None
        self._name = None
        self._updated_dt = None
        self.discriminator = None

        if created_dt is not None:
            self.created_dt = created_dt
        if dataset_organization is not None:
            self.dataset_organization = dataset_organization
        self.dataset_version_volume = dataset_version_volume
        if dataset_volume is not None:
            self.dataset_volume = dataset_volume
        self.description = description
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if is_example is not None:
            self.is_example = is_example
        if is_public is not None:
            self.is_public = is_public
        if is_sample is not None:
            self.is_sample = is_sample
        if is_version_enabled is not None:
            self.is_version_enabled = is_version_enabled
        if name is not None:
            self.name = name
        if updated_dt is not None:
            self.updated_dt = updated_dt

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmDataset.  # noqa: E501


        :return: The created_dt of this OrmDataset.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmDataset.


        :param created_dt: The created_dt of this OrmDataset.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def dataset_organization(self):
        """Gets the dataset_organization of this OrmDataset.  # noqa: E501


        :return: The dataset_organization of this OrmDataset.  # noqa: E501
        :rtype: int
        """
        return self._dataset_organization

    @dataset_organization.setter
    def dataset_organization(self, dataset_organization):
        """Sets the dataset_organization of this OrmDataset.


        :param dataset_organization: The dataset_organization of this OrmDataset.  # noqa: E501
        :type dataset_organization: int
        """

        self._dataset_organization = dataset_organization

    @property
    def dataset_version_volume(self):
        """Gets the dataset_version_volume of this OrmDataset.  # noqa: E501


        :return: The dataset_version_volume of this OrmDataset.  # noqa: E501
        :rtype: int
        """
        return self._dataset_version_volume

    @dataset_version_volume.setter
    def dataset_version_volume(self, dataset_version_volume):
        """Sets the dataset_version_volume of this OrmDataset.


        :param dataset_version_volume: The dataset_version_volume of this OrmDataset.  # noqa: E501
        :type dataset_version_volume: int
        """

        self._dataset_version_volume = dataset_version_volume

    @property
    def dataset_volume(self):
        """Gets the dataset_volume of this OrmDataset.  # noqa: E501


        :return: The dataset_volume of this OrmDataset.  # noqa: E501
        :rtype: int
        """
        return self._dataset_volume

    @dataset_volume.setter
    def dataset_volume(self, dataset_volume):
        """Sets the dataset_volume of this OrmDataset.


        :param dataset_volume: The dataset_volume of this OrmDataset.  # noqa: E501
        :type dataset_volume: int
        """

        self._dataset_volume = dataset_volume

    @property
    def description(self):
        """Gets the description of this OrmDataset.  # noqa: E501


        :return: The description of this OrmDataset.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OrmDataset.


        :param description: The description of this OrmDataset.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def edges(self):
        """Gets the edges of this OrmDataset.  # noqa: E501


        :return: The edges of this OrmDataset.  # noqa: E501
        :rtype: OrmDatasetEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmDataset.


        :param edges: The edges of this OrmDataset.  # noqa: E501
        :type edges: OrmDatasetEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmDataset.  # noqa: E501


        :return: The id of this OrmDataset.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmDataset.


        :param id: The id of this OrmDataset.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this OrmDataset.  # noqa: E501


        :return: The immutable_slug of this OrmDataset.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this OrmDataset.


        :param immutable_slug: The immutable_slug of this OrmDataset.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def is_example(self):
        """Gets the is_example of this OrmDataset.  # noqa: E501


        :return: The is_example of this OrmDataset.  # noqa: E501
        :rtype: bool
        """
        return self._is_example

    @is_example.setter
    def is_example(self, is_example):
        """Sets the is_example of this OrmDataset.


        :param is_example: The is_example of this OrmDataset.  # noqa: E501
        :type is_example: bool
        """

        self._is_example = is_example

    @property
    def is_public(self):
        """Gets the is_public of this OrmDataset.  # noqa: E501


        :return: The is_public of this OrmDataset.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this OrmDataset.


        :param is_public: The is_public of this OrmDataset.  # noqa: E501
        :type is_public: bool
        """

        self._is_public = is_public

    @property
    def is_sample(self):
        """Gets the is_sample of this OrmDataset.  # noqa: E501


        :return: The is_sample of this OrmDataset.  # noqa: E501
        :rtype: bool
        """
        return self._is_sample

    @is_sample.setter
    def is_sample(self, is_sample):
        """Sets the is_sample of this OrmDataset.


        :param is_sample: The is_sample of this OrmDataset.  # noqa: E501
        :type is_sample: bool
        """

        self._is_sample = is_sample

    @property
    def is_version_enabled(self):
        """Gets the is_version_enabled of this OrmDataset.  # noqa: E501


        :return: The is_version_enabled of this OrmDataset.  # noqa: E501
        :rtype: bool
        """
        return self._is_version_enabled

    @is_version_enabled.setter
    def is_version_enabled(self, is_version_enabled):
        """Sets the is_version_enabled of this OrmDataset.


        :param is_version_enabled: The is_version_enabled of this OrmDataset.  # noqa: E501
        :type is_version_enabled: bool
        """

        self._is_version_enabled = is_version_enabled

    @property
    def name(self):
        """Gets the name of this OrmDataset.  # noqa: E501


        :return: The name of this OrmDataset.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrmDataset.


        :param name: The name of this OrmDataset.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmDataset.  # noqa: E501


        :return: The updated_dt of this OrmDataset.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmDataset.


        :param updated_dt: The updated_dt of this OrmDataset.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

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
        if not isinstance(other, OrmDataset):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmDataset):
            return True

        return self.to_dict() != other.to_dict()
