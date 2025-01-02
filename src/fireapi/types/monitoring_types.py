from typing import Dict, List

from pydantic import BaseModel, Field


class TimingEntry(BaseModel):
    date: str
    cpu: str
    mem: str
    ping: int


class MonitoringTimingsData(BaseModel):
    timings: List[TimingEntry]


class MonitoringTimings(BaseModel):
    status: str
    requestID: str
    message: str
    data: MonitoringTimingsData


class Incidence(BaseModel):
    start: str
    end: str
    downtime: int
    type: str = Field(..., description="Type of the detected outage")


class StatisticEntry(BaseModel):
    downtime: int
    availability: float
    incidences: int
    longest_incidence: int
    average_incidence: float


class MonitoringIncidencesData(BaseModel):
    statistic: Dict[str, StatisticEntry] = Field(
        ...,
        description="Statistics for different time periods (LAST_24_HOURS, LAST_7_DAYS, etc.)",
    )
    incidences: List[Incidence]


class MonitoringIncidences(BaseModel):
    status: str
    requestID: str
    message: str
    data: MonitoringIncidencesData
