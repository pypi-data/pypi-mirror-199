# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'InstanceMaintenancePolicy',
    'InstanceMaintenancePolicyWeeklyMaintenanceWindow',
    'InstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime',
    'InstanceMaintenanceSchedule',
    'InstanceNode',
    'InstancePersistenceConfig',
    'InstanceServerCaCert',
    'GetInstanceMaintenancePolicyResult',
    'GetInstanceMaintenancePolicyWeeklyMaintenanceWindowResult',
    'GetInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeResult',
    'GetInstanceMaintenanceScheduleResult',
    'GetInstanceNodeResult',
    'GetInstancePersistenceConfigResult',
    'GetInstanceServerCaCertResult',
]

@pulumi.output_type
class InstanceMaintenancePolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createTime":
            suggest = "create_time"
        elif key == "updateTime":
            suggest = "update_time"
        elif key == "weeklyMaintenanceWindows":
            suggest = "weekly_maintenance_windows"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceMaintenancePolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceMaintenancePolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceMaintenancePolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 create_time: Optional[str] = None,
                 description: Optional[str] = None,
                 update_time: Optional[str] = None,
                 weekly_maintenance_windows: Optional[Sequence['outputs.InstanceMaintenancePolicyWeeklyMaintenanceWindow']] = None):
        """
        :param str create_time: (Output)
               Output only. The time when the policy was created.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        :param str description: Optional. Description of what this policy is for.
               Create/Update methods return INVALID_ARGUMENT if the
               length is greater than 512.
        :param str update_time: (Output)
               Output only. The time when the policy was last updated.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        :param Sequence['InstanceMaintenancePolicyWeeklyMaintenanceWindowArgs'] weekly_maintenance_windows: Optional. Maintenance window that is applied to resources covered by this policy.
               Minimum 1. For the current version, the maximum number
               of weekly_window is expected to be one.
               Structure is documented below.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)
        if weekly_maintenance_windows is not None:
            pulumi.set(__self__, "weekly_maintenance_windows", weekly_maintenance_windows)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The time when the policy was created.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Optional. Description of what this policy is for.
        Create/Update methods return INVALID_ARGUMENT if the
        length is greater than 512.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The time when the policy was last updated.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter(name="weeklyMaintenanceWindows")
    def weekly_maintenance_windows(self) -> Optional[Sequence['outputs.InstanceMaintenancePolicyWeeklyMaintenanceWindow']]:
        """
        Optional. Maintenance window that is applied to resources covered by this policy.
        Minimum 1. For the current version, the maximum number
        of weekly_window is expected to be one.
        Structure is documented below.
        """
        return pulumi.get(self, "weekly_maintenance_windows")


@pulumi.output_type
class InstanceMaintenancePolicyWeeklyMaintenanceWindow(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceMaintenancePolicyWeeklyMaintenanceWindow. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceMaintenancePolicyWeeklyMaintenanceWindow.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceMaintenancePolicyWeeklyMaintenanceWindow.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 day: str,
                 start_time: 'outputs.InstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime',
                 duration: Optional[str] = None):
        """
        :param str day: Required. The day of week that maintenance updates occur.
               - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified.
               - MONDAY: Monday
               - TUESDAY: Tuesday
               - WEDNESDAY: Wednesday
               - THURSDAY: Thursday
               - FRIDAY: Friday
               - SATURDAY: Saturday
               - SUNDAY: Sunday
               Possible values are `DAY_OF_WEEK_UNSPECIFIED`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, and `SUNDAY`.
        :param 'InstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeArgs' start_time: Required. Start time of the window in UTC time.
               Structure is documented below.
        :param str duration: (Output)
               Output only. Duration of the maintenance window.
               The current window is fixed at 1 hour.
               A duration in seconds with up to nine fractional digits,
               terminated by 's'. Example: "3.5s".
        """
        pulumi.set(__self__, "day", day)
        pulumi.set(__self__, "start_time", start_time)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)

    @property
    @pulumi.getter
    def day(self) -> str:
        """
        Required. The day of week that maintenance updates occur.
        - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified.
        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday
        Possible values are `DAY_OF_WEEK_UNSPECIFIED`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, and `SUNDAY`.
        """
        return pulumi.get(self, "day")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> 'outputs.InstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime':
        """
        Required. Start time of the window in UTC time.
        Structure is documented below.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def duration(self) -> Optional[str]:
        """
        (Output)
        Output only. Duration of the maintenance window.
        The current window is fixed at 1 hour.
        A duration in seconds with up to nine fractional digits,
        terminated by 's'. Example: "3.5s".
        """
        return pulumi.get(self, "duration")


