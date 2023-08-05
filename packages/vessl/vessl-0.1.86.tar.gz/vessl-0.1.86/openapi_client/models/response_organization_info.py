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


class ResponseOrganizationInfo(object):
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
        'access_control_config': 'OrmAccessControlConfig',
        'auto_top_up_charge_amount': 'float',
        'auto_top_up_enabled': 'bool',
        'auto_top_up_trigger_amount': 'float',
        'aws_external_id': 'str',
        'created_dt': 'datetime',
        'credit_balance': 'float',
        'description': 'str',
        'display_name': 'str',
        'id': 'int',
        'name': 'str',
        'owner_id': 'int',
        'pricing_plan': 'ResponsePricingPlan',
        'primary_owner_id': 'int',
        'show_tutorial': 'bool',
        'stripe_customer_id': 'str',
        'stripe_subscription_id': 'str',
        'tutorials': 'list[ResponseTutorialResponse]',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'access_control_config': 'access_control_config',
        'auto_top_up_charge_amount': 'auto_top_up_charge_amount',
        'auto_top_up_enabled': 'auto_top_up_enabled',
        'auto_top_up_trigger_amount': 'auto_top_up_trigger_amount',
        'aws_external_id': 'aws_external_id',
        'created_dt': 'created_dt',
        'credit_balance': 'credit_balance',
        'description': 'description',
        'display_name': 'display_name',
        'id': 'id',
        'name': 'name',
        'owner_id': 'owner_id',
        'pricing_plan': 'pricing_plan',
        'primary_owner_id': 'primary_owner_id',
        'show_tutorial': 'show_tutorial',
        'stripe_customer_id': 'stripe_customer_id',
        'stripe_subscription_id': 'stripe_subscription_id',
        'tutorials': 'tutorials',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, access_control_config=None, auto_top_up_charge_amount=None, auto_top_up_enabled=None, auto_top_up_trigger_amount=None, aws_external_id=None, created_dt=None, credit_balance=None, description=None, display_name=None, id=None, name=None, owner_id=None, pricing_plan=None, primary_owner_id=None, show_tutorial=None, stripe_customer_id=None, stripe_subscription_id=None, tutorials=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ResponseOrganizationInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._access_control_config = None
        self._auto_top_up_charge_amount = None
        self._auto_top_up_enabled = None
        self._auto_top_up_trigger_amount = None
        self._aws_external_id = None
        self._created_dt = None
        self._credit_balance = None
        self._description = None
        self._display_name = None
        self._id = None
        self._name = None
        self._owner_id = None
        self._pricing_plan = None
        self._primary_owner_id = None
        self._show_tutorial = None
        self._stripe_customer_id = None
        self._stripe_subscription_id = None
        self._tutorials = None
        self._updated_dt = None
        self.discriminator = None

        self.access_control_config = access_control_config
        self.auto_top_up_charge_amount = auto_top_up_charge_amount
        self.auto_top_up_enabled = auto_top_up_enabled
        self.auto_top_up_trigger_amount = auto_top_up_trigger_amount
        self.aws_external_id = aws_external_id
        self.created_dt = created_dt
        self.credit_balance = credit_balance
        self.description = description
        self.display_name = display_name
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.pricing_plan = pricing_plan
        self.primary_owner_id = primary_owner_id
        self.show_tutorial = show_tutorial
        self.stripe_customer_id = stripe_customer_id
        self.stripe_subscription_id = stripe_subscription_id
        self.tutorials = tutorials
        self.updated_dt = updated_dt

    @property
    def access_control_config(self):
        """Gets the access_control_config of this ResponseOrganizationInfo.  # noqa: E501


        :return: The access_control_config of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: OrmAccessControlConfig
        """
        return self._access_control_config

    @access_control_config.setter
    def access_control_config(self, access_control_config):
        """Sets the access_control_config of this ResponseOrganizationInfo.


        :param access_control_config: The access_control_config of this ResponseOrganizationInfo.  # noqa: E501
        :type access_control_config: OrmAccessControlConfig
        """
        if self.local_vars_configuration.client_side_validation and access_control_config is None:  # noqa: E501
            raise ValueError("Invalid value for `access_control_config`, must not be `None`")  # noqa: E501

        self._access_control_config = access_control_config

    @property
    def auto_top_up_charge_amount(self):
        """Gets the auto_top_up_charge_amount of this ResponseOrganizationInfo.  # noqa: E501


        :return: The auto_top_up_charge_amount of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: float
        """
        return self._auto_top_up_charge_amount

    @auto_top_up_charge_amount.setter
    def auto_top_up_charge_amount(self, auto_top_up_charge_amount):
        """Sets the auto_top_up_charge_amount of this ResponseOrganizationInfo.


        :param auto_top_up_charge_amount: The auto_top_up_charge_amount of this ResponseOrganizationInfo.  # noqa: E501
        :type auto_top_up_charge_amount: float
        """
        if self.local_vars_configuration.client_side_validation and auto_top_up_charge_amount is None:  # noqa: E501
            raise ValueError("Invalid value for `auto_top_up_charge_amount`, must not be `None`")  # noqa: E501

        self._auto_top_up_charge_amount = auto_top_up_charge_amount

    @property
    def auto_top_up_enabled(self):
        """Gets the auto_top_up_enabled of this ResponseOrganizationInfo.  # noqa: E501


        :return: The auto_top_up_enabled of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: bool
        """
        return self._auto_top_up_enabled

    @auto_top_up_enabled.setter
    def auto_top_up_enabled(self, auto_top_up_enabled):
        """Sets the auto_top_up_enabled of this ResponseOrganizationInfo.


        :param auto_top_up_enabled: The auto_top_up_enabled of this ResponseOrganizationInfo.  # noqa: E501
        :type auto_top_up_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and auto_top_up_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `auto_top_up_enabled`, must not be `None`")  # noqa: E501

        self._auto_top_up_enabled = auto_top_up_enabled

    @property
    def auto_top_up_trigger_amount(self):
        """Gets the auto_top_up_trigger_amount of this ResponseOrganizationInfo.  # noqa: E501


        :return: The auto_top_up_trigger_amount of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: float
        """
        return self._auto_top_up_trigger_amount

    @auto_top_up_trigger_amount.setter
    def auto_top_up_trigger_amount(self, auto_top_up_trigger_amount):
        """Sets the auto_top_up_trigger_amount of this ResponseOrganizationInfo.


        :param auto_top_up_trigger_amount: The auto_top_up_trigger_amount of this ResponseOrganizationInfo.  # noqa: E501
        :type auto_top_up_trigger_amount: float
        """
        if self.local_vars_configuration.client_side_validation and auto_top_up_trigger_amount is None:  # noqa: E501
            raise ValueError("Invalid value for `auto_top_up_trigger_amount`, must not be `None`")  # noqa: E501

        self._auto_top_up_trigger_amount = auto_top_up_trigger_amount

    @property
    def aws_external_id(self):
        """Gets the aws_external_id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The aws_external_id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._aws_external_id

    @aws_external_id.setter
    def aws_external_id(self, aws_external_id):
        """Sets the aws_external_id of this ResponseOrganizationInfo.


        :param aws_external_id: The aws_external_id of this ResponseOrganizationInfo.  # noqa: E501
        :type aws_external_id: str
        """
        if self.local_vars_configuration.client_side_validation and aws_external_id is None:  # noqa: E501
            raise ValueError("Invalid value for `aws_external_id`, must not be `None`")  # noqa: E501

        self._aws_external_id = aws_external_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseOrganizationInfo.  # noqa: E501


        :return: The created_dt of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseOrganizationInfo.


        :param created_dt: The created_dt of this ResponseOrganizationInfo.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def credit_balance(self):
        """Gets the credit_balance of this ResponseOrganizationInfo.  # noqa: E501


        :return: The credit_balance of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: float
        """
        return self._credit_balance

    @credit_balance.setter
    def credit_balance(self, credit_balance):
        """Sets the credit_balance of this ResponseOrganizationInfo.


        :param credit_balance: The credit_balance of this ResponseOrganizationInfo.  # noqa: E501
        :type credit_balance: float
        """
        if self.local_vars_configuration.client_side_validation and credit_balance is None:  # noqa: E501
            raise ValueError("Invalid value for `credit_balance`, must not be `None`")  # noqa: E501

        self._credit_balance = credit_balance

    @property
    def description(self):
        """Gets the description of this ResponseOrganizationInfo.  # noqa: E501


        :return: The description of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseOrganizationInfo.


        :param description: The description of this ResponseOrganizationInfo.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this ResponseOrganizationInfo.  # noqa: E501


        :return: The display_name of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ResponseOrganizationInfo.


        :param display_name: The display_name of this ResponseOrganizationInfo.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def id(self):
        """Gets the id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseOrganizationInfo.


        :param id: The id of this ResponseOrganizationInfo.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this ResponseOrganizationInfo.  # noqa: E501


        :return: The name of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseOrganizationInfo.


        :param name: The name of this ResponseOrganizationInfo.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def owner_id(self):
        """Gets the owner_id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The owner_id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: int
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """Sets the owner_id of this ResponseOrganizationInfo.


        :param owner_id: The owner_id of this ResponseOrganizationInfo.  # noqa: E501
        :type owner_id: int
        """

        self._owner_id = owner_id

    @property
    def pricing_plan(self):
        """Gets the pricing_plan of this ResponseOrganizationInfo.  # noqa: E501


        :return: The pricing_plan of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: ResponsePricingPlan
        """
        return self._pricing_plan

    @pricing_plan.setter
    def pricing_plan(self, pricing_plan):
        """Sets the pricing_plan of this ResponseOrganizationInfo.


        :param pricing_plan: The pricing_plan of this ResponseOrganizationInfo.  # noqa: E501
        :type pricing_plan: ResponsePricingPlan
        """
        if self.local_vars_configuration.client_side_validation and pricing_plan is None:  # noqa: E501
            raise ValueError("Invalid value for `pricing_plan`, must not be `None`")  # noqa: E501

        self._pricing_plan = pricing_plan

    @property
    def primary_owner_id(self):
        """Gets the primary_owner_id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The primary_owner_id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: int
        """
        return self._primary_owner_id

    @primary_owner_id.setter
    def primary_owner_id(self, primary_owner_id):
        """Sets the primary_owner_id of this ResponseOrganizationInfo.


        :param primary_owner_id: The primary_owner_id of this ResponseOrganizationInfo.  # noqa: E501
        :type primary_owner_id: int
        """
        if self.local_vars_configuration.client_side_validation and primary_owner_id is None:  # noqa: E501
            raise ValueError("Invalid value for `primary_owner_id`, must not be `None`")  # noqa: E501

        self._primary_owner_id = primary_owner_id

    @property
    def show_tutorial(self):
        """Gets the show_tutorial of this ResponseOrganizationInfo.  # noqa: E501


        :return: The show_tutorial of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: bool
        """
        return self._show_tutorial

    @show_tutorial.setter
    def show_tutorial(self, show_tutorial):
        """Sets the show_tutorial of this ResponseOrganizationInfo.


        :param show_tutorial: The show_tutorial of this ResponseOrganizationInfo.  # noqa: E501
        :type show_tutorial: bool
        """
        if self.local_vars_configuration.client_side_validation and show_tutorial is None:  # noqa: E501
            raise ValueError("Invalid value for `show_tutorial`, must not be `None`")  # noqa: E501

        self._show_tutorial = show_tutorial

    @property
    def stripe_customer_id(self):
        """Gets the stripe_customer_id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The stripe_customer_id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._stripe_customer_id

    @stripe_customer_id.setter
    def stripe_customer_id(self, stripe_customer_id):
        """Sets the stripe_customer_id of this ResponseOrganizationInfo.


        :param stripe_customer_id: The stripe_customer_id of this ResponseOrganizationInfo.  # noqa: E501
        :type stripe_customer_id: str
        """

        self._stripe_customer_id = stripe_customer_id

    @property
    def stripe_subscription_id(self):
        """Gets the stripe_subscription_id of this ResponseOrganizationInfo.  # noqa: E501


        :return: The stripe_subscription_id of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: str
        """
        return self._stripe_subscription_id

    @stripe_subscription_id.setter
    def stripe_subscription_id(self, stripe_subscription_id):
        """Sets the stripe_subscription_id of this ResponseOrganizationInfo.


        :param stripe_subscription_id: The stripe_subscription_id of this ResponseOrganizationInfo.  # noqa: E501
        :type stripe_subscription_id: str
        """

        self._stripe_subscription_id = stripe_subscription_id

    @property
    def tutorials(self):
        """Gets the tutorials of this ResponseOrganizationInfo.  # noqa: E501


        :return: The tutorials of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: list[ResponseTutorialResponse]
        """
        return self._tutorials

    @tutorials.setter
    def tutorials(self, tutorials):
        """Sets the tutorials of this ResponseOrganizationInfo.


        :param tutorials: The tutorials of this ResponseOrganizationInfo.  # noqa: E501
        :type tutorials: list[ResponseTutorialResponse]
        """
        if self.local_vars_configuration.client_side_validation and tutorials is None:  # noqa: E501
            raise ValueError("Invalid value for `tutorials`, must not be `None`")  # noqa: E501

        self._tutorials = tutorials

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseOrganizationInfo.  # noqa: E501


        :return: The updated_dt of this ResponseOrganizationInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseOrganizationInfo.


        :param updated_dt: The updated_dt of this ResponseOrganizationInfo.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

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
        if not isinstance(other, ResponseOrganizationInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseOrganizationInfo):
            return True

        return self.to_dict() != other.to_dict()
