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


class OrmKernelClusterEdges(object):
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
        'cluster_quotas': 'list[OrmClusterQuota]',
        'default_storage': 'OrmStorage',
        'kernel_cluster_nodes': 'list[OrmKernelClusterNode]',
        'kernel_cluster_storages': 'list[OrmKernelClusterStorage]',
        'kernel_cluster_workloads': 'list[OrmWorkload]',
        'kernel_resource_specs': 'list[OrmKernelResourceSpec]',
        'model_services': 'list[OrmModelService]',
        'organization_kernel_clusters': 'list[OrmOrganizationKernelCluster]',
        'pipeline_step_jupyter_visualization_specs': 'list[OrmPipelineStepJupyterVisualization]',
        'pipeline_step_run_specs': 'list[OrmPipelineStepRun]',
        'primary_owner': 'OrmOrganization',
        'region': 'OrmRegion'
    }

    attribute_map = {
        'cluster_quotas': 'cluster_quotas',
        'default_storage': 'default_storage',
        'kernel_cluster_nodes': 'kernel_cluster_nodes',
        'kernel_cluster_storages': 'kernel_cluster_storages',
        'kernel_cluster_workloads': 'kernel_cluster_workloads',
        'kernel_resource_specs': 'kernel_resource_specs',
        'model_services': 'model_services',
        'organization_kernel_clusters': 'organization_kernel_clusters',
        'pipeline_step_jupyter_visualization_specs': 'pipeline_step_jupyter_visualization_specs',
        'pipeline_step_run_specs': 'pipeline_step_run_specs',
        'primary_owner': 'primary_owner',
        'region': 'region'
    }

    def __init__(self, cluster_quotas=None, default_storage=None, kernel_cluster_nodes=None, kernel_cluster_storages=None, kernel_cluster_workloads=None, kernel_resource_specs=None, model_services=None, organization_kernel_clusters=None, pipeline_step_jupyter_visualization_specs=None, pipeline_step_run_specs=None, primary_owner=None, region=None, local_vars_configuration=None):  # noqa: E501
        """OrmKernelClusterEdges - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cluster_quotas = None
        self._default_storage = None
        self._kernel_cluster_nodes = None
        self._kernel_cluster_storages = None
        self._kernel_cluster_workloads = None
        self._kernel_resource_specs = None
        self._model_services = None
        self._organization_kernel_clusters = None
        self._pipeline_step_jupyter_visualization_specs = None
        self._pipeline_step_run_specs = None
        self._primary_owner = None
        self._region = None
        self.discriminator = None

        if cluster_quotas is not None:
            self.cluster_quotas = cluster_quotas
        if default_storage is not None:
            self.default_storage = default_storage
        if kernel_cluster_nodes is not None:
            self.kernel_cluster_nodes = kernel_cluster_nodes
        if kernel_cluster_storages is not None:
            self.kernel_cluster_storages = kernel_cluster_storages
        if kernel_cluster_workloads is not None:
            self.kernel_cluster_workloads = kernel_cluster_workloads
        if kernel_resource_specs is not None:
            self.kernel_resource_specs = kernel_resource_specs
        if model_services is not None:
            self.model_services = model_services
        if organization_kernel_clusters is not None:
            self.organization_kernel_clusters = organization_kernel_clusters
        if pipeline_step_jupyter_visualization_specs is not None:
            self.pipeline_step_jupyter_visualization_specs = pipeline_step_jupyter_visualization_specs
        if pipeline_step_run_specs is not None:
            self.pipeline_step_run_specs = pipeline_step_run_specs
        if primary_owner is not None:
            self.primary_owner = primary_owner
        if region is not None:
            self.region = region

    @property
    def cluster_quotas(self):
        """Gets the cluster_quotas of this OrmKernelClusterEdges.  # noqa: E501


        :return: The cluster_quotas of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmClusterQuota]
        """
        return self._cluster_quotas

    @cluster_quotas.setter
    def cluster_quotas(self, cluster_quotas):
        """Sets the cluster_quotas of this OrmKernelClusterEdges.


        :param cluster_quotas: The cluster_quotas of this OrmKernelClusterEdges.  # noqa: E501
        :type cluster_quotas: list[OrmClusterQuota]
        """

        self._cluster_quotas = cluster_quotas

    @property
    def default_storage(self):
        """Gets the default_storage of this OrmKernelClusterEdges.  # noqa: E501


        :return: The default_storage of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: OrmStorage
        """
        return self._default_storage

    @default_storage.setter
    def default_storage(self, default_storage):
        """Sets the default_storage of this OrmKernelClusterEdges.


        :param default_storage: The default_storage of this OrmKernelClusterEdges.  # noqa: E501
        :type default_storage: OrmStorage
        """

        self._default_storage = default_storage

    @property
    def kernel_cluster_nodes(self):
        """Gets the kernel_cluster_nodes of this OrmKernelClusterEdges.  # noqa: E501


        :return: The kernel_cluster_nodes of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmKernelClusterNode]
        """
        return self._kernel_cluster_nodes

    @kernel_cluster_nodes.setter
    def kernel_cluster_nodes(self, kernel_cluster_nodes):
        """Sets the kernel_cluster_nodes of this OrmKernelClusterEdges.


        :param kernel_cluster_nodes: The kernel_cluster_nodes of this OrmKernelClusterEdges.  # noqa: E501
        :type kernel_cluster_nodes: list[OrmKernelClusterNode]
        """

        self._kernel_cluster_nodes = kernel_cluster_nodes

    @property
    def kernel_cluster_storages(self):
        """Gets the kernel_cluster_storages of this OrmKernelClusterEdges.  # noqa: E501


        :return: The kernel_cluster_storages of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmKernelClusterStorage]
        """
        return self._kernel_cluster_storages

    @kernel_cluster_storages.setter
    def kernel_cluster_storages(self, kernel_cluster_storages):
        """Sets the kernel_cluster_storages of this OrmKernelClusterEdges.


        :param kernel_cluster_storages: The kernel_cluster_storages of this OrmKernelClusterEdges.  # noqa: E501
        :type kernel_cluster_storages: list[OrmKernelClusterStorage]
        """

        self._kernel_cluster_storages = kernel_cluster_storages

    @property
    def kernel_cluster_workloads(self):
        """Gets the kernel_cluster_workloads of this OrmKernelClusterEdges.  # noqa: E501


        :return: The kernel_cluster_workloads of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmWorkload]
        """
        return self._kernel_cluster_workloads

    @kernel_cluster_workloads.setter
    def kernel_cluster_workloads(self, kernel_cluster_workloads):
        """Sets the kernel_cluster_workloads of this OrmKernelClusterEdges.


        :param kernel_cluster_workloads: The kernel_cluster_workloads of this OrmKernelClusterEdges.  # noqa: E501
        :type kernel_cluster_workloads: list[OrmWorkload]
        """

        self._kernel_cluster_workloads = kernel_cluster_workloads

    @property
    def kernel_resource_specs(self):
        """Gets the kernel_resource_specs of this OrmKernelClusterEdges.  # noqa: E501


        :return: The kernel_resource_specs of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmKernelResourceSpec]
        """
        return self._kernel_resource_specs

    @kernel_resource_specs.setter
    def kernel_resource_specs(self, kernel_resource_specs):
        """Sets the kernel_resource_specs of this OrmKernelClusterEdges.


        :param kernel_resource_specs: The kernel_resource_specs of this OrmKernelClusterEdges.  # noqa: E501
        :type kernel_resource_specs: list[OrmKernelResourceSpec]
        """

        self._kernel_resource_specs = kernel_resource_specs

    @property
    def model_services(self):
        """Gets the model_services of this OrmKernelClusterEdges.  # noqa: E501


        :return: The model_services of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmModelService]
        """
        return self._model_services

    @model_services.setter
    def model_services(self, model_services):
        """Sets the model_services of this OrmKernelClusterEdges.


        :param model_services: The model_services of this OrmKernelClusterEdges.  # noqa: E501
        :type model_services: list[OrmModelService]
        """

        self._model_services = model_services

    @property
    def organization_kernel_clusters(self):
        """Gets the organization_kernel_clusters of this OrmKernelClusterEdges.  # noqa: E501


        :return: The organization_kernel_clusters of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmOrganizationKernelCluster]
        """
        return self._organization_kernel_clusters

    @organization_kernel_clusters.setter
    def organization_kernel_clusters(self, organization_kernel_clusters):
        """Sets the organization_kernel_clusters of this OrmKernelClusterEdges.


        :param organization_kernel_clusters: The organization_kernel_clusters of this OrmKernelClusterEdges.  # noqa: E501
        :type organization_kernel_clusters: list[OrmOrganizationKernelCluster]
        """

        self._organization_kernel_clusters = organization_kernel_clusters

    @property
    def pipeline_step_jupyter_visualization_specs(self):
        """Gets the pipeline_step_jupyter_visualization_specs of this OrmKernelClusterEdges.  # noqa: E501


        :return: The pipeline_step_jupyter_visualization_specs of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmPipelineStepJupyterVisualization]
        """
        return self._pipeline_step_jupyter_visualization_specs

    @pipeline_step_jupyter_visualization_specs.setter
    def pipeline_step_jupyter_visualization_specs(self, pipeline_step_jupyter_visualization_specs):
        """Sets the pipeline_step_jupyter_visualization_specs of this OrmKernelClusterEdges.


        :param pipeline_step_jupyter_visualization_specs: The pipeline_step_jupyter_visualization_specs of this OrmKernelClusterEdges.  # noqa: E501
        :type pipeline_step_jupyter_visualization_specs: list[OrmPipelineStepJupyterVisualization]
        """

        self._pipeline_step_jupyter_visualization_specs = pipeline_step_jupyter_visualization_specs

    @property
    def pipeline_step_run_specs(self):
        """Gets the pipeline_step_run_specs of this OrmKernelClusterEdges.  # noqa: E501


        :return: The pipeline_step_run_specs of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: list[OrmPipelineStepRun]
        """
        return self._pipeline_step_run_specs

    @pipeline_step_run_specs.setter
    def pipeline_step_run_specs(self, pipeline_step_run_specs):
        """Sets the pipeline_step_run_specs of this OrmKernelClusterEdges.


        :param pipeline_step_run_specs: The pipeline_step_run_specs of this OrmKernelClusterEdges.  # noqa: E501
        :type pipeline_step_run_specs: list[OrmPipelineStepRun]
        """

        self._pipeline_step_run_specs = pipeline_step_run_specs

    @property
    def primary_owner(self):
        """Gets the primary_owner of this OrmKernelClusterEdges.  # noqa: E501


        :return: The primary_owner of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: OrmOrganization
        """
        return self._primary_owner

    @primary_owner.setter
    def primary_owner(self, primary_owner):
        """Sets the primary_owner of this OrmKernelClusterEdges.


        :param primary_owner: The primary_owner of this OrmKernelClusterEdges.  # noqa: E501
        :type primary_owner: OrmOrganization
        """

        self._primary_owner = primary_owner

    @property
    def region(self):
        """Gets the region of this OrmKernelClusterEdges.  # noqa: E501


        :return: The region of this OrmKernelClusterEdges.  # noqa: E501
        :rtype: OrmRegion
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this OrmKernelClusterEdges.


        :param region: The region of this OrmKernelClusterEdges.  # noqa: E501
        :type region: OrmRegion
        """

        self._region = region

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
        if not isinstance(other, OrmKernelClusterEdges):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmKernelClusterEdges):
            return True

        return self.to_dict() != other.to_dict()