@pulumi.output_type
class InstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(dict):
    def __init__(__self__, *,
                 hours: Optional[int] = None,
                 minutes: Optional[int] = None,
                 nanos: Optional[int] = None,
                 seconds: Optional[int] = None):
        """
        :param int hours: Hours of day in 24 hour format. Should be from 0 to 23.
               An API may choose to allow the value "24:00:00" for scenarios like business closing time.
        :param int minutes: Minutes of hour of day. Must be from 0 to 59.
        :param int nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.
        :param int seconds: Seconds of minutes of the time. Must normally be from 0 to 59.
               An API may allow the value 60 if it allows leap-seconds.
        """
        if hours is not None:
            pulumi.set(__self__, "hours", hours)
        if minutes is not None:
            pulumi.set(__self__, "minutes", minutes)
        if nanos is not None:
            pulumi.set(__self__, "nanos", nanos)
        if seconds is not None:
            pulumi.set(__self__, "seconds", seconds)

    @property
    @pulumi.getter
    def hours(self) -> Optional[int]:
        """
        Hours of day in 24 hour format. Should be from 0 to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.
        """
        return pulumi.get(self, "hours")

    @property
    @pulumi.getter
    def minutes(self) -> Optional[int]:
        """
        Minutes of hour of day. Must be from 0 to 59.
        """
        return pulumi.get(self, "minutes")

    @property
    @pulumi.getter
    def nanos(self) -> Optional[int]:
        """
        Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.
        """
        return pulumi.get(self, "nanos")

    @property
    @pulumi.getter
    def seconds(self) -> Optional[int]:
        """
        Seconds of minutes of the time. Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.
        """
        return pulumi.get(self, "seconds")


@pulumi.output_type
class InstanceMaintenanceSchedule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endTime":
            suggest = "end_time"
        elif key == "scheduleDeadlineTime":
            suggest = "schedule_deadline_time"
        elif key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceMaintenanceSchedule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceMaintenanceSchedule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceMaintenanceSchedule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 end_time: Optional[str] = None,
                 schedule_deadline_time: Optional[str] = None,
                 start_time: Optional[str] = None):
        """
        :param str end_time: (Output)
               Output only. The end time of any upcoming scheduled maintenance for this instance.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        :param str schedule_deadline_time: (Output)
               Output only. The deadline that the maintenance schedule start time
               can not go beyond, including reschedule.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        :param str start_time: (Output)
               Output only. The start time of any upcoming scheduled maintenance for this instance.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        """
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if schedule_deadline_time is not None:
            pulumi.set(__self__, "schedule_deadline_time", schedule_deadline_time)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The end time of any upcoming scheduled maintenance for this instance.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="scheduleDeadlineTime")
    def schedule_deadline_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The deadline that the maintenance schedule start time
        can not go beyond, including reschedule.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "schedule_deadline_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The start time of any upcoming scheduled maintenance for this instance.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "start_time")


