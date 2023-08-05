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


class OrmPricingPlan(object):
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
        'edges': 'OrmPricingPlanEdges',
        'id': 'int',
        'name': 'str',
        'per_node_price': 'float',
        'per_user_price': 'float'
    }

    attribute_map = {
        'edges': 'edges',
        'id': 'id',
        'name': 'name',
        'per_node_price': 'per_node_price',
        'per_user_price': 'per_user_price'
    }

    def __init__(self, edges=None, id=None, name=None, per_node_price=None, per_user_price=None, local_vars_configuration=None):  # noqa: E501
        """OrmPricingPlan - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._edges = None
        self._id = None
        self._name = None
        self._per_node_price = None
        self._per_user_price = None
        self.discriminator = None

        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if per_node_price is not None:
            self.per_node_price = per_node_price
        if per_user_price is not None:
            self.per_user_price = per_user_price

    @property
    def edges(self):
        """Gets the edges of this OrmPricingPlan.  # noqa: E501


        :return: The edges of this OrmPricingPlan.  # noqa: E501
        :rtype: OrmPricingPlanEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmPricingPlan.


        :param edges: The edges of this OrmPricingPlan.  # noqa: E501
        :type edges: OrmPricingPlanEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmPricingPlan.  # noqa: E501


        :return: The id of this OrmPricingPlan.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmPricingPlan.


        :param id: The id of this OrmPricingPlan.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this OrmPricingPlan.  # noqa: E501


        :return: The name of this OrmPricingPlan.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrmPricingPlan.


        :param name: The name of this OrmPricingPlan.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def per_node_price(self):
        """Gets the per_node_price of this OrmPricingPlan.  # noqa: E501


        :return: The per_node_price of this OrmPricingPlan.  # noqa: E501
        :rtype: float
        """
        return self._per_node_price

    @per_node_price.setter
    def per_node_price(self, per_node_price):
        """Sets the per_node_price of this OrmPricingPlan.


        :param per_node_price: The per_node_price of this OrmPricingPlan.  # noqa: E501
        :type per_node_price: float
        """

        self._per_node_price = per_node_price

    @property
    def per_user_price(self):
        """Gets the per_user_price of this OrmPricingPlan.  # noqa: E501


        :return: The per_user_price of this OrmPricingPlan.  # noqa: E501
        :rtype: float
        """
        return self._per_user_price

    @per_user_price.setter
    def per_user_price(self, per_user_price):
        """Sets the per_user_price of this OrmPricingPlan.


        :param per_user_price: The per_user_price of this OrmPricingPlan.  # noqa: E501
        :type per_user_price: float
        """

        self._per_user_price = per_user_price

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
        if not isinstance(other, OrmPricingPlan):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmPricingPlan):
            return True

        return self.to_dict() != other.to_dict()
