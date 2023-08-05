# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class WorkPlan(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WorkPlan - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'enabled': 'bool',
            'valid': 'bool',
            'constrain_weekly_paid_time': 'bool',
            'flexible_weekly_paid_time': 'bool',
            'weekly_exact_paid_minutes': 'int',
            'weekly_minimum_paid_minutes': 'int',
            'weekly_maximum_paid_minutes': 'int',
            'constrain_paid_time_granularity': 'bool',
            'paid_time_granularity_minutes': 'int',
            'constrain_minimum_time_between_shifts': 'bool',
            'minimum_time_between_shifts_minutes': 'int',
            'maximum_days': 'int',
            'minimum_consecutive_non_working_minutes_per_week': 'int',
            'constrain_maximum_consecutive_working_weekends': 'bool',
            'maximum_consecutive_working_weekends': 'int',
            'minimum_working_days_per_week': 'int',
            'constrain_maximum_consecutive_working_days': 'bool',
            'maximum_consecutive_working_days': 'int',
            'minimum_shift_start_distance_minutes': 'int',
            'minimum_days_off_per_planning_period': 'int',
            'maximum_days_off_per_planning_period': 'int',
            'minimum_paid_minutes_per_planning_period': 'int',
            'maximum_paid_minutes_per_planning_period': 'int',
            'optional_days': 'SetWrapperDayOfWeek',
            'shift_start_variance_type': 'str',
            'shift_start_variances': 'ListWrapperShiftStartVariance',
            'shifts': 'list[WorkPlanShift]',
            'agents': 'list[DeletableUserReference]',
            'agent_count': 'int',
            'metadata': 'WfmVersionedEntityMetadata',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'enabled': 'enabled',
            'valid': 'valid',
            'constrain_weekly_paid_time': 'constrainWeeklyPaidTime',
            'flexible_weekly_paid_time': 'flexibleWeeklyPaidTime',
            'weekly_exact_paid_minutes': 'weeklyExactPaidMinutes',
            'weekly_minimum_paid_minutes': 'weeklyMinimumPaidMinutes',
            'weekly_maximum_paid_minutes': 'weeklyMaximumPaidMinutes',
            'constrain_paid_time_granularity': 'constrainPaidTimeGranularity',
            'paid_time_granularity_minutes': 'paidTimeGranularityMinutes',
            'constrain_minimum_time_between_shifts': 'constrainMinimumTimeBetweenShifts',
            'minimum_time_between_shifts_minutes': 'minimumTimeBetweenShiftsMinutes',
            'maximum_days': 'maximumDays',
            'minimum_consecutive_non_working_minutes_per_week': 'minimumConsecutiveNonWorkingMinutesPerWeek',
            'constrain_maximum_consecutive_working_weekends': 'constrainMaximumConsecutiveWorkingWeekends',
            'maximum_consecutive_working_weekends': 'maximumConsecutiveWorkingWeekends',
            'minimum_working_days_per_week': 'minimumWorkingDaysPerWeek',
            'constrain_maximum_consecutive_working_days': 'constrainMaximumConsecutiveWorkingDays',
            'maximum_consecutive_working_days': 'maximumConsecutiveWorkingDays',
            'minimum_shift_start_distance_minutes': 'minimumShiftStartDistanceMinutes',
            'minimum_days_off_per_planning_period': 'minimumDaysOffPerPlanningPeriod',
            'maximum_days_off_per_planning_period': 'maximumDaysOffPerPlanningPeriod',
            'minimum_paid_minutes_per_planning_period': 'minimumPaidMinutesPerPlanningPeriod',
            'maximum_paid_minutes_per_planning_period': 'maximumPaidMinutesPerPlanningPeriod',
            'optional_days': 'optionalDays',
            'shift_start_variance_type': 'shiftStartVarianceType',
            'shift_start_variances': 'shiftStartVariances',
            'shifts': 'shifts',
            'agents': 'agents',
            'agent_count': 'agentCount',
            'metadata': 'metadata',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._enabled = None
        self._valid = None
        self._constrain_weekly_paid_time = None
        self._flexible_weekly_paid_time = None
        self._weekly_exact_paid_minutes = None
        self._weekly_minimum_paid_minutes = None
        self._weekly_maximum_paid_minutes = None
        self._constrain_paid_time_granularity = None
        self._paid_time_granularity_minutes = None
        self._constrain_minimum_time_between_shifts = None
        self._minimum_time_between_shifts_minutes = None
        self._maximum_days = None
        self._minimum_consecutive_non_working_minutes_per_week = None
        self._constrain_maximum_consecutive_working_weekends = None
        self._maximum_consecutive_working_weekends = None
        self._minimum_working_days_per_week = None
        self._constrain_maximum_consecutive_working_days = None
        self._maximum_consecutive_working_days = None
        self._minimum_shift_start_distance_minutes = None
        self._minimum_days_off_per_planning_period = None
        self._maximum_days_off_per_planning_period = None
        self._minimum_paid_minutes_per_planning_period = None
        self._maximum_paid_minutes_per_planning_period = None
        self._optional_days = None
        self._shift_start_variance_type = None
        self._shift_start_variances = None
        self._shifts = None
        self._agents = None
        self._agent_count = None
        self._metadata = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this WorkPlan.
        The globally unique identifier for the object.

        :return: The id of this WorkPlan.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkPlan.
        The globally unique identifier for the object.

        :param id: The id of this WorkPlan.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WorkPlan.


        :return: The name of this WorkPlan.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkPlan.


        :param name: The name of this WorkPlan.
        :type: str
        """
        

        self._name = name

    @property
    def enabled(self):
        """
        Gets the enabled of this WorkPlan.
        Whether the work plan is enabled for scheduling

        :return: The enabled of this WorkPlan.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this WorkPlan.
        Whether the work plan is enabled for scheduling

        :param enabled: The enabled of this WorkPlan.
        :type: bool
        """
        

        self._enabled = enabled

    @property
    def valid(self):
        """
        Gets the valid of this WorkPlan.
        Whether the work plan is valid or not

        :return: The valid of this WorkPlan.
        :rtype: bool
        """
        return self._valid

    @valid.setter
    def valid(self, valid):
        """
        Sets the valid of this WorkPlan.
        Whether the work plan is valid or not

        :param valid: The valid of this WorkPlan.
        :type: bool
        """
        

        self._valid = valid

    @property
    def constrain_weekly_paid_time(self):
        """
        Gets the constrain_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is enabled for this work plan

        :return: The constrain_weekly_paid_time of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_weekly_paid_time

    @constrain_weekly_paid_time.setter
    def constrain_weekly_paid_time(self, constrain_weekly_paid_time):
        """
        Sets the constrain_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is enabled for this work plan

        :param constrain_weekly_paid_time: The constrain_weekly_paid_time of this WorkPlan.
        :type: bool
        """
        

        self._constrain_weekly_paid_time = constrain_weekly_paid_time

    @property
    def flexible_weekly_paid_time(self):
        """
        Gets the flexible_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is flexible for this work plan

        :return: The flexible_weekly_paid_time of this WorkPlan.
        :rtype: bool
        """
        return self._flexible_weekly_paid_time

    @flexible_weekly_paid_time.setter
    def flexible_weekly_paid_time(self, flexible_weekly_paid_time):
        """
        Sets the flexible_weekly_paid_time of this WorkPlan.
        Whether the weekly paid time constraint is flexible for this work plan

        :param flexible_weekly_paid_time: The flexible_weekly_paid_time of this WorkPlan.
        :type: bool
        """
        

        self._flexible_weekly_paid_time = flexible_weekly_paid_time

    @property
    def weekly_exact_paid_minutes(self):
        """
        Gets the weekly_exact_paid_minutes of this WorkPlan.
        Exact weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == false

        :return: The weekly_exact_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_exact_paid_minutes

    @weekly_exact_paid_minutes.setter
    def weekly_exact_paid_minutes(self, weekly_exact_paid_minutes):
        """
        Sets the weekly_exact_paid_minutes of this WorkPlan.
        Exact weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == false

        :param weekly_exact_paid_minutes: The weekly_exact_paid_minutes of this WorkPlan.
        :type: int
        """
        

        self._weekly_exact_paid_minutes = weekly_exact_paid_minutes

    @property
    def weekly_minimum_paid_minutes(self):
        """
        Gets the weekly_minimum_paid_minutes of this WorkPlan.
        Minimum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :return: The weekly_minimum_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_minimum_paid_minutes

    @weekly_minimum_paid_minutes.setter
    def weekly_minimum_paid_minutes(self, weekly_minimum_paid_minutes):
        """
        Sets the weekly_minimum_paid_minutes of this WorkPlan.
        Minimum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :param weekly_minimum_paid_minutes: The weekly_minimum_paid_minutes of this WorkPlan.
        :type: int
        """
        

        self._weekly_minimum_paid_minutes = weekly_minimum_paid_minutes

    @property
    def weekly_maximum_paid_minutes(self):
        """
        Gets the weekly_maximum_paid_minutes of this WorkPlan.
        Maximum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :return: The weekly_maximum_paid_minutes of this WorkPlan.
        :rtype: int
        """
        return self._weekly_maximum_paid_minutes

    @weekly_maximum_paid_minutes.setter
    def weekly_maximum_paid_minutes(self, weekly_maximum_paid_minutes):
        """
        Sets the weekly_maximum_paid_minutes of this WorkPlan.
        Maximum weekly paid time in minutes for this work plan. Used if flexibleWeeklyPaidTime == true

        :param weekly_maximum_paid_minutes: The weekly_maximum_paid_minutes of this WorkPlan.
        :type: int
        """
        

        self._weekly_maximum_paid_minutes = weekly_maximum_paid_minutes

    @property
    def constrain_paid_time_granularity(self):
        """
        Gets the constrain_paid_time_granularity of this WorkPlan.
        Whether paid time granularity is constrained for this work plan

        :return: The constrain_paid_time_granularity of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_paid_time_granularity

    @constrain_paid_time_granularity.setter
    def constrain_paid_time_granularity(self, constrain_paid_time_granularity):
        """
        Sets the constrain_paid_time_granularity of this WorkPlan.
        Whether paid time granularity is constrained for this work plan

        :param constrain_paid_time_granularity: The constrain_paid_time_granularity of this WorkPlan.
        :type: bool
        """
        

        self._constrain_paid_time_granularity = constrain_paid_time_granularity

    @property
    def paid_time_granularity_minutes(self):
        """
        Gets the paid_time_granularity_minutes of this WorkPlan.
        Granularity in minutes allowed for shift paid time in this work plan. Used if constrainPaidTimeGranularity == true

        :return: The paid_time_granularity_minutes of this WorkPlan.
        :rtype: int
        """
        return self._paid_time_granularity_minutes

    @paid_time_granularity_minutes.setter
    def paid_time_granularity_minutes(self, paid_time_granularity_minutes):
        """
        Sets the paid_time_granularity_minutes of this WorkPlan.
        Granularity in minutes allowed for shift paid time in this work plan. Used if constrainPaidTimeGranularity == true

        :param paid_time_granularity_minutes: The paid_time_granularity_minutes of this WorkPlan.
        :type: int
        """
        

        self._paid_time_granularity_minutes = paid_time_granularity_minutes

    @property
    def constrain_minimum_time_between_shifts(self):
        """
        Gets the constrain_minimum_time_between_shifts of this WorkPlan.
        Whether the minimum time between shifts constraint is enabled for this work plan

        :return: The constrain_minimum_time_between_shifts of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_minimum_time_between_shifts

    @constrain_minimum_time_between_shifts.setter
    def constrain_minimum_time_between_shifts(self, constrain_minimum_time_between_shifts):
        """
        Sets the constrain_minimum_time_between_shifts of this WorkPlan.
        Whether the minimum time between shifts constraint is enabled for this work plan

        :param constrain_minimum_time_between_shifts: The constrain_minimum_time_between_shifts of this WorkPlan.
        :type: bool
        """
        

        self._constrain_minimum_time_between_shifts = constrain_minimum_time_between_shifts

    @property
    def minimum_time_between_shifts_minutes(self):
        """
        Gets the minimum_time_between_shifts_minutes of this WorkPlan.
        Minimum time between shifts in minutes defined in this work plan. Used if constrainMinimumTimeBetweenShifts == true

        :return: The minimum_time_between_shifts_minutes of this WorkPlan.
        :rtype: int
        """
        return self._minimum_time_between_shifts_minutes

    @minimum_time_between_shifts_minutes.setter
    def minimum_time_between_shifts_minutes(self, minimum_time_between_shifts_minutes):
        """
        Sets the minimum_time_between_shifts_minutes of this WorkPlan.
        Minimum time between shifts in minutes defined in this work plan. Used if constrainMinimumTimeBetweenShifts == true

        :param minimum_time_between_shifts_minutes: The minimum_time_between_shifts_minutes of this WorkPlan.
        :type: int
        """
        

        self._minimum_time_between_shifts_minutes = minimum_time_between_shifts_minutes

    @property
    def maximum_days(self):
        """
        Gets the maximum_days of this WorkPlan.
        Maximum number days in a week allowed to be scheduled for this work plan

        :return: The maximum_days of this WorkPlan.
        :rtype: int
        """
        return self._maximum_days

    @maximum_days.setter
    def maximum_days(self, maximum_days):
        """
        Sets the maximum_days of this WorkPlan.
        Maximum number days in a week allowed to be scheduled for this work plan

        :param maximum_days: The maximum_days of this WorkPlan.
        :type: int
        """
        

        self._maximum_days = maximum_days

    @property
    def minimum_consecutive_non_working_minutes_per_week(self):
        """
        Gets the minimum_consecutive_non_working_minutes_per_week of this WorkPlan.
        Minimum amount of consecutive non working minutes per week that agents who are assigned this work plan are allowed to have off

        :return: The minimum_consecutive_non_working_minutes_per_week of this WorkPlan.
        :rtype: int
        """
        return self._minimum_consecutive_non_working_minutes_per_week

    @minimum_consecutive_non_working_minutes_per_week.setter
    def minimum_consecutive_non_working_minutes_per_week(self, minimum_consecutive_non_working_minutes_per_week):
        """
        Sets the minimum_consecutive_non_working_minutes_per_week of this WorkPlan.
        Minimum amount of consecutive non working minutes per week that agents who are assigned this work plan are allowed to have off

        :param minimum_consecutive_non_working_minutes_per_week: The minimum_consecutive_non_working_minutes_per_week of this WorkPlan.
        :type: int
        """
        

        self._minimum_consecutive_non_working_minutes_per_week = minimum_consecutive_non_working_minutes_per_week

    @property
    def constrain_maximum_consecutive_working_weekends(self):
        """
        Gets the constrain_maximum_consecutive_working_weekends of this WorkPlan.
        Whether to constrain the maximum consecutive working weekends

        :return: The constrain_maximum_consecutive_working_weekends of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_maximum_consecutive_working_weekends

    @constrain_maximum_consecutive_working_weekends.setter
    def constrain_maximum_consecutive_working_weekends(self, constrain_maximum_consecutive_working_weekends):
        """
        Sets the constrain_maximum_consecutive_working_weekends of this WorkPlan.
        Whether to constrain the maximum consecutive working weekends

        :param constrain_maximum_consecutive_working_weekends: The constrain_maximum_consecutive_working_weekends of this WorkPlan.
        :type: bool
        """
        

        self._constrain_maximum_consecutive_working_weekends = constrain_maximum_consecutive_working_weekends

    @property
    def maximum_consecutive_working_weekends(self):
        """
        Gets the maximum_consecutive_working_weekends of this WorkPlan.
        The maximum number of consecutive weekends that agents who are assigned to this work plan are allowed to work

        :return: The maximum_consecutive_working_weekends of this WorkPlan.
        :rtype: int
        """
        return self._maximum_consecutive_working_weekends

    @maximum_consecutive_working_weekends.setter
    def maximum_consecutive_working_weekends(self, maximum_consecutive_working_weekends):
        """
        Sets the maximum_consecutive_working_weekends of this WorkPlan.
        The maximum number of consecutive weekends that agents who are assigned to this work plan are allowed to work

        :param maximum_consecutive_working_weekends: The maximum_consecutive_working_weekends of this WorkPlan.
        :type: int
        """
        

        self._maximum_consecutive_working_weekends = maximum_consecutive_working_weekends

    @property
    def minimum_working_days_per_week(self):
        """
        Gets the minimum_working_days_per_week of this WorkPlan.
        The minimum number of days that agents assigned to a work plan must work per week

        :return: The minimum_working_days_per_week of this WorkPlan.
        :rtype: int
        """
        return self._minimum_working_days_per_week

    @minimum_working_days_per_week.setter
    def minimum_working_days_per_week(self, minimum_working_days_per_week):
        """
        Sets the minimum_working_days_per_week of this WorkPlan.
        The minimum number of days that agents assigned to a work plan must work per week

        :param minimum_working_days_per_week: The minimum_working_days_per_week of this WorkPlan.
        :type: int
        """
        

        self._minimum_working_days_per_week = minimum_working_days_per_week

    @property
    def constrain_maximum_consecutive_working_days(self):
        """
        Gets the constrain_maximum_consecutive_working_days of this WorkPlan.
        Whether to constrain the maximum consecutive working days

        :return: The constrain_maximum_consecutive_working_days of this WorkPlan.
        :rtype: bool
        """
        return self._constrain_maximum_consecutive_working_days

    @constrain_maximum_consecutive_working_days.setter
    def constrain_maximum_consecutive_working_days(self, constrain_maximum_consecutive_working_days):
        """
        Sets the constrain_maximum_consecutive_working_days of this WorkPlan.
        Whether to constrain the maximum consecutive working days

        :param constrain_maximum_consecutive_working_days: The constrain_maximum_consecutive_working_days of this WorkPlan.
        :type: bool
        """
        

        self._constrain_maximum_consecutive_working_days = constrain_maximum_consecutive_working_days

    @property
    def maximum_consecutive_working_days(self):
        """
        Gets the maximum_consecutive_working_days of this WorkPlan.
        The maximum number of consecutive days that agents assigned to this work plan are allowed to work. Used if constrainMaximumConsecutiveWorkingDays == true

        :return: The maximum_consecutive_working_days of this WorkPlan.
        :rtype: int
        """
        return self._maximum_consecutive_working_days

    @maximum_consecutive_working_days.setter
    def maximum_consecutive_working_days(self, maximum_consecutive_working_days):
        """
        Sets the maximum_consecutive_working_days of this WorkPlan.
        The maximum number of consecutive days that agents assigned to this work plan are allowed to work. Used if constrainMaximumConsecutiveWorkingDays == true

        :param maximum_consecutive_working_days: The maximum_consecutive_working_days of this WorkPlan.
        :type: int
        """
        

        self._maximum_consecutive_working_days = maximum_consecutive_working_days

    @property
    def minimum_shift_start_distance_minutes(self):
        """
        Gets the minimum_shift_start_distance_minutes of this WorkPlan.
        The time period in minutes for the duration between the start times of two consecutive working days

        :return: The minimum_shift_start_distance_minutes of this WorkPlan.
        :rtype: int
        """
        return self._minimum_shift_start_distance_minutes

    @minimum_shift_start_distance_minutes.setter
    def minimum_shift_start_distance_minutes(self, minimum_shift_start_distance_minutes):
        """
        Sets the minimum_shift_start_distance_minutes of this WorkPlan.
        The time period in minutes for the duration between the start times of two consecutive working days

        :param minimum_shift_start_distance_minutes: The minimum_shift_start_distance_minutes of this WorkPlan.
        :type: int
        """
        

        self._minimum_shift_start_distance_minutes = minimum_shift_start_distance_minutes

    @property
    def minimum_days_off_per_planning_period(self):
        """
        Gets the minimum_days_off_per_planning_period of this WorkPlan.
        Minimum days off in the planning period

        :return: The minimum_days_off_per_planning_period of this WorkPlan.
        :rtype: int
        """
        return self._minimum_days_off_per_planning_period

    @minimum_days_off_per_planning_period.setter
    def minimum_days_off_per_planning_period(self, minimum_days_off_per_planning_period):
        """
        Sets the minimum_days_off_per_planning_period of this WorkPlan.
        Minimum days off in the planning period

        :param minimum_days_off_per_planning_period: The minimum_days_off_per_planning_period of this WorkPlan.
        :type: int
        """
        

        self._minimum_days_off_per_planning_period = minimum_days_off_per_planning_period

    @property
    def maximum_days_off_per_planning_period(self):
        """
        Gets the maximum_days_off_per_planning_period of this WorkPlan.
        Maximum days off in the planning period

        :return: The maximum_days_off_per_planning_period of this WorkPlan.
        :rtype: int
        """
        return self._maximum_days_off_per_planning_period

    @maximum_days_off_per_planning_period.setter
    def maximum_days_off_per_planning_period(self, maximum_days_off_per_planning_period):
        """
        Sets the maximum_days_off_per_planning_period of this WorkPlan.
        Maximum days off in the planning period

        :param maximum_days_off_per_planning_period: The maximum_days_off_per_planning_period of this WorkPlan.
        :type: int
        """
        

        self._maximum_days_off_per_planning_period = maximum_days_off_per_planning_period

    @property
    def minimum_paid_minutes_per_planning_period(self):
        """
        Gets the minimum_paid_minutes_per_planning_period of this WorkPlan.
        Minimum paid minutes in the planning period

        :return: The minimum_paid_minutes_per_planning_period of this WorkPlan.
        :rtype: int
        """
        return self._minimum_paid_minutes_per_planning_period

    @minimum_paid_minutes_per_planning_period.setter
    def minimum_paid_minutes_per_planning_period(self, minimum_paid_minutes_per_planning_period):
        """
        Sets the minimum_paid_minutes_per_planning_period of this WorkPlan.
        Minimum paid minutes in the planning period

        :param minimum_paid_minutes_per_planning_period: The minimum_paid_minutes_per_planning_period of this WorkPlan.
        :type: int
        """
        

        self._minimum_paid_minutes_per_planning_period = minimum_paid_minutes_per_planning_period

    @property
    def maximum_paid_minutes_per_planning_period(self):
        """
        Gets the maximum_paid_minutes_per_planning_period of this WorkPlan.
        Maximum paid minutes in the planning period

        :return: The maximum_paid_minutes_per_planning_period of this WorkPlan.
        :rtype: int
        """
        return self._maximum_paid_minutes_per_planning_period

    @maximum_paid_minutes_per_planning_period.setter
    def maximum_paid_minutes_per_planning_period(self, maximum_paid_minutes_per_planning_period):
        """
        Sets the maximum_paid_minutes_per_planning_period of this WorkPlan.
        Maximum paid minutes in the planning period

        :param maximum_paid_minutes_per_planning_period: The maximum_paid_minutes_per_planning_period of this WorkPlan.
        :type: int
        """
        

        self._maximum_paid_minutes_per_planning_period = maximum_paid_minutes_per_planning_period

    @property
    def optional_days(self):
        """
        Gets the optional_days of this WorkPlan.
        Optional days to schedule for this work plan

        :return: The optional_days of this WorkPlan.
        :rtype: SetWrapperDayOfWeek
        """
        return self._optional_days

    @optional_days.setter
    def optional_days(self, optional_days):
        """
        Sets the optional_days of this WorkPlan.
        Optional days to schedule for this work plan

        :param optional_days: The optional_days of this WorkPlan.
        :type: SetWrapperDayOfWeek
        """
        

        self._optional_days = optional_days

    @property
    def shift_start_variance_type(self):
        """
        Gets the shift_start_variance_type of this WorkPlan.
        This constraint ensures that an agent starts each workday within a user-defined time threshold

        :return: The shift_start_variance_type of this WorkPlan.
        :rtype: str
        """
        return self._shift_start_variance_type

    @shift_start_variance_type.setter
    def shift_start_variance_type(self, shift_start_variance_type):
        """
        Sets the shift_start_variance_type of this WorkPlan.
        This constraint ensures that an agent starts each workday within a user-defined time threshold

        :param shift_start_variance_type: The shift_start_variance_type of this WorkPlan.
        :type: str
        """
        allowed_values = ["ShiftStart", "ShiftStartAndPaidDuration"]
        if shift_start_variance_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for shift_start_variance_type -> " + shift_start_variance_type)
            self._shift_start_variance_type = "outdated_sdk_version"
        else:
            self._shift_start_variance_type = shift_start_variance_type

    @property
    def shift_start_variances(self):
        """
        Gets the shift_start_variances of this WorkPlan.
        Variance in minutes among start times of shifts in this work plan

        :return: The shift_start_variances of this WorkPlan.
        :rtype: ListWrapperShiftStartVariance
        """
        return self._shift_start_variances

    @shift_start_variances.setter
    def shift_start_variances(self, shift_start_variances):
        """
        Sets the shift_start_variances of this WorkPlan.
        Variance in minutes among start times of shifts in this work plan

        :param shift_start_variances: The shift_start_variances of this WorkPlan.
        :type: ListWrapperShiftStartVariance
        """
        

        self._shift_start_variances = shift_start_variances

    @property
    def shifts(self):
        """
        Gets the shifts of this WorkPlan.
        Shifts in this work plan

        :return: The shifts of this WorkPlan.
        :rtype: list[WorkPlanShift]
        """
        return self._shifts

    @shifts.setter
    def shifts(self, shifts):
        """
        Sets the shifts of this WorkPlan.
        Shifts in this work plan

        :param shifts: The shifts of this WorkPlan.
        :type: list[WorkPlanShift]
        """
        

        self._shifts = shifts

    @property
    def agents(self):
        """
        Gets the agents of this WorkPlan.
        Agents in this work plan

        :return: The agents of this WorkPlan.
        :rtype: list[DeletableUserReference]
        """
        return self._agents

    @agents.setter
    def agents(self, agents):
        """
        Sets the agents of this WorkPlan.
        Agents in this work plan

        :param agents: The agents of this WorkPlan.
        :type: list[DeletableUserReference]
        """
        

        self._agents = agents

    @property
    def agent_count(self):
        """
        Gets the agent_count of this WorkPlan.
        Number of agents in this work plan

        :return: The agent_count of this WorkPlan.
        :rtype: int
        """
        return self._agent_count

    @agent_count.setter
    def agent_count(self, agent_count):
        """
        Sets the agent_count of this WorkPlan.
        Number of agents in this work plan

        :param agent_count: The agent_count of this WorkPlan.
        :type: int
        """
        

        self._agent_count = agent_count

    @property
    def metadata(self):
        """
        Gets the metadata of this WorkPlan.
        Version metadata for this work plan

        :return: The metadata of this WorkPlan.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this WorkPlan.
        Version metadata for this work plan

        :param metadata: The metadata of this WorkPlan.
        :type: WfmVersionedEntityMetadata
        """
        

        self._metadata = metadata

    @property
    def self_uri(self):
        """
        Gets the self_uri of this WorkPlan.
        The URI for this object

        :return: The self_uri of this WorkPlan.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this WorkPlan.
        The URI for this object

        :param self_uri: The self_uri of this WorkPlan.
        :type: str
        """
        

        self._self_uri = self_uri

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