@pulumi.output_type
class InstanceNode(dict):
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 zone: Optional[str] = None):
        """
        :param str id: (Output)
               Node identifying string. e.g. 'node-0', 'node-1'
        :param str zone: (Output)
               Location of the node.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        (Output)
        Node identifying string. e.g. 'node-0', 'node-1'
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def zone(self) -> Optional[str]:
        """
        (Output)
        Location of the node.
        """
        return pulumi.get(self, "zone")


@pulumi.output_type
class InstancePersistenceConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "persistenceMode":
            suggest = "persistence_mode"
        elif key == "rdbNextSnapshotTime":
            suggest = "rdb_next_snapshot_time"
        elif key == "rdbSnapshotPeriod":
            suggest = "rdb_snapshot_period"
        elif key == "rdbSnapshotStartTime":
            suggest = "rdb_snapshot_start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstancePersistenceConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstancePersistenceConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstancePersistenceConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 persistence_mode: Optional[str] = None,
                 rdb_next_snapshot_time: Optional[str] = None,
                 rdb_snapshot_period: Optional[str] = None,
                 rdb_snapshot_start_time: Optional[str] = None):
        """
        :param str persistence_mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used.
               - DISABLED: 	Persistence is disabled for the instance, and any existing snapshots are deleted.
               - RDB: RDB based Persistence is enabled.
               Possible values are `DISABLED` and `RDB`.
        :param str rdb_next_snapshot_time: (Output)
               Output only. The next time that a snapshot attempt is scheduled to occur.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up
               to nine fractional digits.
               Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        :param str rdb_snapshot_period: Optional. Available snapshot periods for scheduling.
               - ONE_HOUR:	Snapshot every 1 hour.
               - SIX_HOURS:	Snapshot every 6 hours.
               - TWELVE_HOURS:	Snapshot every 12 hours.
               - TWENTY_FOUR_HOURS:	Snapshot every 24 hours.
               Possible values are `ONE_HOUR`, `SIX_HOURS`, `TWELVE_HOURS`, and `TWENTY_FOUR_HOURS`.
        :param str rdb_snapshot_start_time: Optional. Date and time that the first snapshot was/will be attempted,
               and to which future snapshots will be aligned. If not provided,
               the current time will be used.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution
               and up to nine fractional digits.
               Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        if persistence_mode is not None:
            pulumi.set(__self__, "persistence_mode", persistence_mode)
        if rdb_next_snapshot_time is not None:
            pulumi.set(__self__, "rdb_next_snapshot_time", rdb_next_snapshot_time)
        if rdb_snapshot_period is not None:
            pulumi.set(__self__, "rdb_snapshot_period", rdb_snapshot_period)
        if rdb_snapshot_start_time is not None:
            pulumi.set(__self__, "rdb_snapshot_start_time", rdb_snapshot_start_time)

    @property
    @pulumi.getter(name="persistenceMode")
    def persistence_mode(self) -> Optional[str]:
        """
        Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used.
        - DISABLED: 	Persistence is disabled for the instance, and any existing snapshots are deleted.
        - RDB: RDB based Persistence is enabled.
        Possible values are `DISABLED` and `RDB`.
        """
        return pulumi.get(self, "persistence_mode")

    @property
    @pulumi.getter(name="rdbNextSnapshotTime")
    def rdb_next_snapshot_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The next time that a snapshot attempt is scheduled to occur.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up
        to nine fractional digits.
        Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "rdb_next_snapshot_time")

    @property
    @pulumi.getter(name="rdbSnapshotPeriod")
    def rdb_snapshot_period(self) -> Optional[str]:
        """
        Optional. Available snapshot periods for scheduling.
        - ONE_HOUR:	Snapshot every 1 hour.
        - SIX_HOURS:	Snapshot every 6 hours.
        - TWELVE_HOURS:	Snapshot every 12 hours.
        - TWENTY_FOUR_HOURS:	Snapshot every 24 hours.
        Possible values are `ONE_HOUR`, `SIX_HOURS`, `TWELVE_HOURS`, and `TWENTY_FOUR_HOURS`.
        """
        return pulumi.get(self, "rdb_snapshot_period")

    @property
    @pulumi.getter(name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> Optional[str]:
        """
        Optional. Date and time that the first snapshot was/will be attempted,
        and to which future snapshots will be aligned. If not provided,
        the current time will be used.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution
        and up to nine fractional digits.
        Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "rdb_snapshot_start_time")


@pulumi.output_type
class InstanceServerCaCert(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createTime":
            suggest = "create_time"
        elif key == "expireTime":
            suggest = "expire_time"
        elif key == "serialNumber":
            suggest = "serial_number"
        elif key == "sha1Fingerprint":
            suggest = "sha1_fingerprint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceServerCaCert. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceServerCaCert.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceServerCaCert.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cert: Optional[str] = None,
                 create_time: Optional[str] = None,
                 expire_time: Optional[str] = None,
                 serial_number: Optional[str] = None,
                 sha1_fingerprint: Optional[str] = None):
        """
        :param str cert: (Output)
               The certificate data in PEM format.
        :param str create_time: (Output)
               Output only. The time when the policy was created.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
               resolution and up to nine fractional digits.
        :param str expire_time: (Output)
               The time when the certificate expires.
        :param str serial_number: (Output)
               Serial number, as extracted from the certificate.
        :param str sha1_fingerprint: (Output)
               Sha1 Fingerprint of the certificate.
        """
        if cert is not None:
            pulumi.set(__self__, "cert", cert)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)
        if sha1_fingerprint is not None:
            pulumi.set(__self__, "sha1_fingerprint", sha1_fingerprint)

    @property
    @pulumi.getter
    def cert(self) -> Optional[str]:
        """
        (Output)
        The certificate data in PEM format.
        """
        return pulumi.get(self, "cert")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[str]:
        """
        (Output)
        Output only. The time when the policy was created.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[str]:
        """
        (Output)
        The time when the certificate expires.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[str]:
        """
        (Output)
        Serial number, as extracted from the certificate.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="sha1Fingerprint")
    def sha1_fingerprint(self) -> Optional[str]:
        """
        (Output)
        Sha1 Fingerprint of the certificate.
        """
        return pulumi.get(self, "sha1_fingerprint")


