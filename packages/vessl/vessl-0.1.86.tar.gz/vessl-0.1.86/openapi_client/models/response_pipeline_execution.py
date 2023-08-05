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


class ResponsePipelineExecution(object):
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
        'arguments': 'list[ResponsePipelineVariable]',
        'created_dt': 'datetime',
        'end_dt': 'datetime',
        'number': 'int',
        'reason': 'str',
        'status': 'str',
        'step_dependencies': 'list[ResponsePipelineStepDependency]',
        'step_executions': 'list[ResponseReducedPipelineStepExecution]',
        'triggered_by': 'ResponseUser'
    }

    attribute_map = {
        'arguments': 'arguments',
        'created_dt': 'created_dt',
        'end_dt': 'end_dt',
        'number': 'number',
        'reason': 'reason',
        'status': 'status',
        'step_dependencies': 'step_dependencies',
        'step_executions': 'step_executions',
        'triggered_by': 'triggered_by'
    }

    def __init__(self, arguments=None, created_dt=None, end_dt=None, number=None, reason=None, status=None, step_dependencies=None, step_executions=None, triggered_by=None, local_vars_configuration=None):  # noqa: E501
        """ResponsePipelineExecution - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._arguments = None
        self._created_dt = None
        self._end_dt = None
        self._number = None
        self._reason = None
        self._status = None
        self._step_dependencies = None
        self._step_executions = None
        self._triggered_by = None
        self.discriminator = None

        self.arguments = arguments
        self.created_dt = created_dt
        self.end_dt = end_dt
        self.number = number
        if reason is not None:
            self.reason = reason
        self.status = status
        self.step_dependencies = step_dependencies
        self.step_executions = step_executions
        if triggered_by is not None:
            self.triggered_by = triggered_by

    @property
    def arguments(self):
        """Gets the arguments of this ResponsePipelineExecution.  # noqa: E501


        :return: The arguments of this ResponsePipelineExecution.  # noqa: E501
        :rtype: list[ResponsePipelineVariable]
        """
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        """Sets the arguments of this ResponsePipelineExecution.


        :param arguments: The arguments of this ResponsePipelineExecution.  # noqa: E501
        :type arguments: list[ResponsePipelineVariable]
        """
        if self.local_vars_configuration.client_side_validation and arguments is None:  # noqa: E501
            raise ValueError("Invalid value for `arguments`, must not be `None`")  # noqa: E501

        self._arguments = arguments

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponsePipelineExecution.  # noqa: E501


        :return: The created_dt of this ResponsePipelineExecution.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponsePipelineExecution.


        :param created_dt: The created_dt of this ResponsePipelineExecution.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def end_dt(self):
        """Gets the end_dt of this ResponsePipelineExecution.  # noqa: E501


        :return: The end_dt of this ResponsePipelineExecution.  # noqa: E501
        :rtype: datetime
        """
        return self._end_dt

    @end_dt.setter
    def end_dt(self, end_dt):
        """Sets the end_dt of this ResponsePipelineExecution.


        :param end_dt: The end_dt of this ResponsePipelineExecution.  # noqa: E501
        :type end_dt: datetime
        """

        self._end_dt = end_dt

    @property
    def number(self):
        """Gets the number of this ResponsePipelineExecution.  # noqa: E501


        :return: The number of this ResponsePipelineExecution.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this ResponsePipelineExecution.


        :param number: The number of this ResponsePipelineExecution.  # noqa: E501
        :type number: int
        """
        if self.local_vars_configuration.client_side_validation and number is None:  # noqa: E501
            raise ValueError("Invalid value for `number`, must not be `None`")  # noqa: E501

        self._number = number

    @property
    def reason(self):
        """Gets the reason of this ResponsePipelineExecution.  # noqa: E501


        :return: The reason of this ResponsePipelineExecution.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this ResponsePipelineExecution.


        :param reason: The reason of this ResponsePipelineExecution.  # noqa: E501
        :type reason: str
        """

        self._reason = reason

    @property
    def status(self):
        """Gets the status of this ResponsePipelineExecution.  # noqa: E501


        :return: The status of this ResponsePipelineExecution.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResponsePipelineExecution.


        :param status: The status of this ResponsePipelineExecution.  # noqa: E501
        :type status: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def step_dependencies(self):
        """Gets the step_dependencies of this ResponsePipelineExecution.  # noqa: E501


        :return: The step_dependencies of this ResponsePipelineExecution.  # noqa: E501
        :rtype: list[ResponsePipelineStepDependency]
        """
        return self._step_dependencies

    @step_dependencies.setter
    def step_dependencies(self, step_dependencies):
        """Sets the step_dependencies of this ResponsePipelineExecution.


        :param step_dependencies: The step_dependencies of this ResponsePipelineExecution.  # noqa: E501
        :type step_dependencies: list[ResponsePipelineStepDependency]
        """
        if self.local_vars_configuration.client_side_validation and step_dependencies is None:  # noqa: E501
            raise ValueError("Invalid value for `step_dependencies`, must not be `None`")  # noqa: E501

        self._step_dependencies = step_dependencies

    @property
    def step_executions(self):
        """Gets the step_executions of this ResponsePipelineExecution.  # noqa: E501


        :return: The step_executions of this ResponsePipelineExecution.  # noqa: E501
        :rtype: list[ResponseReducedPipelineStepExecution]
        """
        return self._step_executions

    @step_executions.setter
    def step_executions(self, step_executions):
        """Sets the step_executions of this ResponsePipelineExecution.


        :param step_executions: The step_executions of this ResponsePipelineExecution.  # noqa: E501
        :type step_executions: list[ResponseReducedPipelineStepExecution]
        """
        if self.local_vars_configuration.client_side_validation and step_executions is None:  # noqa: E501
            raise ValueError("Invalid value for `step_executions`, must not be `None`")  # noqa: E501

        self._step_executions = step_executions

    @property
    def triggered_by(self):
        """Gets the triggered_by of this ResponsePipelineExecution.  # noqa: E501


        :return: The triggered_by of this ResponsePipelineExecution.  # noqa: E501
        :rtype: ResponseUser
        """
        return self._triggered_by

    @triggered_by.setter
    def triggered_by(self, triggered_by):
        """Sets the triggered_by of this ResponsePipelineExecution.


        :param triggered_by: The triggered_by of this ResponsePipelineExecution.  # noqa: E501
        :type triggered_by: ResponseUser
        """

        self._triggered_by = triggered_by

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
        if not isinstance(other, ResponsePipelineExecution):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponsePipelineExecution):
            return True

        return self.to_dict() != other.to_dict()
