'''
# snowflake-user-user

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::User::User` v1.1.0.

## Description

Allows for the creation and modification of a Snowflake User. https://docs.snowflake.com/en/user-guide/admin-user-management.html

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::User::User \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-User-User \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::User::User`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-user-user+v1.1.0).
* Issues related to `Snowflake::User::User` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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


class CfnUser(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/snowflake-user-user.CfnUser",
):
    '''A CloudFormation ``Snowflake::User::User``.

    :cloudformationResource: Snowflake::User::User
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        password: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        days_to_expiry: typing.Optional[jsii.Number] = None,
        default_role: typing.Optional[builtins.str] = None,
        default_warehouse: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        must_change_password: typing.Optional[builtins.bool] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Snowflake::User::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Identifier for the user; must be unique for your account.
        :param password: The password for the user.
        :param comment: Specifies a comment for the user.
        :param days_to_expiry: Specifies the number of days after which the user status is set to Expired and the user is no longer allowed to log in.
        :param default_role: Specifies the primary role that is active by default for the user's session upon login.
        :param default_warehouse: Specifies the namespace (database only or database and schema) that is active by default for the user's session upon login.
        :param disabled: Specifies whether the user is disabled.
        :param display_name: Name displayed for the user in the Snowflake web interface.
        :param email: Email address for the user.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param login_name: Name that the user enters to log into the system. Login names for users must be unique across your entire account.
        :param middle_name: Middle name of the user.
        :param mins_to_bypass_mfa: Specifies the number of minutes to temporarily bypass MFA for the user.
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared.
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.
        :param rsa_public_key: Specifies the user's RSA public key; used for key pair authentication.
        :param rsa_public_key2: Specifies the user's second RSA public key; used to rotate the public and private keys for key pair authentication based on an expiration schedule set by your organization.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766e005371a9376804ba1d6b68c851ecd75383813d93153b1acb839ef6115d83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            name=name,
            password=password,
            comment=comment,
            days_to_expiry=days_to_expiry,
            default_role=default_role,
            default_warehouse=default_warehouse,
            disabled=disabled,
            display_name=display_name,
            email=email,
            first_name=first_name,
            last_name=last_name,
            login_name=login_name,
            middle_name=middle_name,
            mins_to_bypass_mfa=mins_to_bypass_mfa,
            mins_to_unlock=mins_to_unlock,
            must_change_password=must_change_password,
            rsa_public_key=rsa_public_key,
            rsa_public_key2=rsa_public_key2,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnUserProps":
        '''Resource props.'''
        return typing.cast("CfnUserProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/snowflake-user-user.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "password": "password",
        "comment": "comment",
        "days_to_expiry": "daysToExpiry",
        "default_role": "defaultRole",
        "default_warehouse": "defaultWarehouse",
        "disabled": "disabled",
        "display_name": "displayName",
        "email": "email",
        "first_name": "firstName",
        "last_name": "lastName",
        "login_name": "loginName",
        "middle_name": "middleName",
        "mins_to_bypass_mfa": "minsToBypassMfa",
        "mins_to_unlock": "minsToUnlock",
        "must_change_password": "mustChangePassword",
        "rsa_public_key": "rsaPublicKey",
        "rsa_public_key2": "rsaPublicKey2",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        password: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        days_to_expiry: typing.Optional[jsii.Number] = None,
        default_role: typing.Optional[builtins.str] = None,
        default_warehouse: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        must_change_password: typing.Optional[builtins.bool] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Allows for the creation and modification of a Snowflake User.

        https://docs.snowflake.com/en/user-guide/admin-user-management.html

        :param name: Identifier for the user; must be unique for your account.
        :param password: The password for the user.
        :param comment: Specifies a comment for the user.
        :param days_to_expiry: Specifies the number of days after which the user status is set to Expired and the user is no longer allowed to log in.
        :param default_role: Specifies the primary role that is active by default for the user's session upon login.
        :param default_warehouse: Specifies the namespace (database only or database and schema) that is active by default for the user's session upon login.
        :param disabled: Specifies whether the user is disabled.
        :param display_name: Name displayed for the user in the Snowflake web interface.
        :param email: Email address for the user.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param login_name: Name that the user enters to log into the system. Login names for users must be unique across your entire account.
        :param middle_name: Middle name of the user.
        :param mins_to_bypass_mfa: Specifies the number of minutes to temporarily bypass MFA for the user.
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared.
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.
        :param rsa_public_key: Specifies the user's RSA public key; used for key pair authentication.
        :param rsa_public_key2: Specifies the user's second RSA public key; used to rotate the public and private keys for key pair authentication based on an expiration schedule set by your organization.

        :schema: CfnUserProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba22c88a9e562291dc510929a3107d622165c33cc841054b1711a7e5a7d7e35)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument days_to_expiry", value=days_to_expiry, expected_type=type_hints["days_to_expiry"])
            check_type(argname="argument default_role", value=default_role, expected_type=type_hints["default_role"])
            check_type(argname="argument default_warehouse", value=default_warehouse, expected_type=type_hints["default_warehouse"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument login_name", value=login_name, expected_type=type_hints["login_name"])
            check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
            check_type(argname="argument mins_to_bypass_mfa", value=mins_to_bypass_mfa, expected_type=type_hints["mins_to_bypass_mfa"])
            check_type(argname="argument mins_to_unlock", value=mins_to_unlock, expected_type=type_hints["mins_to_unlock"])
            check_type(argname="argument must_change_password", value=must_change_password, expected_type=type_hints["must_change_password"])
            check_type(argname="argument rsa_public_key", value=rsa_public_key, expected_type=type_hints["rsa_public_key"])
            check_type(argname="argument rsa_public_key2", value=rsa_public_key2, expected_type=type_hints["rsa_public_key2"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "password": password,
        }
        if comment is not None:
            self._values["comment"] = comment
        if days_to_expiry is not None:
            self._values["days_to_expiry"] = days_to_expiry
        if default_role is not None:
            self._values["default_role"] = default_role
        if default_warehouse is not None:
            self._values["default_warehouse"] = default_warehouse
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if email is not None:
            self._values["email"] = email
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if login_name is not None:
            self._values["login_name"] = login_name
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if mins_to_bypass_mfa is not None:
            self._values["mins_to_bypass_mfa"] = mins_to_bypass_mfa
        if mins_to_unlock is not None:
            self._values["mins_to_unlock"] = mins_to_unlock
        if must_change_password is not None:
            self._values["must_change_password"] = must_change_password
        if rsa_public_key is not None:
            self._values["rsa_public_key"] = rsa_public_key
        if rsa_public_key2 is not None:
            self._values["rsa_public_key2"] = rsa_public_key2

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifier for the user;

        must be unique for your account.

        :schema: CfnUserProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''The password for the user.

        :schema: CfnUserProps#Password
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the user.

        :schema: CfnUserProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_to_expiry(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days after which the user status is set to Expired and the user is no longer allowed to log in.

        :schema: CfnUserProps#DaysToExpiry
        '''
        result = self._values.get("days_to_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the primary role that is active by default for the user's session upon login.

        :schema: CfnUserProps#DefaultRole
        '''
        result = self._values.get("default_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the namespace (database only or database and schema) that is active by default for the user's session upon login.

        :schema: CfnUserProps#DefaultWarehouse
        '''
        result = self._values.get("default_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the user is disabled.

        :schema: CfnUserProps#Disabled
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name displayed for the user in the Snowflake web interface.

        :schema: CfnUserProps#DisplayName
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address for the user.

        :schema: CfnUserProps#Email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''First name of the user.

        :schema: CfnUserProps#FirstName
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Last name of the user.

        :schema: CfnUserProps#LastName
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''Name that the user enters to log into the system.

        Login names for users must be unique across your entire account.

        :schema: CfnUserProps#LoginName
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def middle_name(self) -> typing.Optional[builtins.str]:
        '''Middle name of the user.

        :schema: CfnUserProps#MiddleName
        '''
        result = self._values.get("middle_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mins_to_bypass_mfa(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes to temporarily bypass MFA for the user.

        :schema: CfnUserProps#MinsToBypassMfa
        '''
        result = self._values.get("mins_to_bypass_mfa")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mins_to_unlock(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes until the temporary lock on the user login is cleared.

        :schema: CfnUserProps#MinsToUnlock
        '''
        result = self._values.get("mins_to_unlock")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def must_change_password(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.

        :schema: CfnUserProps#MustChangePassword
        '''
        result = self._values.get("must_change_password")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the user's RSA public key;

        used for key pair authentication.

        :schema: CfnUserProps#RsaPublicKey
        '''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies the user's second RSA public key;

        used to rotate the public and private keys for key pair authentication based on an expiration schedule set by your organization.

        :schema: CfnUserProps#RsaPublicKey2
        '''
        result = self._values.get("rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnUser",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__766e005371a9376804ba1d6b68c851ecd75383813d93153b1acb839ef6115d83(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    password: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    days_to_expiry: typing.Optional[jsii.Number] = None,
    default_role: typing.Optional[builtins.str] = None,
    default_warehouse: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    login_name: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    must_change_password: typing.Optional[builtins.bool] = None,
    rsa_public_key: typing.Optional[builtins.str] = None,
    rsa_public_key2: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba22c88a9e562291dc510929a3107d622165c33cc841054b1711a7e5a7d7e35(
    *,
    name: builtins.str,
    password: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    days_to_expiry: typing.Optional[jsii.Number] = None,
    default_role: typing.Optional[builtins.str] = None,
    default_warehouse: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    login_name: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    must_change_password: typing.Optional[builtins.bool] = None,
    rsa_public_key: typing.Optional[builtins.str] = None,
    rsa_public_key2: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
