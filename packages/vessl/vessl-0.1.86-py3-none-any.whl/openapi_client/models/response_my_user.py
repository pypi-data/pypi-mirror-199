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


class ResponseMyUser(object):
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
        'default_organization': 'ResponseOrganization',
        'display_name': 'str',
        'email': 'str',
        'git_ssh_key_name': 'str',
        'github_username': 'str',
        'has_password': 'bool',
        'id': 'int',
        'is_email_verified': 'bool',
        'is_pending': 'bool',
        'is_superuser': 'bool',
        'last_login': 'datetime',
        'notification_config': 'dict[str, bool]',
        'organizations': 'list[ResponseOrganization]',
        'updated_dt': 'datetime',
        'username': 'str'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'default_organization': 'default_organization',
        'display_name': 'display_name',
        'email': 'email',
        'git_ssh_key_name': 'git_ssh_key_name',
        'github_username': 'github_username',
        'has_password': 'has_password',
        'id': 'id',
        'is_email_verified': 'is_email_verified',
        'is_pending': 'is_pending',
        'is_superuser': 'is_superuser',
        'last_login': 'last_login',
        'notification_config': 'notification_config',
        'organizations': 'organizations',
        'updated_dt': 'updated_dt',
        'username': 'username'
    }

    def __init__(self, created_dt=None, default_organization=None, display_name=None, email=None, git_ssh_key_name=None, github_username=None, has_password=None, id=None, is_email_verified=None, is_pending=None, is_superuser=None, last_login=None, notification_config=None, organizations=None, updated_dt=None, username=None, local_vars_configuration=None):  # noqa: E501
        """ResponseMyUser - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._default_organization = None
        self._display_name = None
        self._email = None
        self._git_ssh_key_name = None
        self._github_username = None
        self._has_password = None
        self._id = None
        self._is_email_verified = None
        self._is_pending = None
        self._is_superuser = None
        self._last_login = None
        self._notification_config = None
        self._organizations = None
        self._updated_dt = None
        self._username = None
        self.discriminator = None

        self.created_dt = created_dt
        self.default_organization = default_organization
        self.display_name = display_name
        self.email = email
        self.git_ssh_key_name = git_ssh_key_name
        self.github_username = github_username
        self.has_password = has_password
        self.id = id
        self.is_email_verified = is_email_verified
        self.is_pending = is_pending
        self.is_superuser = is_superuser
        self.last_login = last_login
        self.notification_config = notification_config
        self.organizations = organizations
        self.updated_dt = updated_dt
        self.username = username

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseMyUser.  # noqa: E501


        :return: The created_dt of this ResponseMyUser.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseMyUser.


        :param created_dt: The created_dt of this ResponseMyUser.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def default_organization(self):
        """Gets the default_organization of this ResponseMyUser.  # noqa: E501


        :return: The default_organization of this ResponseMyUser.  # noqa: E501
        :rtype: ResponseOrganization
        """
        return self._default_organization

    @default_organization.setter
    def default_organization(self, default_organization):
        """Sets the default_organization of this ResponseMyUser.


        :param default_organization: The default_organization of this ResponseMyUser.  # noqa: E501
        :type default_organization: ResponseOrganization
        """
        if self.local_vars_configuration.client_side_validation and default_organization is None:  # noqa: E501
            raise ValueError("Invalid value for `default_organization`, must not be `None`")  # noqa: E501

        self._default_organization = default_organization

    @property
    def display_name(self):
        """Gets the display_name of this ResponseMyUser.  # noqa: E501


        :return: The display_name of this ResponseMyUser.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ResponseMyUser.


        :param display_name: The display_name of this ResponseMyUser.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def email(self):
        """Gets the email of this ResponseMyUser.  # noqa: E501


        :return: The email of this ResponseMyUser.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ResponseMyUser.


        :param email: The email of this ResponseMyUser.  # noqa: E501
        :type email: str
        """
        if self.local_vars_configuration.client_side_validation and email is None:  # noqa: E501
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def git_ssh_key_name(self):
        """Gets the git_ssh_key_name of this ResponseMyUser.  # noqa: E501


        :return: The git_ssh_key_name of this ResponseMyUser.  # noqa: E501
        :rtype: str
        """
        return self._git_ssh_key_name

    @git_ssh_key_name.setter
    def git_ssh_key_name(self, git_ssh_key_name):
        """Sets the git_ssh_key_name of this ResponseMyUser.


        :param git_ssh_key_name: The git_ssh_key_name of this ResponseMyUser.  # noqa: E501
        :type git_ssh_key_name: str
        """

        self._git_ssh_key_name = git_ssh_key_name

    @property
    def github_username(self):
        """Gets the github_username of this ResponseMyUser.  # noqa: E501


        :return: The github_username of this ResponseMyUser.  # noqa: E501
        :rtype: str
        """
        return self._github_username

    @github_username.setter
    def github_username(self, github_username):
        """Sets the github_username of this ResponseMyUser.


        :param github_username: The github_username of this ResponseMyUser.  # noqa: E501
        :type github_username: str
        """

        self._github_username = github_username

    @property
    def has_password(self):
        """Gets the has_password of this ResponseMyUser.  # noqa: E501


        :return: The has_password of this ResponseMyUser.  # noqa: E501
        :rtype: bool
        """
        return self._has_password

    @has_password.setter
    def has_password(self, has_password):
        """Sets the has_password of this ResponseMyUser.


        :param has_password: The has_password of this ResponseMyUser.  # noqa: E501
        :type has_password: bool
        """
        if self.local_vars_configuration.client_side_validation and has_password is None:  # noqa: E501
            raise ValueError("Invalid value for `has_password`, must not be `None`")  # noqa: E501

        self._has_password = has_password

    @property
    def id(self):
        """Gets the id of this ResponseMyUser.  # noqa: E501


        :return: The id of this ResponseMyUser.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseMyUser.


        :param id: The id of this ResponseMyUser.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def is_email_verified(self):
        """Gets the is_email_verified of this ResponseMyUser.  # noqa: E501


        :return: The is_email_verified of this ResponseMyUser.  # noqa: E501
        :rtype: bool
        """
        return self._is_email_verified

    @is_email_verified.setter
    def is_email_verified(self, is_email_verified):
        """Sets the is_email_verified of this ResponseMyUser.


        :param is_email_verified: The is_email_verified of this ResponseMyUser.  # noqa: E501
        :type is_email_verified: bool
        """
        if self.local_vars_configuration.client_side_validation and is_email_verified is None:  # noqa: E501
            raise ValueError("Invalid value for `is_email_verified`, must not be `None`")  # noqa: E501

        self._is_email_verified = is_email_verified

    @property
    def is_pending(self):
        """Gets the is_pending of this ResponseMyUser.  # noqa: E501


        :return: The is_pending of this ResponseMyUser.  # noqa: E501
        :rtype: bool
        """
        return self._is_pending

    @is_pending.setter
    def is_pending(self, is_pending):
        """Sets the is_pending of this ResponseMyUser.


        :param is_pending: The is_pending of this ResponseMyUser.  # noqa: E501
        :type is_pending: bool
        """
        if self.local_vars_configuration.client_side_validation and is_pending is None:  # noqa: E501
            raise ValueError("Invalid value for `is_pending`, must not be `None`")  # noqa: E501

        self._is_pending = is_pending

    @property
    def is_superuser(self):
        """Gets the is_superuser of this ResponseMyUser.  # noqa: E501


        :return: The is_superuser of this ResponseMyUser.  # noqa: E501
        :rtype: bool
        """
        return self._is_superuser

    @is_superuser.setter
    def is_superuser(self, is_superuser):
        """Sets the is_superuser of this ResponseMyUser.


        :param is_superuser: The is_superuser of this ResponseMyUser.  # noqa: E501
        :type is_superuser: bool
        """
        if self.local_vars_configuration.client_side_validation and is_superuser is None:  # noqa: E501
            raise ValueError("Invalid value for `is_superuser`, must not be `None`")  # noqa: E501

        self._is_superuser = is_superuser

    @property
    def last_login(self):
        """Gets the last_login of this ResponseMyUser.  # noqa: E501


        :return: The last_login of this ResponseMyUser.  # noqa: E501
        :rtype: datetime
        """
        return self._last_login

    @last_login.setter
    def last_login(self, last_login):
        """Sets the last_login of this ResponseMyUser.


        :param last_login: The last_login of this ResponseMyUser.  # noqa: E501
        :type last_login: datetime
        """

        self._last_login = last_login

    @property
    def notification_config(self):
        """Gets the notification_config of this ResponseMyUser.  # noqa: E501


        :return: The notification_config of this ResponseMyUser.  # noqa: E501
        :rtype: dict[str, bool]
        """
        return self._notification_config

    @notification_config.setter
    def notification_config(self, notification_config):
        """Sets the notification_config of this ResponseMyUser.


        :param notification_config: The notification_config of this ResponseMyUser.  # noqa: E501
        :type notification_config: dict[str, bool]
        """
        if self.local_vars_configuration.client_side_validation and notification_config is None:  # noqa: E501
            raise ValueError("Invalid value for `notification_config`, must not be `None`")  # noqa: E501

        self._notification_config = notification_config

    @property
    def organizations(self):
        """Gets the organizations of this ResponseMyUser.  # noqa: E501


        :return: The organizations of this ResponseMyUser.  # noqa: E501
        :rtype: list[ResponseOrganization]
        """
        return self._organizations

    @organizations.setter
    def organizations(self, organizations):
        """Sets the organizations of this ResponseMyUser.


        :param organizations: The organizations of this ResponseMyUser.  # noqa: E501
        :type organizations: list[ResponseOrganization]
        """
        if self.local_vars_configuration.client_side_validation and organizations is None:  # noqa: E501
            raise ValueError("Invalid value for `organizations`, must not be `None`")  # noqa: E501

        self._organizations = organizations

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseMyUser.  # noqa: E501


        :return: The updated_dt of this ResponseMyUser.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseMyUser.


        :param updated_dt: The updated_dt of this ResponseMyUser.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

        self._updated_dt = updated_dt

    @property
    def username(self):
        """Gets the username of this ResponseMyUser.  # noqa: E501


        :return: The username of this ResponseMyUser.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this ResponseMyUser.


        :param username: The username of this ResponseMyUser.  # noqa: E501
        :type username: str
        """
        if self.local_vars_configuration.client_side_validation and username is None:  # noqa: E501
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

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
        if not isinstance(other, ResponseMyUser):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseMyUser):
            return True

        return self.to_dict() != other.to_dict()
