'''
# fastly-logging-s3

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Logging::S3` v1.1.0.

## Description

Manage a Fastly service

## References

* [Source](https://developer.fastly.com/reference/api/logging/s3/)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Logging::S3 \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Logging-S3 \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Logging::S3`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-logging-s3+v1.1.0).
* Issues related to `Fastly::Logging::S3` should be reported to the [publisher](https://developer.fastly.com/reference/api/logging/s3/).

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


class CfnS3(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3",
):
    '''A CloudFormation ``Fastly::Logging::S3``.

    :cloudformationResource: Fastly::Logging::S3
    :link: https://developer.fastly.com/reference/api/logging/s3/
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        compression_codec: typing.Optional["CfnS3PropsCompressionCodec"] = None,
        domain: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        format_version: typing.Optional["CfnS3PropsFormatVersion"] = None,
        gzip_level: typing.Optional[jsii.Number] = None,
        iam_role: typing.Optional[builtins.str] = None,
        message_type: typing.Optional["CfnS3PropsMessageType"] = None,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        period: typing.Optional[jsii.Number] = None,
        placement: typing.Optional["CfnS3PropsPlacement"] = None,
        public_key: typing.Optional[builtins.str] = None,
        redundancy: typing.Optional[builtins.str] = None,
        response_condition: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        service_id: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Logging::S3``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket_name: The bucket name for S3 account.
        :param access_key: The access key for your S3 account. Not required if iam_role is provided.
        :param acl: The access control list (ACL) specific request header.
        :param compression_codec: The codec used for compressing your logs.
        :param domain: The domain of the Amazon S3 endpoint.
        :param format: A Fastly log format string.
        :param format_version: The version of the custom logging format used for the configured endpoint.
        :param gzip_level: The level of gzip encoding when sending logs (default 0, no compression).
        :param iam_role: The Amazon Resource Name (ARN) for the IAM role granting Fastly access to S3. Not required if access_key and secret_key are provided.
        :param message_type: How the message should be formatted. [Default classic]
        :param name: The name for the real-time logging configuration.
        :param path: The path to upload logs to.
        :param period: How frequently log files are finalized so they can be available for reading (in seconds).
        :param placement: Where in the generated VCL the logging call should be placed.
        :param public_key: A PGP public key that Fastly will use to encrypt your log files before writing them to disk.
        :param redundancy: The S3 redundancy level.
        :param response_condition: The name of an existing condition in the configured endpoint, or leave blank to always execute.
        :param secret_key: The secret key for your S3 account. Not required if iam_role is provided.
        :param server_side_encryption: Set this to AES256 or aws:kms to enable S3 Server Side Encryption.
        :param server_side_encryption_kms_key_id: Optional server-side KMS Key Id. Must be set if server_side_encryption is set to aws:kms or AES256.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param version: Integer identifying a domain version. Read-only.
        :param version_id: Alphanumeric string identifying the service version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9070044867a3b986ddeba6743f84dba197de7d1cdba50b3e2154e5bb5d04c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnS3Props(
            bucket_name=bucket_name,
            access_key=access_key,
            acl=acl,
            compression_codec=compression_codec,
            domain=domain,
            format=format,
            format_version=format_version,
            gzip_level=gzip_level,
            iam_role=iam_role,
            message_type=message_type,
            name=name,
            path=path,
            period=period,
            placement=placement,
            public_key=public_key,
            redundancy=redundancy,
            response_condition=response_condition,
            secret_key=secret_key,
            server_side_encryption=server_side_encryption,
            server_side_encryption_kms_key_id=server_side_encryption_kms_key_id,
            service_id=service_id,
            version=version,
            version_id=version_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''Attribute ``Fastly::Logging::S3.CreatedAt``.

        :link: https://developer.fastly.com/reference/api/logging/s3/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDeletedAt")
    def attr_deleted_at(self) -> builtins.str:
        '''Attribute ``Fastly::Logging::S3.DeletedAt``.

        :link: https://developer.fastly.com/reference/api/logging/s3/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeletedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''Attribute ``Fastly::Logging::S3.UpdatedAt``.

        :link: https://developer.fastly.com/reference/api/logging/s3/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnS3Props":
        '''Resource props.'''
        return typing.cast("CfnS3Props", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "access_key": "accessKey",
        "acl": "acl",
        "compression_codec": "compressionCodec",
        "domain": "domain",
        "format": "format",
        "format_version": "formatVersion",
        "gzip_level": "gzipLevel",
        "iam_role": "iamRole",
        "message_type": "messageType",
        "name": "name",
        "path": "path",
        "period": "period",
        "placement": "placement",
        "public_key": "publicKey",
        "redundancy": "redundancy",
        "response_condition": "responseCondition",
        "secret_key": "secretKey",
        "server_side_encryption": "serverSideEncryption",
        "server_side_encryption_kms_key_id": "serverSideEncryptionKmsKeyId",
        "service_id": "serviceId",
        "version": "version",
        "version_id": "versionId",
    },
)
class CfnS3Props:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        compression_codec: typing.Optional["CfnS3PropsCompressionCodec"] = None,
        domain: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        format_version: typing.Optional["CfnS3PropsFormatVersion"] = None,
        gzip_level: typing.Optional[jsii.Number] = None,
        iam_role: typing.Optional[builtins.str] = None,
        message_type: typing.Optional["CfnS3PropsMessageType"] = None,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        period: typing.Optional[jsii.Number] = None,
        placement: typing.Optional["CfnS3PropsPlacement"] = None,
        public_key: typing.Optional[builtins.str] = None,
        redundancy: typing.Optional[builtins.str] = None,
        response_condition: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[builtins.str] = None,
        server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        service_id: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a Fastly service.

        :param bucket_name: The bucket name for S3 account.
        :param access_key: The access key for your S3 account. Not required if iam_role is provided.
        :param acl: The access control list (ACL) specific request header.
        :param compression_codec: The codec used for compressing your logs.
        :param domain: The domain of the Amazon S3 endpoint.
        :param format: A Fastly log format string.
        :param format_version: The version of the custom logging format used for the configured endpoint.
        :param gzip_level: The level of gzip encoding when sending logs (default 0, no compression).
        :param iam_role: The Amazon Resource Name (ARN) for the IAM role granting Fastly access to S3. Not required if access_key and secret_key are provided.
        :param message_type: How the message should be formatted. [Default classic]
        :param name: The name for the real-time logging configuration.
        :param path: The path to upload logs to.
        :param period: How frequently log files are finalized so they can be available for reading (in seconds).
        :param placement: Where in the generated VCL the logging call should be placed.
        :param public_key: A PGP public key that Fastly will use to encrypt your log files before writing them to disk.
        :param redundancy: The S3 redundancy level.
        :param response_condition: The name of an existing condition in the configured endpoint, or leave blank to always execute.
        :param secret_key: The secret key for your S3 account. Not required if iam_role is provided.
        :param server_side_encryption: Set this to AES256 or aws:kms to enable S3 Server Side Encryption.
        :param server_side_encryption_kms_key_id: Optional server-side KMS Key Id. Must be set if server_side_encryption is set to aws:kms or AES256.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param version: Integer identifying a domain version. Read-only.
        :param version_id: Alphanumeric string identifying the service version.

        :schema: CfnS3Props
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f0de01efd4ec39d7a0aaa1b7ec1b5f7c45bf840c00bc1d9efb30e6ed9d2ff1)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument compression_codec", value=compression_codec, expected_type=type_hints["compression_codec"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument gzip_level", value=gzip_level, expected_type=type_hints["gzip_level"])
            check_type(argname="argument iam_role", value=iam_role, expected_type=type_hints["iam_role"])
            check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument redundancy", value=redundancy, expected_type=type_hints["redundancy"])
            check_type(argname="argument response_condition", value=response_condition, expected_type=type_hints["response_condition"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument server_side_encryption_kms_key_id", value=server_side_encryption_kms_key_id, expected_type=type_hints["server_side_encryption_kms_key_id"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if compression_codec is not None:
            self._values["compression_codec"] = compression_codec
        if domain is not None:
            self._values["domain"] = domain
        if format is not None:
            self._values["format"] = format
        if format_version is not None:
            self._values["format_version"] = format_version
        if gzip_level is not None:
            self._values["gzip_level"] = gzip_level
        if iam_role is not None:
            self._values["iam_role"] = iam_role
        if message_type is not None:
            self._values["message_type"] = message_type
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path
        if period is not None:
            self._values["period"] = period
        if placement is not None:
            self._values["placement"] = placement
        if public_key is not None:
            self._values["public_key"] = public_key
        if redundancy is not None:
            self._values["redundancy"] = redundancy
        if response_condition is not None:
            self._values["response_condition"] = response_condition
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_kms_key_id is not None:
            self._values["server_side_encryption_kms_key_id"] = server_side_encryption_kms_key_id
        if service_id is not None:
            self._values["service_id"] = service_id
        if version is not None:
            self._values["version"] = version
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The bucket name for S3 account.

        :schema: CfnS3Props#BucketName
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The access key for your S3 account.

        Not required if iam_role is provided.

        :schema: CfnS3Props#AccessKey
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''The access control list (ACL) specific request header.

        :schema: CfnS3Props#Acl
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_codec(self) -> typing.Optional["CfnS3PropsCompressionCodec"]:
        '''The codec used for compressing your logs.

        :schema: CfnS3Props#CompressionCodec
        '''
        result = self._values.get("compression_codec")
        return typing.cast(typing.Optional["CfnS3PropsCompressionCodec"], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of the Amazon S3 endpoint.

        :schema: CfnS3Props#Domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''A Fastly log format string.

        :schema: CfnS3Props#Format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format_version(self) -> typing.Optional["CfnS3PropsFormatVersion"]:
        '''The version of the custom logging format used for the configured endpoint.

        :schema: CfnS3Props#FormatVersion
        '''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional["CfnS3PropsFormatVersion"], result)

    @builtins.property
    def gzip_level(self) -> typing.Optional[jsii.Number]:
        '''The level of gzip encoding when sending logs (default 0, no compression).

        :schema: CfnS3Props#GzipLevel
        '''
        result = self._values.get("gzip_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iam_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the IAM role granting Fastly access to S3.

        Not required if access_key and secret_key are provided.

        :schema: CfnS3Props#IamRole
        '''
        result = self._values.get("iam_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_type(self) -> typing.Optional["CfnS3PropsMessageType"]:
        '''How the message should be formatted.

        [Default classic]

        :schema: CfnS3Props#MessageType
        '''
        result = self._values.get("message_type")
        return typing.cast(typing.Optional["CfnS3PropsMessageType"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the real-time logging configuration.

        :schema: CfnS3Props#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to upload logs to.

        :schema: CfnS3Props#Path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''How frequently log files are finalized so they can be available for reading (in seconds).

        :schema: CfnS3Props#Period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement(self) -> typing.Optional["CfnS3PropsPlacement"]:
        '''Where in the generated VCL the logging call should be placed.

        :schema: CfnS3Props#Placement
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional["CfnS3PropsPlacement"], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''A PGP public key that Fastly will use to encrypt your log files before writing them to disk.

        :schema: CfnS3Props#PublicKey
        '''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redundancy(self) -> typing.Optional[builtins.str]:
        '''The S3 redundancy level.

        :schema: CfnS3Props#Redundancy
        '''
        result = self._values.get("redundancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_condition(self) -> typing.Optional[builtins.str]:
        '''The name of an existing condition in the configured endpoint, or leave blank to always execute.

        :schema: CfnS3Props#ResponseCondition
        '''
        result = self._values.get("response_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The secret key for your S3 account.

        Not required if iam_role is provided.

        :schema: CfnS3Props#SecretKey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.str]:
        '''Set this to AES256 or aws:kms to enable S3 Server Side Encryption.

        :schema: CfnS3Props#ServerSideEncryption
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Optional server-side KMS Key Id.

        Must be set if server_side_encryption is set to aws:kms or AES256.

        :schema: CfnS3Props#ServerSideEncryptionKmsKeyId
        '''
        result = self._values.get("server_side_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_id(self) -> typing.Optional[builtins.str]:
        '''Alphanumeric string identifying the service.

        Read-only.

        :schema: CfnS3Props#ServiceId
        '''
        result = self._values.get("service_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Integer identifying a domain version.

        Read-only.

        :schema: CfnS3Props#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Alphanumeric string identifying the service version.

        :schema: CfnS3Props#VersionId
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnS3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3PropsCompressionCodec"
)
class CfnS3PropsCompressionCodec(enum.Enum):
    '''The codec used for compressing your logs.

    :schema: CfnS3PropsCompressionCodec
    '''

    ZSTD = "ZSTD"
    '''zstd.'''
    SNAPPY = "SNAPPY"
    '''snappy.'''
    GZIP = "GZIP"
    '''gzip.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3PropsFormatVersion")
class CfnS3PropsFormatVersion(enum.Enum):
    '''The version of the custom logging format used for the configured endpoint.

    :schema: CfnS3PropsFormatVersion
    '''

    VALUE_1 = "VALUE_1"
    '''1.'''
    VALUE_2 = "VALUE_2"
    '''2.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3PropsMessageType")
class CfnS3PropsMessageType(enum.Enum):
    '''How the message should be formatted.

    [Default classic]

    :schema: CfnS3PropsMessageType
    '''

    CLASSIC = "CLASSIC"
    '''classic.'''
    LOGGLY = "LOGGLY"
    '''loggly.'''
    LOGPLEX = "LOGPLEX"
    '''logplex.'''
    BLANK = "BLANK"
    '''blank.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-logging-s3.CfnS3PropsPlacement")
class CfnS3PropsPlacement(enum.Enum):
    '''Where in the generated VCL the logging call should be placed.

    :schema: CfnS3PropsPlacement
    '''

    NONE = "NONE"
    '''none.'''
    WAF_DEBUG = "WAF_DEBUG"
    '''waf_debug.'''


__all__ = [
    "CfnS3",
    "CfnS3Props",
    "CfnS3PropsCompressionCodec",
    "CfnS3PropsFormatVersion",
    "CfnS3PropsMessageType",
    "CfnS3PropsPlacement",
]

publication.publish()

def _typecheckingstub__fa9070044867a3b986ddeba6743f84dba197de7d1cdba50b3e2154e5bb5d04c0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    acl: typing.Optional[builtins.str] = None,
    compression_codec: typing.Optional[CfnS3PropsCompressionCodec] = None,
    domain: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    format_version: typing.Optional[CfnS3PropsFormatVersion] = None,
    gzip_level: typing.Optional[jsii.Number] = None,
    iam_role: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[CfnS3PropsMessageType] = None,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    placement: typing.Optional[CfnS3PropsPlacement] = None,
    public_key: typing.Optional[builtins.str] = None,
    redundancy: typing.Optional[builtins.str] = None,
    response_condition: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[builtins.str] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    service_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f0de01efd4ec39d7a0aaa1b7ec1b5f7c45bf840c00bc1d9efb30e6ed9d2ff1(
    *,
    bucket_name: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    acl: typing.Optional[builtins.str] = None,
    compression_codec: typing.Optional[CfnS3PropsCompressionCodec] = None,
    domain: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    format_version: typing.Optional[CfnS3PropsFormatVersion] = None,
    gzip_level: typing.Optional[jsii.Number] = None,
    iam_role: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[CfnS3PropsMessageType] = None,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    placement: typing.Optional[CfnS3PropsPlacement] = None,
    public_key: typing.Optional[builtins.str] = None,
    redundancy: typing.Optional[builtins.str] = None,
    response_condition: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[builtins.str] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    service_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
