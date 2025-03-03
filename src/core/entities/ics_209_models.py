from datetime import date, time
from typing import Optional

from sqlalchemy import Time, BigInteger
from sqlmodel import Field, Relationship, SQLModel, Column

class Ics209(SQLModel, table=True):
    __tablename__ = "ics_209"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )
    report_version: str
    report_number: str
    incident_commander_id: Optional[int] = Field(
        default=None, foreign_key="incident_commander.id", ondelete="CASCADE"
    )
    incident_source: str
    is_source_ctrl: Optional[bool]
    materials_release: str
    is_material_ctrl: Optional[bool]
    response_status: str
    
    is_acc: Optional[bool]
    acc_num: Optional[int]
    is_acc_mustered: Optional[bool]
    is_acc_sheltered: Optional[bool]
    is_acc_evacuated: Optional[bool]
    
    is_unacc: Optional[bool]
    unacc_num: Optional[int]
    unacc_emp: Optional[int]
    unacc_con: Optional[int]
    unacc_oth: Optional[int]
    
    is_injured: Optional[bool]
    inj_num: Optional[int]
    inj_emp: Optional[int]
    inj_con: Optional[int]
    inj_oth: Optional[int]
    
    is_dead: Optional[bool]
    dead_num: Optional[int]
    dead_emp: Optional[int]
    dead_con: Optional[int]
    dead_oth: Optional[int]
    
    env_impact: str
    env_desc: str
    comm_impact: str
    comm_desc: str
    ops_impact: str
    ops_desc: str
    
    events_period: str
    obj_next_period: str
    actions_next_period: str
    res_needed: str
    est_completion_date: Optional[date]
    est_res_democ_start: Optional[date]
    cost_to_date: int = Field(sa_column=Column(BigInteger()))
    final_cost_est: int = Field(sa_column=Column(BigInteger()))
    
    gov_contact: str
    media_contact: str
    kin_contact: str
    shareholder_contact: str
    comm_rep_contact: str
    ngo_contact: str
    
    ics_209_preparation: Optional["Ics209Preparation"] = Relationship(
        back_populates="ics_209",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_209_approval: Optional["Ics209Approval"] = Relationship(
        back_populates="ics_209",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_209"
    )
    incident_commander: Optional["IncidentCommander"] = Relationship(
        back_populates="ics_209"
    )
    

class Ics209Preparation(SQLModel, table=True):
    __tablename__ = "ics_209_preparation"
    id: int = Field(default=None, primary_key=True)
    ics_209_id: Optional[int] = Field(default=None, foreign_key="ics_209.id", ondelete="CASCADE")
    situation_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="situation_unit_leader.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))
    
    situation_unit_leader: Optional["SituationUnitLeader"] = Relationship(
        back_populates="ics_209_preparation",
    )
    ics_209: Optional["Ics209"] = Relationship(back_populates="ics_209_preparation")
    

class Ics209Approval(SQLModel, table=True):
    __tablename__ = "ics_209_approval"
    id: int = Field(default=None, primary_key=True)
    ics_209_id: Optional[int] = Field(default=None, foreign_key="ics_209.id", ondelete="CASCADE")
    incident_commander_id: Optional[int] = Field(
        default=None, foreign_key="incident_commander.id", ondelete="CASCADE"
    )
    is_approved: bool
    date_approved: Optional[date]
    time_approved: Optional[time] = Field(sa_column=Field(sa_type=Time))
    
    incident_commander: Optional["IncidentCommander"] = Relationship(
        back_populates="ics_209_approval",
    )
    ics_209: Optional["Ics209"] = Relationship(back_populates="ics_209_approval")