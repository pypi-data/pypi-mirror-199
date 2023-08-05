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


class ResponsePipelineSpec(object):
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
        'parameter_specs': 'dict[str, PipelinePipelineSingleVariableSpec]',
        'published': 'bool',
        'step_dependencies': 'list[ResponsePipelineStepDependency]',
        'steps': 'list[ResponseReducedPipelineStep]'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'parameter_specs': 'parameter_specs',
        'published': 'published',
        'step_dependencies': 'step_dependencies',
        'steps': 'steps'
    }

    def __init__(self, created_dt=None, parameter_specs=None, published=None, step_dependencies=None, steps=None, local_vars_configuration=None):  # noqa: E501
        """ResponsePipelineSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._parameter_specs = None
        self._published = None
        self._step_dependencies = None
        self._steps = None
        self.discriminator = None

        self.created_dt = created_dt
        self.parameter_specs = parameter_specs
        self.published = published
        self.step_dependencies = step_dependencies
        self.steps = steps

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponsePipelineSpec.  # noqa: E501


        :return: The created_dt of this ResponsePipelineSpec.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponsePipelineSpec.


        :param created_dt: The created_dt of this ResponsePipelineSpec.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def parameter_specs(self):
        """Gets the parameter_specs of this ResponsePipelineSpec.  # noqa: E501


        :return: The parameter_specs of this ResponsePipelineSpec.  # noqa: E501
        :rtype: dict[str, PipelinePipelineSingleVariableSpec]
        """
        return self._parameter_specs

    @parameter_specs.setter
    def parameter_specs(self, parameter_specs):
        """Sets the parameter_specs of this ResponsePipelineSpec.


        :param parameter_specs: The parameter_specs of this ResponsePipelineSpec.  # noqa: E501
        :type parameter_specs: dict[str, PipelinePipelineSingleVariableSpec]
        """
        if self.local_vars_configuration.client_side_validation and parameter_specs is None:  # noqa: E501
            raise ValueError("Invalid value for `parameter_specs`, must not be `None`")  # noqa: E501

        self._parameter_specs = parameter_specs

    @property
    def published(self):
        """Gets the published of this ResponsePipelineSpec.  # noqa: E501


        :return: The published of this ResponsePipelineSpec.  # noqa: E501
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """Sets the published of this ResponsePipelineSpec.


        :param published: The published of this ResponsePipelineSpec.  # noqa: E501
        :type published: bool
        """
        if self.local_vars_configuration.client_side_validation and published is None:  # noqa: E501
            raise ValueError("Invalid value for `published`, must not be `None`")  # noqa: E501

        self._published = published

    @property
    def step_dependencies(self):
        """Gets the step_dependencies of this ResponsePipelineSpec.  # noqa: E501


        :return: The step_dependencies of this ResponsePipelineSpec.  # noqa: E501
        :rtype: list[ResponsePipelineStepDependency]
        """
        return self._step_dependencies

    @step_dependencies.setter
    def step_dependencies(self, step_dependencies):
        """Sets the step_dependencies of this ResponsePipelineSpec.


        :param step_dependencies: The step_dependencies of this ResponsePipelineSpec.  # noqa: E501
        :type step_dependencies: list[ResponsePipelineStepDependency]
        """
        if self.local_vars_configuration.client_side_validation and step_dependencies is None:  # noqa: E501
            raise ValueError("Invalid value for `step_dependencies`, must not be `None`")  # noqa: E501

        self._step_dependencies = step_dependencies

    @property
    def steps(self):
        """Gets the steps of this ResponsePipelineSpec.  # noqa: E501


        :return: The steps of this ResponsePipelineSpec.  # noqa: E501
        :rtype: list[ResponseReducedPipelineStep]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """Sets the steps of this ResponsePipelineSpec.


        :param steps: The steps of this ResponsePipelineSpec.  # noqa: E501
        :type steps: list[ResponseReducedPipelineStep]
        """
        if self.local_vars_configuration.client_side_validation and steps is None:  # noqa: E501
            raise ValueError("Invalid value for `steps`, must not be `None`")  # noqa: E501

        self._steps = steps

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
        if not isinstance(other, ResponsePipelineSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponsePipelineSpec):
            return True

        return self.to_dict() != other.to_dict()