@pulumi.output_type
class GetInstanceMaintenancePolicyResult(dict):
    def __init__(__self__, *,
                 create_time: str,
                 description: str,
                 update_time: str,
                 weekly_maintenance_windows: Sequence['outputs.GetInstanceMaintenancePolicyWeeklyMaintenanceWindowResult']):
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "update_time", update_time)
        pulumi.set(__self__, "weekly_maintenance_windows", weekly_maintenance_windows)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter(name="weeklyMaintenanceWindows")
    def weekly_maintenance_windows(self) -> Sequence['outputs.GetInstanceMaintenancePolicyWeeklyMaintenanceWindowResult']:
        return pulumi.get(self, "weekly_maintenance_windows")


@pulumi.output_type
class GetInstanceMaintenancePolicyWeeklyMaintenanceWindowResult(dict):
    def __init__(__self__, *,
                 day: str,
                 duration: str,
                 start_times: Sequence['outputs.GetInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeResult']):
        pulumi.set(__self__, "day", day)
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "start_times", start_times)

    @property
    @pulumi.getter
    def day(self) -> str:
        return pulumi.get(self, "day")

    @property
    @pulumi.getter
    def duration(self) -> str:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="startTimes")
    def start_times(self) -> Sequence['outputs.GetInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeResult']:
        return pulumi.get(self, "start_times")


@pulumi.output_type
class GetInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeResult(dict):
    def __init__(__self__, *,
                 hours: int,
                 minutes: int,
                 nanos: int,
                 seconds: int):
        pulumi.set(__self__, "hours", hours)
        pulumi.set(__self__, "minutes", minutes)
        pulumi.set(__self__, "nanos", nanos)
        pulumi.set(__self__, "seconds", seconds)

    @property
    @pulumi.getter
    def hours(self) -> int:
        return pulumi.get(self, "hours")

    @property
    @pulumi.getter
    def minutes(self) -> int:
        return pulumi.get(self, "minutes")

    @property
    @pulumi.getter
    def nanos(self) -> int:
        return pulumi.get(self, "nanos")

    @property
    @pulumi.getter
    def seconds(self) -> int:
        return pulumi.get(self, "seconds")


@pulumi.output_type
class GetInstanceMaintenanceScheduleResult(dict):
    def __init__(__self__, *,
                 end_time: str,
                 schedule_deadline_time: str,
                 start_time: str):
        pulumi.set(__self__, "end_time", end_time)
        pulumi.set(__self__, "schedule_deadline_time", schedule_deadline_time)
        pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="scheduleDeadlineTime")
    def schedule_deadline_time(self) -> str:
        return pulumi.get(self, "schedule_deadline_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        return pulumi.get(self, "start_time")


@pulumi.output_type
class GetInstanceNodeResult(dict):
    def __init__(__self__, *,
                 id: str,
                 zone: str):
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def zone(self) -> str:
        return pulumi.get(self, "zone")


@pulumi.output_type
class GetInstancePersistenceConfigResult(dict):
    def __init__(__self__, *,
                 persistence_mode: str,
                 rdb_next_snapshot_time: str,
                 rdb_snapshot_period: str,
                 rdb_snapshot_start_time: str):
        pulumi.set(__self__, "persistence_mode", persistence_mode)
        pulumi.set(__self__, "rdb_next_snapshot_time", rdb_next_snapshot_time)
        pulumi.set(__self__, "rdb_snapshot_period", rdb_snapshot_period)
        pulumi.set(__self__, "rdb_snapshot_start_time", rdb_snapshot_start_time)

    @property
    @pulumi.getter(name="persistenceMode")
    def persistence_mode(self) -> str:
        return pulumi.get(self, "persistence_mode")

    @property
    @pulumi.getter(name="rdbNextSnapshotTime")
    def rdb_next_snapshot_time(self) -> str:
        return pulumi.get(self, "rdb_next_snapshot_time")

    @property
    @pulumi.getter(name="rdbSnapshotPeriod")
    def rdb_snapshot_period(self) -> str:
        return pulumi.get(self, "rdb_snapshot_period")

    @property
    @pulumi.getter(name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> str:
        return pulumi.get(self, "rdb_snapshot_start_time")


@pulumi.output_type
class GetInstanceServerCaCertResult(dict):
    def __init__(__self__, *,
                 cert: str,
                 create_time: str,
                 expire_time: str,
                 serial_number: str,
                 sha1_fingerprint: str):
        pulumi.set(__self__, "cert", cert)
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "expire_time", expire_time)
        pulumi.set(__self__, "serial_number", serial_number)
        pulumi.set(__self__, "sha1_fingerprint", sha1_fingerprint)

    @property
    @pulumi.getter
    def cert(self) -> str:
        return pulumi.get(self, "cert")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> str:
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> str:
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="sha1Fingerprint")
    def sha1_fingerprint(self) -> str:
        return pulumi.get(self, "sha1_fingerprint")


