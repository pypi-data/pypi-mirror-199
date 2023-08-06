'''
# dynatrace-configuration-dashboard

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Configuration::Dashboard` v1.2.0.

## Description

Manage a dashboard in Dynatrace.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Configuration::Dashboard \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Configuration-Dashboard \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Configuration::Dashboard`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-configuration-dashboard+v1.2.0).
* Issues related to `Dynatrace::Configuration::Dashboard` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnDashboard(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.CfnDashboard",
):
    '''A CloudFormation ``Dynatrace::Configuration::Dashboard``.

    :cloudformationResource: Dynatrace::Configuration::Dashboard
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dashboard_metadata: typing.Union["DashboardMetadata", typing.Dict[builtins.str, typing.Any]],
        tiles: typing.Sequence[typing.Union["Tile", typing.Dict[builtins.str, typing.Any]]],
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Configuration::Dashboard``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param dashboard_metadata: 
        :param tiles: 
        :param id: 
        :param metadata: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0964e762f980dc78d1de0a534724856042948296efa48f2fa99d6e01aa7b1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnDashboardProps(
            dashboard_metadata=dashboard_metadata,
            tiles=tiles,
            id=id,
            metadata=metadata,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDashboardProps":
        '''Resource props.'''
        return typing.cast("CfnDashboardProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.CfnDashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_metadata": "dashboardMetadata",
        "tiles": "tiles",
        "id": "id",
        "metadata": "metadata",
    },
)
class CfnDashboardProps:
    def __init__(
        self,
        *,
        dashboard_metadata: typing.Union["DashboardMetadata", typing.Dict[builtins.str, typing.Any]],
        tiles: typing.Sequence[typing.Union["Tile", typing.Dict[builtins.str, typing.Any]]],
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Manage a dashboard in Dynatrace.

        :param dashboard_metadata: 
        :param tiles: 
        :param id: 
        :param metadata: 

        :schema: CfnDashboardProps
        '''
        if isinstance(dashboard_metadata, dict):
            dashboard_metadata = DashboardMetadata(**dashboard_metadata)
        if isinstance(metadata, dict):
            metadata = Metadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69e9fff09099c79080a15af576cd3e6f746837d40ba8ff416c2fa46db0b6934)
            check_type(argname="argument dashboard_metadata", value=dashboard_metadata, expected_type=type_hints["dashboard_metadata"])
            check_type(argname="argument tiles", value=tiles, expected_type=type_hints["tiles"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dashboard_metadata": dashboard_metadata,
            "tiles": tiles,
        }
        if id is not None:
            self._values["id"] = id
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def dashboard_metadata(self) -> "DashboardMetadata":
        '''
        :schema: CfnDashboardProps#DashboardMetadata
        '''
        result = self._values.get("dashboard_metadata")
        assert result is not None, "Required property 'dashboard_metadata' is missing"
        return typing.cast("DashboardMetadata", result)

    @builtins.property
    def tiles(self) -> typing.List["Tile"]:
        '''
        :schema: CfnDashboardProps#Tiles
        '''
        result = self._values.get("tiles")
        assert result is not None, "Required property 'tiles' is missing"
        return typing.cast(typing.List["Tile"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDashboardProps#Id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional["Metadata"]:
        '''
        :schema: CfnDashboardProps#Metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["Metadata"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.DashboardFilter",
    jsii_struct_bases=[],
    name_mapping={"management_zone": "managementZone", "timeframe": "timeframe"},
)
class DashboardFilter:
    def __init__(
        self,
        *,
        management_zone: typing.Optional[typing.Union["EntityShortRepresentation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeframe: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Filters, applied to a dashboard.

        :param management_zone: 
        :param timeframe: The default timeframe of the dashboard.

        :schema: DashboardFilter
        '''
        if isinstance(management_zone, dict):
            management_zone = EntityShortRepresentation(**management_zone)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71409840f249ddc420ef1a0a8c4f31a1cc198a38c4e9641e86776cd1e36a7bdd)
            check_type(argname="argument management_zone", value=management_zone, expected_type=type_hints["management_zone"])
            check_type(argname="argument timeframe", value=timeframe, expected_type=type_hints["timeframe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if management_zone is not None:
            self._values["management_zone"] = management_zone
        if timeframe is not None:
            self._values["timeframe"] = timeframe

    @builtins.property
    def management_zone(self) -> typing.Optional["EntityShortRepresentation"]:
        '''
        :schema: DashboardFilter#ManagementZone
        '''
        result = self._values.get("management_zone")
        return typing.cast(typing.Optional["EntityShortRepresentation"], result)

    @builtins.property
    def timeframe(self) -> typing.Optional[builtins.str]:
        '''The default timeframe of the dashboard.

        :schema: DashboardFilter#Timeframe
        '''
        result = self._values.get("timeframe")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.DashboardMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "owner": "owner",
        "dashboard_filter": "dashboardFilter",
        "dynamic_filters": "dynamicFilters",
        "preset": "preset",
        "shared": "shared",
        "tags": "tags",
        "tiles_name_size": "tilesNameSize",
    },
)
class DashboardMetadata:
    def __init__(
        self,
        *,
        name: builtins.str,
        owner: builtins.str,
        dashboard_filter: typing.Optional[typing.Union[DashboardFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        dynamic_filters: typing.Optional[typing.Union["DynamicFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        preset: typing.Optional[builtins.bool] = None,
        shared: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        tiles_name_size: typing.Optional["DashboardMetadataTilesNameSize"] = None,
    ) -> None:
        '''Parameters of a dashboard.

        :param name: The name of the dashboard.
        :param owner: The owner of the dashboard.
        :param dashboard_filter: 
        :param dynamic_filters: 
        :param preset: The dashboard is a preset (true) or a custom (false) dashboard.
        :param shared: The dashboard is shared (true) or private (false).
        :param tags: A set of tags assigned to the dashboard.
        :param tiles_name_size: The general size of the tiles tile. Default value is medium

        :schema: DashboardMetadata
        '''
        if isinstance(dashboard_filter, dict):
            dashboard_filter = DashboardFilter(**dashboard_filter)
        if isinstance(dynamic_filters, dict):
            dynamic_filters = DynamicFilters(**dynamic_filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19f431d58134bf0a371f5d2486e08612fab69482dc9c942192a547c51643aa6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument dashboard_filter", value=dashboard_filter, expected_type=type_hints["dashboard_filter"])
            check_type(argname="argument dynamic_filters", value=dynamic_filters, expected_type=type_hints["dynamic_filters"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tiles_name_size", value=tiles_name_size, expected_type=type_hints["tiles_name_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "owner": owner,
        }
        if dashboard_filter is not None:
            self._values["dashboard_filter"] = dashboard_filter
        if dynamic_filters is not None:
            self._values["dynamic_filters"] = dynamic_filters
        if preset is not None:
            self._values["preset"] = preset
        if shared is not None:
            self._values["shared"] = shared
        if tags is not None:
            self._values["tags"] = tags
        if tiles_name_size is not None:
            self._values["tiles_name_size"] = tiles_name_size

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the dashboard.

        :schema: DashboardMetadata#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''The owner of the dashboard.

        :schema: DashboardMetadata#Owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashboard_filter(self) -> typing.Optional[DashboardFilter]:
        '''
        :schema: DashboardMetadata#DashboardFilter
        '''
        result = self._values.get("dashboard_filter")
        return typing.cast(typing.Optional[DashboardFilter], result)

    @builtins.property
    def dynamic_filters(self) -> typing.Optional["DynamicFilters"]:
        '''
        :schema: DashboardMetadata#DynamicFilters
        '''
        result = self._values.get("dynamic_filters")
        return typing.cast(typing.Optional["DynamicFilters"], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.bool]:
        '''The dashboard is a preset (true) or a custom (false) dashboard.

        :schema: DashboardMetadata#Preset
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def shared(self) -> typing.Optional[builtins.bool]:
        '''The dashboard is shared (true) or private (false).

        :schema: DashboardMetadata#Shared
        '''
        result = self._values.get("shared")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of tags assigned to the dashboard.

        :schema: DashboardMetadata#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tiles_name_size(self) -> typing.Optional["DashboardMetadataTilesNameSize"]:
        '''The general size of the tiles tile.

        Default value is medium

        :schema: DashboardMetadata#TilesNameSize
        '''
        result = self._values.get("tiles_name_size")
        return typing.cast(typing.Optional["DashboardMetadataTilesNameSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.DashboardMetadataTilesNameSize"
)
class DashboardMetadataTilesNameSize(enum.Enum):
    '''The general size of the tiles tile.

    Default value is medium

    :schema: DashboardMetadataTilesNameSize
    '''

    SMALL = "SMALL"
    '''small.'''
    MEDIUM = "MEDIUM"
    '''medium.'''
    LARGE = "LARGE"
    '''large.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.DynamicFilters",
    jsii_struct_bases=[],
    name_mapping={"filters": "filters"},
)
class DynamicFilters:
    def __init__(self, *, filters: typing.Sequence[builtins.str]) -> None:
        '''Dashboard filter configuration of a dashboard.

        :param filters: A set of all possible global dashboard filters that can be applied to a dashboard.

        :schema: DynamicFilters
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb85bdd9c5b0ca6cae02fd65d6e4fc23f0c54df2bec85778b3595d0528e9486b)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filters": filters,
        }

    @builtins.property
    def filters(self) -> typing.List[builtins.str]:
        '''A set of all possible global dashboard filters that can be applied to a dashboard.

        :schema: DynamicFilters#Filters
        '''
        result = self._values.get("filters")
        assert result is not None, "Required property 'filters' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamicFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.EntityShortRepresentation",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class EntityShortRepresentation:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The short representation of a Dynatrace entity.

        :param id: The ID of the Dynatrace entity.
        :param name: The name of the Dynatrace entity.

        :schema: EntityShortRepresentation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c470570980515efc639534c1aec9e522bd86df86b91208522c79e9fc134a08db)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Dynatrace entity.

        :schema: EntityShortRepresentation#Id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Dynatrace entity.

        :schema: EntityShortRepresentation#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EntityShortRepresentation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_version": "clusterVersion",
        "configuration_versions": "configurationVersions",
    },
)
class Metadata:
    def __init__(
        self,
        *,
        cluster_version: typing.Optional[builtins.str] = None,
        configuration_versions: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''Metadata useful for debugging.

        :param cluster_version: Dynatrace version.
        :param configuration_versions: A sorted list of the version numbers of the configuration.

        :schema: Metadata
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5ef8d8a3fe6fd2431b9286f2f1e0b758678791981aa6607dec7cf6238ea84c)
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument configuration_versions", value=configuration_versions, expected_type=type_hints["configuration_versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_version is not None:
            self._values["cluster_version"] = cluster_version
        if configuration_versions is not None:
            self._values["configuration_versions"] = configuration_versions

    @builtins.property
    def cluster_version(self) -> typing.Optional[builtins.str]:
        '''Dynatrace version.

        :schema: Metadata#ClusterVersion
        '''
        result = self._values.get("cluster_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_versions(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A sorted list of the version numbers of the configuration.

        :schema: Metadata#ConfigurationVersions
        '''
        result = self._values.get("configuration_versions")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.Tile",
    jsii_struct_bases=[],
    name_mapping={
        "bounds": "bounds",
        "configured": "configured",
        "name": "name",
        "tile_filter": "tileFilter",
        "tile_type": "tileType",
    },
)
class Tile:
    def __init__(
        self,
        *,
        bounds: typing.Optional[typing.Union["TileBounds", typing.Dict[builtins.str, typing.Any]]] = None,
        configured: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        tile_filter: typing.Optional[typing.Union[DashboardFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        tile_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration of a tile.

        The actual set of fields depends on the type of the tile. Find the list of actual objects in the description of the tileType field or see Dashboards API - Tile JSON models (https://dt-url.net/2wc3spx).

        :param bounds: 
        :param configured: 
        :param name: 
        :param tile_filter: 
        :param tile_type: 

        :schema: Tile
        '''
        if isinstance(bounds, dict):
            bounds = TileBounds(**bounds)
        if isinstance(tile_filter, dict):
            tile_filter = DashboardFilter(**tile_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c70041ad446fbf79f4b249adbe3f7d70ecd103b7983fe04657662356025f4b7)
            check_type(argname="argument bounds", value=bounds, expected_type=type_hints["bounds"])
            check_type(argname="argument configured", value=configured, expected_type=type_hints["configured"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tile_filter", value=tile_filter, expected_type=type_hints["tile_filter"])
            check_type(argname="argument tile_type", value=tile_type, expected_type=type_hints["tile_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bounds is not None:
            self._values["bounds"] = bounds
        if configured is not None:
            self._values["configured"] = configured
        if name is not None:
            self._values["name"] = name
        if tile_filter is not None:
            self._values["tile_filter"] = tile_filter
        if tile_type is not None:
            self._values["tile_type"] = tile_type

    @builtins.property
    def bounds(self) -> typing.Optional["TileBounds"]:
        '''
        :schema: Tile#Bounds
        '''
        result = self._values.get("bounds")
        return typing.cast(typing.Optional["TileBounds"], result)

    @builtins.property
    def configured(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Tile#Configured
        '''
        result = self._values.get("configured")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Tile#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tile_filter(self) -> typing.Optional[DashboardFilter]:
        '''
        :schema: Tile#TileFilter
        '''
        result = self._values.get("tile_filter")
        return typing.cast(typing.Optional[DashboardFilter], result)

    @builtins.property
    def tile_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Tile#TileType
        '''
        result = self._values.get("tile_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-configuration-dashboard.TileBounds",
    jsii_struct_bases=[],
    name_mapping={"height": "height", "left": "left", "top": "top", "width": "width"},
)
class TileBounds:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        left: typing.Optional[jsii.Number] = None,
        top: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param height: 
        :param left: 
        :param top: 
        :param width: 

        :schema: TileBounds
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b0f0588470569c2bb36a2afe2a36151a60d111dc3321907468655abd40555c)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument top", value=top, expected_type=type_hints["top"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if left is not None:
            self._values["left"] = left
        if top is not None:
            self._values["top"] = top
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: TileBounds#Height
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def left(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: TileBounds#Left
        '''
        result = self._values.get("left")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def top(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: TileBounds#Top
        '''
        result = self._values.get("top")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: TileBounds#Width
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TileBounds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDashboard",
    "CfnDashboardProps",
    "DashboardFilter",
    "DashboardMetadata",
    "DashboardMetadataTilesNameSize",
    "DynamicFilters",
    "EntityShortRepresentation",
    "Metadata",
    "Tile",
    "TileBounds",
]

publication.publish()

def _typecheckingstub__da0964e762f980dc78d1de0a534724856042948296efa48f2fa99d6e01aa7b1e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dashboard_metadata: typing.Union[DashboardMetadata, typing.Dict[builtins.str, typing.Any]],
    tiles: typing.Sequence[typing.Union[Tile, typing.Dict[builtins.str, typing.Any]]],
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69e9fff09099c79080a15af576cd3e6f746837d40ba8ff416c2fa46db0b6934(
    *,
    dashboard_metadata: typing.Union[DashboardMetadata, typing.Dict[builtins.str, typing.Any]],
    tiles: typing.Sequence[typing.Union[Tile, typing.Dict[builtins.str, typing.Any]]],
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71409840f249ddc420ef1a0a8c4f31a1cc198a38c4e9641e86776cd1e36a7bdd(
    *,
    management_zone: typing.Optional[typing.Union[EntityShortRepresentation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeframe: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19f431d58134bf0a371f5d2486e08612fab69482dc9c942192a547c51643aa6(
    *,
    name: builtins.str,
    owner: builtins.str,
    dashboard_filter: typing.Optional[typing.Union[DashboardFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamic_filters: typing.Optional[typing.Union[DynamicFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    preset: typing.Optional[builtins.bool] = None,
    shared: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    tiles_name_size: typing.Optional[DashboardMetadataTilesNameSize] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb85bdd9c5b0ca6cae02fd65d6e4fc23f0c54df2bec85778b3595d0528e9486b(
    *,
    filters: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470570980515efc639534c1aec9e522bd86df86b91208522c79e9fc134a08db(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5ef8d8a3fe6fd2431b9286f2f1e0b758678791981aa6607dec7cf6238ea84c(
    *,
    cluster_version: typing.Optional[builtins.str] = None,
    configuration_versions: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c70041ad446fbf79f4b249adbe3f7d70ecd103b7983fe04657662356025f4b7(
    *,
    bounds: typing.Optional[typing.Union[TileBounds, typing.Dict[builtins.str, typing.Any]]] = None,
    configured: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    tile_filter: typing.Optional[typing.Union[DashboardFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    tile_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b0f0588470569c2bb36a2afe2a36151a60d111dc3321907468655abd40555c(
    *,
    height: typing.Optional[jsii.Number] = None,
    left: typing.Optional[jsii.Number] = None,
    top: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
